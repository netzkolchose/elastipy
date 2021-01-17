don't be plastic, elastipy!
===========================



.. code:: ipython3

    import sys
    sys.path.insert(0, "..")

exporting some objects
----------------------

Without too much thinking we can just use the built-in export helper and
generate some data.

.. code:: ipython3

    from elastipy import Exporter
    
    class ShapeExporter(Exporter):
        INDEX_NAME = "elastipy-example-shapes"
        MAPPINGS = {
            "properties": {
                "shape": {"type": "keyword"},
                "color": {"type": "keyword"},
                "area": {"type": "float"},
            }
        }

The **INDEX\_NAME** is obviously the name of the elasticsearch index.
The **MAPPINGS** parameter describes the `elasticsearch
mapping <https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html>`__.
Here we say that documents will at least have these common fields, one
of type **float** and two of type **keyword** which means they are
strings but not full-text searchable ones. Instead they are efficiently
indexed and aggregatable.

The data we create out of thin air..

.. code:: ipython3

    import random
    
    def shape_generator(count=1000):
        for i in range(count):
            yield {
                "shape": random.choice(("triangle", "square")),
                "color": random.choice(("red", "green", "blue")),
                "area": random.uniform(1, 10),
            }

Now create our exporter and export a couple of documents. It uses the
`bulk helper
tools <https://elasticsearch-py.readthedocs.io/en/7.10.0/helpers.html#bulk-helpers>`__
internally.

.. code:: ipython3

    exporter = ShapeExporter()
    count, errors = exporter.export_list(shape_generator())
    print(count, "exported")


.. parsed-literal::

    1000 exported


query oh elastipyia
-------------------

In most cases this import is enough to access all the good stuff:

.. code:: ipython3

    from elastipy import Search, query

Now get some documents:

.. code:: ipython3

    s = Search(index=ShapeExporter.INDEX_NAME)

**s** is now a search request that can be configured. Setting any search
related options will always return a new instance. Here we set the
maximum number of documents to respond:

.. code:: ipython3

    s = s.size(3)

Next we add a
`query <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`__,
more specifically a `term
query <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html>`__.

.. code:: ipython3

    s = s.term(field="color", value="green")

Our request to elasticsearch would look like this right now:

.. code:: ipython3

    s.dump_body()


.. parsed-literal::

    {
      "query": {
        "term": {
          "color": {
            "value": "green"
          }
        }
      },
      "size": 3
    }


More queries can be added, which defaults to an **AND** combination:

.. code:: ipython3

    s = s.range(field="area", gt=5.)
    s.dump_body()


.. parsed-literal::

    {
      "query": {
        "bool": {
          "must": [
            {
              "term": {
                "color": {
                  "value": "green"
                }
              }
            },
            {
              "range": {
                "area": {
                  "gt": 5.0
                }
              }
            }
          ]
        }
      },
      "size": 3
    }


**OR** combinations can be archived with the
`bool <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html>`__
query itself or by applying the ``|`` operator to the query classes in
``elastipy.query``:

.. code:: ipython3

    s = s | (query.Term(field="color", value="red") & query.Range(field="area", gt=8.))
    s.dump_body()


.. parsed-literal::

    {
      "query": {
        "bool": {
          "should": [
            {
              "bool": {
                "must": [
                  {
                    "term": {
                      "color": {
                        "value": "green"
                      }
                    }
                  },
                  {
                    "range": {
                      "area": {
                        "gt": 5.0
                      }
                    }
                  }
                ]
              }
            },
            {
              "bool": {
                "must": [
                  {
                    "term": {
                      "color": {
                        "value": "red"
                      }
                    }
                  },
                  {
                    "range": {
                      "area": {
                        "gt": 8.0
                      }
                    }
                  }
                ]
              }
            }
          ]
        }
      },
      "size": 3
    }


Better execute the search now before the body get's too complicated:

.. code:: ipython3

    response = s.execute()
    response.dump()


.. parsed-literal::

    {
      "took": 1,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": 249,
        "max_score": 2.1119494,
        "hits": [
          {
            "_index": "elastipy-example-shapes",
            "_type": "_doc",
            "_id": "OX65DXcBeebHNMb6yFT6",
            "_score": 2.1119494,
            "_source": {
              "shape": "triangle",
              "color": "green",
              "area": 8.249469348431154
            }
          },
          {
            "_index": "elastipy-example-shapes",
            "_type": "_doc",
            "_id": "QX65DXcBeebHNMb6yFT6",
            "_score": 2.1119494,
            "_source": {
              "shape": "square",
              "color": "green",
              "area": 8.334699437379598
            }
          },
          {
            "_index": "elastipy-example-shapes",
            "_type": "_doc",
            "_id": "T365DXcBeebHNMb6yFT6",
            "_score": 2.1119494,
            "_source": {
              "shape": "square",
              "color": "green",
              "area": 5.303149599876332
            }
          }
        ]
      }
    }


The response object is a small wrapper around ``dict`` that has some
convenience properties.

.. code:: ipython3

    response.documents




.. parsed-literal::

    [{'shape': 'triangle', 'color': 'green', 'area': 8.249469348431154},
     {'shape': 'square', 'color': 'green', 'area': 8.334699437379598},
     {'shape': 'square', 'color': 'green', 'area': 5.303149599876332}]



The functions and properties are tried to make chainable in a way that
allows for short and powerful oneliners:

.. code:: ipython3

    Search(index=ShapeExporter.INDEX_NAME).size(20).sort("-area").execute().documents




.. parsed-literal::

    [{'shape': 'triangle', 'color': 'red', 'area': 9.979456153451741},
     {'shape': 'square', 'color': 'green', 'area': 9.979385991503124},
     {'shape': 'triangle', 'color': 'green', 'area': 9.976357130797751},
     {'shape': 'square', 'color': 'green', 'area': 9.974790391463257},
     {'shape': 'triangle', 'color': 'blue', 'area': 9.972795370592197},
     {'shape': 'square', 'color': 'green', 'area': 9.95190426930661},
     {'shape': 'triangle', 'color': 'blue', 'area': 9.941861620798456},
     {'shape': 'square', 'color': 'green', 'area': 9.936174506327639},
     {'shape': 'triangle', 'color': 'red', 'area': 9.930792284450627},
     {'shape': 'triangle', 'color': 'blue', 'area': 9.910231588457428},
     {'shape': 'square', 'color': 'green', 'area': 9.892232482088211},
     {'shape': 'triangle', 'color': 'blue', 'area': 9.886895102745454},
     {'shape': 'square', 'color': 'blue', 'area': 9.885680130859289},
     {'shape': 'square', 'color': 'red', 'area': 9.859942003386534},
     {'shape': 'triangle', 'color': 'green', 'area': 9.855287953208633},
     {'shape': 'triangle', 'color': 'green', 'area': 9.849825172877582},
     {'shape': 'square', 'color': 'red', 'area': 9.833959514624274},
     {'shape': 'square', 'color': 'green', 'area': 9.832498529926946},
     {'shape': 'square', 'color': 'red', 'area': 9.82924239305871},
     {'shape': 'square', 'color': 'green', 'area': 9.825434535069801}]



