## elastipy

A python wrapper to make elasticsearch queries and aggregations more fun.

Actually i'm just learning this stuff and have the following requests:
- some generic convenient data access to nested bucketed aggregations and such
- the IDE/auto-completion should help a bit/lot with all the elasticsearch parameters


#### aggregation example

```python
from elastipy import Search

# get a search object
q = Search(index="world")

# if we leave out the field parameter it fall's back to Search.timestamp_field 
#   which is "timestamp" by default
agg = q.agg_date_histogram(calendar_interval="1w")

# submit the whole request
q.execute()

list(agg.keys())
# ["2020-01-01T00:00:00Z", "2020-01-08T00:00:00Z", ...]
list(agg.values())
# [3437438, 4985459, 7343874, ...]  # without a metric these are the doc_counts

# above example as a one-liner
Search(index="world").agg_date_histogram(calendar_interval="1w").execute().to_dict()
# {
#   "2020-01-01T00:00:00Z": 3437438,
#   "2020-01-08T00:00:00Z": 4985459,
#   ...
# } 
```

Nested aggregations and metrics:
```python
from elastipy import Search

q = Search(index="world")

# the first parameter is the name of the aggregation 
#   (if omitted it will be "a0", "a1", aso..)  
agg = q \
    .agg_terms("occasion", field="occasion") \
    .agg_rare_terms("rare-excuses", field="excuse") \
    .metric_avg("avg-length", field="conversation_length") \
    .metric_max("max-length", field="conversation_length") \
    .execute()
# the rare_terms aggregation is nested into the terms aggregation
# the metrics are siblings nested inside rare_terms

# keys(), values(), items() and to_dict() all operate on the current aggregation
#   for bucket aggregations they typically show the doc_count value
agg.to_dict()
# {
#     ("dinner", "my mouth is too dry"): 100,
#     ("dinner", "i can't reach the spoon"): 60,
# }

# the dict_rows() and print.table() methods operate on the whole aggregation branch
agg.dict_rows()
# [
#     {
#         "occasion": "dinner", 
#         "occasion.doc_count": 1234567, 
#         "rare-excuses": "my mouth is too dry", 
#         "rare-excuses.doc_count": 100, 
#         "avg-length": 12.7, 
#         "max-length": 122.3, 
#     },
#     {
#         "occasion": "dinner", 
#         "occasion.doc_count": 1234567, 
#         "rare-excuses": "i can't reach the spoon", 
#         "rare-excuses.doc_count": 60, 
#         "avg-length": 5.1, 
#         "max-length": 27.0, 
#     }
# ]

agg.print.table()
# ocassion | occasion.doc_count | rare-excuses            | rare-excuses.doc_count | avg-length | max-length
# dinner   | 1234567            | my mouth is too dry     | 100                    | 12.7       | 122.3
# dinner   | 1234567            | i can't reach the spoon | 60                     | 5.1        | 27.0
```

#### query example

The querying is a bit similar to [elasticsearch-dsl](https://github.com/elastic/elasticsearch-dsl-py) 
but there are also methods for each supported query on the **Search** object.  

```python
from elastipy import Search, query

q = Search(index="world")
# chaining means AND
q = q.term(field="category", value="programming").term("usage", "widely-used")
# also can use operators
q = q & (query.Term("topic", "yet-another-api") | query.Term("topic", "yet-another-operator-overload"))

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

# .query() replaces the current query 
q = q.query(query.MatchAll())
```

There is some housekeeping and glue code for the basics. The methods for queries and aggregations as 
well as the query classes are auto-generated from [yaml files](definition). They include all parameters,
default values and documentation.

#### export example

There is a small helper to export stuff to elasticsearch.

```python
from elastipy import Exporter

class MyExporter(Exporter):
    INDEX_NAME = "my-index"
    
    # mapping can be defined here
    # it will be sent to elasticsearch before the first document is exported 
    MAPPING = {
        "properties": {
            "some_field": {"type": "text"},
        }       
    }   

Exporter().export_list(a_lot_of_objects)    
```
It uses bulk requests and is very fast, supports document transformation and
control over id and sub-index of documents.

```python
import datetime
from elastipy import Exporter

class MyExporter(Exporter):
    INDEX_NAME = "my-index-*"
    
    # if each document has a unique id value we can use it
    # as the elasticsearch id as well. That way we do not
    # create documents twice when exporting them again.
    # Their data just gets updated.
    def get_document_id(self, es_data):
        return es_data["id"]
    
    # we can bucket documents into separate indices 
    def get_document_index(self, es_data):
        return self.index_name().replace("*", es_data["group"])
    
    # here we can adjust or add some data before it gets exported.
    # it's also possible to split the data into several documents
    #   by yielding or returning a list
    def transform_document(self, data):
        data = data.copy()
        data["timestamp"] = datetime.datetime.now()
        return data

Exporter().export_list(a_lot_of_objects)

# if we are tired enough we can call
Exporter().delete_index()
# This would actually delete all sub-indices because 
#   there's this '*' in the INDEX_NAME
```

**More examples can be found [here](examples).**


#### The big steps to success

  - make sure that all the combinations of queries work as expected
  - finalize the generic keys/values gathering from all those different aggregations with all their little 
  peculiarities
  - complete the yaml definitions by carefully reading all the 
   [online documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
  - a convenient way to declare the client connection settings


### development / testing

Still a bit *bastlerisch* at this point. 

The unit-tests run against elasticsearch at localhost:9200 with all indices 
prefixed with **elastipy---unittest-**