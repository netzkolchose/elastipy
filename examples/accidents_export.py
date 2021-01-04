"""
Exports data of german car accidents to index 'elastipy-example-accidents'

Data is from https://unfallatlas.statistikportal.de/_opendata2020.html
    "Unfallatlas | Kartenanwendung der Statistischen Ämter des Bundes und der Länder"

You may excuse this geological restriction. I just live there and it's always
more interesting to look at data involving you everyday life.

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
    "lightly"  # injured
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


# we subclass the Exporter and define all the fields

class AccidentExporter(Exporter):
    INDEX_NAME = "elastipy-example-car-accidents"
    MAPPINGS = {
        "properties": {
            "id": {"type": "keyword"},
            "state": {"type": "keyword"},
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
        }
    }

    def get_object_id(self, es_data):
        return es_data["id"]

    # here we convert a single line from the CSV to the elasticsearch object
    def transform_object_data(self, data):
        try:
            return {
                "id": data["OBJECTID"],
                "state": FEDERAL_STATES[int(data["ULAND"])-1],
                # TODO: actually there are a few more geographic fields which need big conversion lists...
                # TODO: also there are geo coordinates in there
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


def export_data():
    data = load_data()
    exporter = AccidentExporter()
    exporter.update_index()
    exporter.export_list(data)


if __name__ == "__main__":
    export_data()
