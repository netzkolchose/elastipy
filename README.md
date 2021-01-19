## elastipy

[![Build Status](https://travis-ci.com/defgsus/elastipy.svg?branch=development)](https://travis-ci.com/defgsus/elastipy)
[![Coverage Status](https://coveralls.io/repos/github/defgsus/elastipy/badge.svg?branch=feature/travis)](https://coveralls.io/github/defgsus/elastipy?branch=feature/travis)
[![Documentation Status](https://readthedocs.org/projects/elastipy/badge/?version=latest)](https://elastipy.readthedocs.io/en/latest/?badge=latest)

A python wrapper to make elasticsearch queries and aggregations more fun.

Lean more at [readthedocs.io](https://elastipy.readthedocs.io/en/latest/)

Actually i'm just learning this stuff and have the following requests:
- some generic convenient data access to nested bucketed aggregations and such
- the IDE/auto-completion should help a bit/lot with all the elasticsearch parameters

---

- [requirements](#requirements)
- quickref
    - [aggregations](#aggregations)
    - [metrics](#nested-aggregations-and-metrics)
    - [query](#queries)
    - [exporting](#exporting)
- [testing](#testing)
- [development](#development)

---

#### requirements

One thing is, of course, to [install elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html).

- **elastipy** itself requires [elasticsearch-py](https://github.com/elastic/elasticsearch-py)
- doc building is listed in [docs/requirements.txt](docs/requirements.txt) and mainly
consists of sphinx with the readthedocs theme.
- generating the interface and running the tests and notebooks is listed in 
[requirements.txt](requirements.txt) and contains pyyaml and coverage as well as the 
usual stack of jupyter, scipy, matplotlib, ..   

















### configuration 

By default an [elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html) host is expected at `localhost:9200`. There are currently two ways 
to specify a different connection.


```python
from elasticsearch import Elasticsearch
from elastipy import Search

# Use an explicit Elasticsearch client (or compatible class)
client = Elasticsearch(
    hosts=[{"host": "localhost", "port": 9200}], 
    http_auth=("user", "pwd")
)

# create a Search using the specified client
s = Search(index="bla", client=client)

# can also be done later
s = s.client(client)
```

Check the Elasticsearch [API reference](https://elasticsearch-py.readthedocs.io/en/v7.10.1/api.html#elasticsearch) for all the parameters.

We can also set a default client at the program start:  


```python
from elastipy import connections

connections.set("default", client)

# .. or as parameters, they get converted to an Elasticsearch client
connections.set("default", {"hosts": [{"host": "localhost", "port": 9200}]})

# get a client
connections.get("default")
```




    <Elasticsearch([{'host': 'localhost', 'port': 9200}])>



Different connections can be specified with the *alias* name:


```python
connections.set("special", {"hosts": [{"host": "special", "port": 1234}]})

s = Search(client="special")
s.get_client()
```




    <Elasticsearch([{'host': 'special', 'port': 1234}])>



### aggregations

More details can be found in the [tutorial](https://elastipy.readthedocs.io/en/latest/tutorial.html).


```python
# get a search object
s = Search(index="world")

# create an Aggregation class connected to the Search
agg = s.agg_date_histogram(calendar_interval="1w")
# (for date-specific aggregations we can leave out the 'field' parameter 
#  it fall's back to Search.timestamp_field which is "timestamp" by default)

# submit the whole request
s.execute()

# access the response

list(agg.keys())
```




    ['1999-12-27T00:00:00.000Z',
     '2000-01-03T00:00:00.000Z',
     '2000-01-10T00:00:00.000Z',
     '2000-01-17T00:00:00.000Z']




```python
list(agg.values())
```




    [21, 77, 60, 42]



Without a [metric](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics.html) these numbers are the document counts.

Above example as a one-liner:


```python
Search(index="world").agg_date_histogram(calendar_interval="1w").execute().to_dict()
```




    {'1999-12-27T00:00:00.000Z': 21,
     '2000-01-03T00:00:00.000Z': 77,
     '2000-01-10T00:00:00.000Z': 60,
     '2000-01-17T00:00:00.000Z': 42}



### nested aggregations and metrics


```python
s = Search(index="world")

# the first parameter is the name of the aggregation 
#   (if omitted it will be "a0", "a1", aso..)  
agg = s \
    .agg_terms("occasion", field="occasion") \
    .agg_rare_terms("rare-excuses", field="excuse", max_doc_count=2) \
    .metric_avg("avg-length", field="conversation_length") \
    .metric_max("max-length", field="conversation_length") \
    .execute()
```

The `rare_terms` aggregation is nested into the `terms` aggregation and 
the metrics are siblings nested inside `rare_terms`.

`keys()`, `values()`, `items()` and `to_dict()` all operate on the current aggregation.
For bucket aggregations they typically show the `doc_count` value.'


```python
agg.to_dict()
```




    {('dinner', 'my mouth is too dry'): 1,
     ('dinner', "i can't reach the spoon"): 2}



The `rows()`, `dict_rows()` and `dump.table()` methods operate on the whole aggregation branch:


```python
list(agg.dict_rows())
```




    [{'occasion': 'dinner',
      'occasion.doc_count': 200,
      'rare-excuses': 'my mouth is too dry',
      'rare-excuses.doc_count': 1,
      'avg-length': 163.0,
      'max-length': 163.0},
     {'occasion': 'dinner',
      'occasion.doc_count': 200,
      'rare-excuses': "i can't reach the spoon",
      'rare-excuses.doc_count': 2,
      'avg-length': 109.5,
      'max-length': 133.0}]




```python
agg.dump.table(colors=False)
```

    occasion │ occasion.doc_count │ rare-excuses            │ rare-excuses.doc_count │ avg-length   │ max-length  
    ─────────┼────────────────────┼─────────────────────────┼────────────────────────┼──────────────┼─────────────
    dinner   │ 200                │ my mouth is too dry     │ 1 ██████████▌          │ 163.0 ██████ │ 163.0 ██████
    dinner   │ 200                │ i can't reach the spoon │ 2 ████████████████████ │ 109.5 ████   │ 133.0 ████▉ 


### queries


```python
from elastipy import query

s = Search(index="prog-world")

# chaining means AND
s = s \
    .term(field="category", value="programming") \
    .term("usage", "widely-used")

# also can use operators
s = s & (
    query.Term("topic", "yet-another-api") 
    | query.Term("topic", "yet-another-operator-overload")
)

# .query() replaces the current query 
s = s.query(query.MatchAll())

languages_per_country = s.agg_terms(field="country").agg_terms(field="language").execute()

languages_per_country.to_dict()
```




    {('IT', 'PHP'): 28,
     ('IT', 'Python'): 24,
     ('IT', 'C++'): 21,
     ('ES', 'C++'): 29,
     ('ES', 'Python'): 22,
     ('ES', 'PHP'): 18,
     ('US', 'PHP'): 23,
     ('US', 'Python'): 20,
     ('US', 'C++'): 15}



### exporting

There is a small helper to export stuff to elasticsearch.




```python
from elastipy import Exporter

class MyExporter(Exporter):
    INDEX_NAME = "my-index"
    
    # mapping can be defined here
    # it will be sent to elasticsearch before the first document is exported 
    MAPPINGS = {
        "properties": {
            "some_field": {"type": "text"},
        }       
    }   

count, errors = MyExporter().export_list(a_lot_of_objects)

print(f"expored {count} objects, errors: {errors}")
```

    expored 1000 objects, errors: []


It uses bulk requests and is very fast, supports document transformation and
control over id and sub-index of documents.


```python
import datetime

class MyExporter(Exporter):
    INDEX_NAME = "my-index-*"
    MAPPINGS = {
        "properties": {
            "some_field": {"type": "text"},
            "group": {"type": "keyword"},
            "id": {"type": "keyword"},
            "timestamp": {"type": "date"},
        }       
    }   

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

MyExporter().export_list(a_lot_of_objects)
```




    (1000, [])



If we are tired enough we can call:


```python
MyExporter().delete_index()
```




    True



This will actually delete all sub-indices because there's this wildcard `*` in the `INDEX_NAME`.


**More examples can be found [here](examples).**


#### The big steps to success

  - make sure that all the combinations of queries work as expected
  - finalize the generic keys/values gathering from all those different aggregations with all their little 
  peculiarities
  - complete the yaml definitions by carefully reading all the 
   [online documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)


### testing

To run the tests call:
```shell script
python test.py
````

To include testing against a live elasticsearch:
```shell script
python test.py --live
```

To change **localhost:9200** to something different
pass any arguments as json:
```shell script
python test.py --live --elasticsearch '{"hosts": [{"host": "127.0.0.5", "port": 1200}], "http_auth": ["user", "password"]}'
```

The live tests will create new indices and immediately destroy them afterwards. 
They are prefixed with **elastipy---unittest-**


### development

There is some housekeeping and glue code for the basics. 
The methods for queries and aggregations as well as the query 
classes are auto-generated from [yaml files](definition). 
They include all parameters, default values and documentation.

The interface python code is rendered via 
```shell script
# in project root
python generate_interfaces.py
``` 
using all the yamls and some rendering code from the [definition/](definition/) directory.

Notebooks that create part of the documentation are executed and converted to .rst files in 
the [docs/](docs/) directory with
```shell script
python run_doc_notebooks.py
``` 

I'm stuck with restructuredtext for the docstrings although besides the `:param:` syntax 
i find it simply repellent. It still has the most supported toolchain it seems.  