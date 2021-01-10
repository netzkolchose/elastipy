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


def accidents_by_city():
    s = search()
    # make sure we have a population value
    s = s.range(field="population", gt=0)

    agg = s.agg_terms("city", field="city", size=30)

    # the pipeline aggregation below does not have access to the city.doc_count
    #   so we repeat the count value here as a metric
    agg.metric_value_count("count", field="city")
    agg.metric_avg("population", field="population")
    agg.metric_avg("density", field="population_density")

    # divide number of accidents by population size
    agg.pipeline_bucket_script(
        "accidents_per_population_percent",
        buckets_path={
            "accidents": "count",
            "population": "population"
        },
        script="params.accidents / params.population * 100"
    )

    s.execute()

    print("\n### Accidents by city\n")
    agg.print.table(digits=2, sort="-accidents_per_population_percent", zero_based=True)


def accidents_by_weekday():
    s = search()

    # one still has to know the syntax of the order parameter
    #   maybe i'll wrap it up in a class as well..
    agg = s.agg_terms("weekday", field="weekday", order={"_key": "asc"})
    add_vehicle_metrics(agg)

    s.execute()

    print("\n### Accidents by weekday\n")
    agg.print.table(digits=3)


def accidents_by_hour():
    s = search()

    agg = s.agg_histogram("hour", field="hour", interval=1, order={"_key": "asc"})
    add_vehicle_metrics(agg)

    s.execute()

    print("\n### Accidents by hour\n")
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
    #   and all bucket keys that lead to it
    data = agg.to_dict()
    print("number of accidents on slick roads in the dark", data[("darkness", "slick")])


def accidents_by_vehicle_combination():
    s = search()
    agg = s \
        .agg_adjacency_matrix("combi", filters={
            "truck": query.Term(field="truck", value=1),
            "car": query.Term(field="car", value=1),
            "motorcycle": query.Term(field="motorcycle", value=1),
            "bicycle": query.Term(field="bicycle", value=1),
            "pedestrian": query.Term(field="pedestrian", value=1),
            "other": query.Term(field="other", value=1),
        }) \
        .metric_avg("lightly", field="lightly_i") \
        .metric_avg("seriously", field="seriously_i") \
        .metric_avg("deadly", field="deadly_i")
        #.metric_percentile_ranks("category", field="category_i", values=[0, 1, 2])

    s.execute()

    print("\n### Accidents by vehicle combination\n")
    agg.print.table(sort="-combi.doc_count", digits=2, zero_based=True)


def accidents_geo_centroid_per_state():
    s = search()
    agg = s \
        .agg_terms("state", field="state", size=16) \
        .metric_geo_centroid("centroid", field="location")

    s.execute()

    print("\n### Accidents geo-centroid per state\n")
    # it's not possible to order the terms aggregation along a centroid coordinate
    # but we can at least order the table output
    agg.print.table(digits=5, sort="centroid.lat")


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
accidents_by_city()
accidents_by_weekday()
accidents_by_hour()
accidents_by_condition()
accidents_by_vehicle_combination()
accidents_geo_centroid_per_state()
accidents_geo_bounds_per_state()
accidents_geotile_grid()

