"""
Exports data of german car accidents to index 'elastipy-example-accidents'

Data is from https://unfallatlas.statistikportal.de/_opendata2020.html
    "Unfallatlas | Kartenanwendung der Statistischen Ämter des Bundes und der Länder"

and https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/_inhalt.html
    "Gemeindeverzeichnis-Informationssystem GV-ISys. Herausgeber: Statistische Ämter des Bundes und der Länder"

You may excuse this geological restriction. I just live there and it's always
more interesting to look at data involving your own environment.

"""

import csv
import zipfile
from io import TextIOWrapper

from helper import get_web_file, Exporter


# --- a few conversions of integers from the CSV ---

# the number prefix is to make them sortable alphabetically
WEEKDAYS = (
    "01 Sunday",
    "02 Monday",
    "03 Tuesday",
    "04 Wednesday",
    "05 Thursday",
    "06 Friday",
    "07 Saturday",
)

CATEGORIES = (
    "deadly",
    "seriously",  # injured
    "lightly"
)

FEDERAL_STATES = (
    "Schleswig-Holstein",
    "Hamburg",
    "Niedersachsen",
    "Bremen",
    "Nordrhein-Westfalen",
    "Hessen",
    "Rheinland-Pfalz",
    "Baden-Württemberg",
    "Bayern",
    "Saarland",
    "Berlin",
    "Brandenburg",
    "Mecklenburg-Vorpommern",
    "Sachsen",
    "Sachsen-Anhalt",
    "Thüringen",
)

# below stuff was translated using deepl.com

KINDS = (
    "other",
    "collision with approaching/stopping/stationary vehicle",
    "collision with vehicle ahead/waiting vehicle",
    "collision with vehicle driving sideways in the same direction",
    "collision with oncoming vehicle",
    "collision with turning/crossing vehicle",
    "collision between vehicle and pedestrian",
    "impact with road obstacle",
    "coming off lane to the right",
    "coming off lane to the left",
)

TYPES = (
    "driving",
    "turning",
    "turning/crossing",
    "crossing",
    "stationary",
    "longitudinal",
    "other",
)

LIGHTS = (
    "daylight",
    "twilight",
    "darkness",
)

STREET_CONDITIONS = (
    "dry",
    "wet",
    "slick",
)


# --- subclass the Exporter and define all the fields

class AccidentExporter(Exporter):
    INDEX_NAME = "elastipy-example-car-accidents"
    MAPPINGS = {
        "properties": {
            "id": {"type": "keyword"},
            "state": {"type": "keyword"},
            "city": {"type": "keyword"},
            "area": {"type": "float"},
            "population": {"type": "integer"},
            "population_density": {"type": "float"},
            # "street": {"type": "keyword"},
            "timestamp": {"type": "date"},
            "weekday": {"type": "keyword"},
            "hour": {"type": "integer"},
            # we keep the untranslated integer just in case someone wants to math with it
            "category_i": {"type": "integer"},
            "category": {"type": "keyword"},
            "kind_i": {"type": "integer"},
            "kind": {"type": "keyword"},
            "type_i": {"type": "integer"},
            "type": {"type": "keyword"},
            "light_i": {"type": "integer"},
            "light": {"type": "keyword"},
            "bicycle": {"type": "integer"},
            "car": {"type": "integer"},
            "foot": {"type": "integer"},
            "motorcycle": {"type": "integer"},
            "truck": {"type": "integer"},
            "other": {"type": "integer"},
            "street_condition_i": {"type": "integer"},
            "street_condition": {"type": "keyword"},
            "location": {"type": "geo_point"},
        }
    }

    def get_document_id(self, es_data):
        return es_data["id"]

    # here we convert a single line from the CSV to the elasticsearch object
    def transform_document(self, data):
        try:
            code = "".join((data["ULAND"], data["UREGBEZ"], data["UKREIS"], data["UGEMEINDE"]))

            # map the administrative code to some geographic data
            if code in self.mapping_data:
                geographic = self.mapping_data[code]
            else:
                # print(f"not found {code}")
                geographic = dict()
                self.codes_not_found.add(code)

            return {
                "id": data["OBJECTID"],
                "state": FEDERAL_STATES[int(data["ULAND"])-1],
                **geographic,
                # Berlin has a street in there but it's not in the federal data
                # "street": data["STRASSE"],

                # the day-of-month is unknown so we explicitly say beginning of month in UTC (note the 'Z')
                "timestamp": "{:04}-{:02}-01T00:00:00Z".format(int(data["UJAHR"]), int(data["UMONAT"])),
                "weekday": WEEKDAYS[int(data["UWOCHENTAG"]) - 1],
                "hour": data["USTUNDE"],
                "category_i": data["UKATEGORIE"],
                "category": CATEGORIES[int(data["UKATEGORIE"]) - 1],
                "kind_i": data["UART"],
                "kind": KINDS[int(data["UART"])],
                "type_i": data["UTYP1"],
                "type": TYPES[int(data["UTYP1"]) - 1],
                "light_i": data["ULICHTVERH"],
                "light": LIGHTS[int(data["ULICHTVERH"])],
                "bicycle": data["IstRad"],
                "car": data["IstPKW"],
                "foot": data["IstFuss"],
                "motorcycle": data["IstKrad"],
                "truck": data["IstGkfz"],
                "other": data["IstSonstige"],
                "street_condition_i": data["STRZUSTAND"],
                "street_condition": STREET_CONDITIONS[int(data["STRZUSTAND"])],
                "location": {
                    "lat": data["YGCSWGS84"].replace(",", "."),
                    "lon": data["XGCSWGS84"].replace(",", "."),
                }
            }
        except BaseException as e:
            print("WHEN CONVERTING:", data)
            raise


def load_data():
    """
    Description is here:
        https://www.opengeodata.nrw.de/produkte/transport_verkehr/unfallatlas/DSB_Unfallatlas.pdf
    """
    filename = get_web_file(
        "https://www.opengeodata.nrw.de/produkte/transport_verkehr/unfallatlas/Unfallorte2019_EPSG25832_CSV.zip",
        "car-accidents-2019.zip",
    )
    with open(filename, "rb") as fp:
        with zipfile.ZipFile(fp) as zfp:
            with zfp.open("csv/Unfallorte2019_LinRef.txt") as csv_binary:
                with TextIOWrapper(csv_binary, encoding="latin1") as csv_text:
                    reader = csv.DictReader(csv_text, delimiter=";")
                    return list(reader)


def load_mapping_data():
    """
    Mapping of code to city name and some geographic data
    """
    FILES = {
        2018: (
            "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GV100ADJ/GV100AD31122018.zip?__blob=publicationFile",
            "GV100AD_311218.ASC",
            "iso-8859-1"
        ),
        2019: (
            "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GV100ADJ/GV100AD31122019.zip?__blob=publicationFile",
            "GV100AD_311219.ASC",
            "utf-8"
        ),
        2020: (
            "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GV100ADQ/GV100AD3011.zip?__blob=publicationFile",
            "GV100AD_301120.asc",
            "utf-8"
        )
    }

    lines = []
    for year, (url, text_filename, encoding) in FILES.items():
        filename = get_web_file(url, f"gemeindeverzeichnis-{year}.zip")
        with open(filename, "rb") as fp:
            with zipfile.ZipFile(fp) as zfp:
                with zfp.open(text_filename) as csv_binary:
                    with TextIOWrapper(csv_binary, encoding=encoding) as csv_text:
                        lines += csv_text.readlines()

    def _int(v):
        try:
            return int(v.lstrip("0"))
        except ValueError:
            return None

    def _float(v):
        try:
            v = v.lstrip("0")
            return float(v[:-2] + "." + v[-2:])
        except ValueError:
            return None

    data = {
        l[10:18]: {
            "city": l[22:72].strip().split(",")[0],
            "zipcode": l[165:170],
            "area": _float(l[128:139]),
            "population": _int(l[139:150]),
        }
        for l in lines
    }

    for entry in data.values():
        try:
            entry["population_density"] = entry["population"] / entry["area"]
        except (TypeError, ZeroDivisionError):
            pass

    return data


def export_data():
    # load accident data
    data = load_data()

    # create exporter instance
    exporter = AccidentExporter()

    # attach the code to geographic mapping data to the exporter
    #   so we can reach it from the transform_object_data method
    exporter.mapping_data = load_mapping_data()
    exporter.codes_not_found = set()

    # create the index or update it's mapping
    exporter.update_index()

    # export everything
    exporter.export_list(data, verbose=True, chunk_size=10000)

    # well... 'open' administrative data is still 'administrative'
    if exporter.codes_not_found:
        print(len(exporter.codes_not_found), "administrative codes not mapped")


if __name__ == "__main__":
    export_data()
    #print(load_data()[:10])
    #data = load_mapping_data()
    #print(data["11000000"])
