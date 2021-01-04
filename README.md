## elastipy

A python wrapper to make elasticsearch queries and aggregations more fun.

Actually i'm just learning this stuff and have the following requests:
- some generic convenient data access to nested bucketed aggregations and such
- the IDE/auto-completion should help a bit/lot with all the elasticsearch parameters

This library is a bit similar to [elasticsearch-dsl](https://github.com/elastic/elasticsearch-dsl-py),
you just don't have to study the documentation pages all the time. 

```python
from elastipy import Search

q = Search(index="world")
agg = q.agg_date_histogram(field="timestamp", fixed_interval="1w")
q.execute()

list(agg.keys())
# ["2020-01-01T00:00:00Z", "2020-01-08T00:00:00Z", ...]
list(agg.values())
# [3437438, 4985459, 7343874, ...]  # without a metric these are the doc_counts

# short form of the above
Search(index="world").agg_date_histogram(field="timestamp", fixed_interval="1w").execute().to_dict()
```
It's really cool if your IDE's auto-completion helps you with this stuff. 

Example with queries involved:
```python
from elastipy import Search, query

q = Search(index="world")
q = q.term("topic", "yet-another-api") | query.Term("topic", "yet-another-operator-overload")

languages_per_country = q.agg_terms(field="country").agg_terms(field="language").execute()

languages_per_country.to_dict()
# {
#     ('DE', 'Python'): 3197,
#     ('DE', 'C++'): 1701,
#     ('DE', 'php'): 52,
#     ('ES', 'Python'): 5104,
#     ('ES', 'C++'): 1201,
#     ('ES', 'php'): 77,
#     ...
# }
```

There is some housekeeping and glue code for the basics. The methods for queries and aggregations as 
well as the query classes are auto-generated from [yaml files](definition). They include all parameters,
default values and documentation.

Have a look at the [examples](examples).


#### The big steps to success

  - make sure that all the combinations of queries work as expected
  - finalize the generic keys/values gathering from all those different aggregations with all their little 
  peculiarities
  - complete the yaml definitions by carefully reading all the 
   [online documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)



### development / testing

Still a bit *bastlerisch* at this point. 

The unit-tests run against elasticsearch at localhost:9200 with all indices 
prefixed with **elastipy---unittest-**