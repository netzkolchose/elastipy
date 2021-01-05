"""
Run accidents_export.py first and then have fun with this script
"""
from helper import Search, query
from accidents_export import AccidentExporter


# search in this elasticsearch index
def search():
    return Search(index=AccidentExporter().index_name())


def accidents_by_state():
    # get a search instance
    s = search()
    # add an aggregation
    agg = s.agg_terms("state", field="state", size=16)
    # call the REST api
    s.execute()

    # print all received data points
    print("\n### Accidents by state\n")
    agg.print.table()


# a function to add some metrics to an aggregation
def add_vehicle_metrics(agg):
    # Since the boolean flags for the vehicle type are integer values
    #   we can just count the average and get the ratio between 0 and 1.
    # The agg.print.table() as well as the agg.dict_rows() methods
    #   return all values including contained metrics
    agg.metric_avg("with trucks", field="truck")
    agg.metric_avg("with cars", field="car")
    agg.metric_avg("with motorcycles", field="motorcycle")
    agg.metric_avg("with bicycles", field="bicycle")
    agg.metric_avg("with pedestrians", field="foot")
    agg.metric_avg("with other", field="other")


def accidents_by_state_more_precise():
    s = search()

    # query each category separately
    for category in (None, "lightly", "seriously", "deadly"):
        if category:
            s2 = s.term(field="category", value=category)
        else:
            # make a copy to not mess up the original Search instance
            s2 = s.copy()

        agg = s2.agg_terms("state", field="state", size=16)
        add_vehicle_metrics(agg)

        s2.execute()

        print("\n### Accidents by state (category: %s)\n" % ("all" if not category else category))
        agg.print.table(digits=3)


def accidents_by_weekday():
    s = search()

    # one still has to know the syntax of the order parameter
    #   maybe i'll wrap it up in a class as well..
    agg = s.agg_terms("weekday", field="weekday", order={"_key": "asc"})
    add_vehicle_metrics(agg)

    s.execute()

    print("\n### Accidents by weekday\n")
    agg.print.table(digits=3)


def accidents_by_condition():
    s = search()
    # nested aggregations can be joined
    agg = s \
        .agg_terms("light", field="light") \
        .agg_terms("street", field="street_condition")

    s.execute()

    print("\n### Accidents by condition\n")
    agg.print.table()

    # the to_dict method returns the values of the chosen aggregation
    #   but all keys that lead to it
    data = agg.to_dict()
    print("number of accidents on slick roads in the dark", data[("darkness", "slick")])


def accidents_by_vehicle_combination():
    s = search()
    agg = s \
        .agg_adjacency_matrix(filters={
            "truck": query.Term(field="truck", value=1),
            "car": query.Term(field="car", value=1),
            "motorcycle": query.Term(field="motorcycle", value=1),
            "bicycle": query.Term(field="bicycle", value=1),
            "pedestrian": query.Term(field="pedestrian", value=1),
            "other": query.Term(field="other", value=1),
        })

    s.execute()

    print("\n### Accidents by vehicle combination\n")
    agg.print.table()


def accidents_geo_centroid_per_state():
    s = search()
    agg = s \
        .agg_terms("state", field="state", size=16) \
        .metric_geo_centroid("centroid", field="location")

    s.execute()

    print("\n### Accidents geo-centroid per state\n")
    agg.print.table(digits=5)


def accidents_geo_bounds_per_state():
    s = search()
    agg = s \
        .agg_terms("state", field="state", size=16) \
        .metric_geo_bounds("bounds", field="location")

    s.execute()

    print("\n### Accidents geo-bounds per state\n")
    agg.print.table(digits=5)


def accidents_geotile_grid():
    s = search()
    agg = s.agg_geotile_grid("grid", field="location", precision=6)

    s.execute()

    print("\n### Accidents geo-grid")
    print("(The key represents zoom-level/X/Y, see https://en.wikipedia.org/wiki/Tiled_web_map\n")
    agg.print.table()


#accidents_by_state()
accidents_by_state_more_precise()
accidents_by_weekday()
accidents_by_condition()
accidents_by_vehicle_combination()
accidents_geo_centroid_per_state()
accidents_geo_bounds_per_state()
accidents_geotile_grid()
