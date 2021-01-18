don't be plastic, elastipy!
===========================

Hi there, this tutorial is actually a `jupyter
notebook <https://jupyter.org/>`__ and can be found in
`examples <https://github.com/defgsus/elastipy/blob/development/examples/>`__/`tutorial.ipynb <https://github.com/defgsus/elastipy/blob/development/examples/tutorial.ipynb>`__

exporting some objects
----------------------

Without too much thinking we can just use the built-in export helper and
generate some data.

.. code:: python3

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

.. code:: python3

    import random
    
    def shape_generator(count=1000, seed=23):
        rnd = random.Random(seed)
        for i in range(count):
            yield {
                "shape": rnd.choice(("triangle", "square")),
                "color": rnd.choice(("red", "green", "blue")),
                "area": rnd.gauss(5, 1.3),
            }

Now create our exporter and export a couple of documents. It uses the
`bulk helper
tools <https://elasticsearch-py.readthedocs.io/en/7.10.0/helpers.html#bulk-helpers>`__
internally.

.. code:: python3

    exporter = ShapeExporter()
    
    count, errors = exporter.export_list(shape_generator(), refresh=True)
    
    print(count, "exported")


.. parsed-literal::

    1000 exported


The ``refresh=True`` parameter will refresh the index as soon as
everything is exported, so we do not have to wait for objects to appear
in the elasticsearch index.

query oh elastipyia
-------------------

In most cases this import is enough to access all the good stuff:

.. code:: python3

    from elastipy import Search, query

Now get some documents:

.. code:: python3

    s = Search(index="elastipy-example-shapes")

**s** is now a search request that can be configured. Setting any search
related options will always return a new instance. Here we set the
maximum number of documents to respond:

.. code:: python3

    s = s.size(3)

Next we add a
`query <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`__,
more specifically a `term
query <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html>`__.

.. code:: python3

    s = s.term(field="color", value="green")

Our request to elasticsearch would look like this right now:

.. code:: python3

    s.dump.body()


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




.. parsed-literal::

    <elastipy.search_print.SearchPrintWrapper at 0x7f96147c5c18>



More queries can be added, which defaults to an **AND** combination:

.. code:: python3

    s = s.range(field="area", gt=5.)
    s.dump.body()


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




.. parsed-literal::

    <elastipy.search_print.SearchPrintWrapper at 0x7f9594661358>



**OR** combinations can be archived with the
`bool <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html>`__
query itself or by applying the ``|`` operator to the query classes in
``elastipy.query``:

.. code:: python3

    s = s | (query.Term(field="color", value="red") & query.Range(field="area", gt=8.))
    s.dump.body()


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




.. parsed-literal::

    <elastipy.search_print.SearchPrintWrapper at 0x7f9594661940>



Better execute the search now before the body get's too complicated:

.. code:: python3

    response = s.execute()
    response.dump()


.. parsed-literal::

    {
      "took": 0,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": 166,
        "max_score": 2.1203249,
        "hits": [
          {
            "_index": "elastipy-example-shapes",
            "_type": "_doc",
            "_id": "Cn7oEncBeebHNMb6vbRf",
            "_score": 2.1203249,
            "_source": {
              "shape": "square",
              "color": "green",
              "area": 7.263731074718455
            }
          },
          {
            "_index": "elastipy-example-shapes",
            "_type": "_doc",
            "_id": "F37oEncBeebHNMb6vbRf",
            "_score": 2.1203249,
            "_source": {
              "shape": "triangle",
              "color": "green",
              "area": 6.012755425383653
            }
          },
          {
            "_index": "elastipy-example-shapes",
            "_type": "_doc",
            "_id": "Gn7oEncBeebHNMb6vbRf",
            "_score": 2.1203249,
            "_source": {
              "shape": "square",
              "color": "green",
              "area": 5.783465577671204
            }
          }
        ]
      }
    }


The response object is a small wrapper around ``dict`` that has some
convenience properties.

.. code:: python3

    response.documents




.. parsed-literal::

    [{'shape': 'square', 'color': 'green', 'area': 7.263731074718455},
     {'shape': 'triangle', 'color': 'green', 'area': 6.012755425383653},
     {'shape': 'square', 'color': 'green', 'area': 5.783465577671204}]



How many documents are there at all?

.. code:: python3

    Search(index="elastipy-example-shapes").execute().total_hits




.. parsed-literal::

    1000



--------------

The functions and properties are tried to make chainable in a way that
allows for short and powerful oneliners:

.. code:: python3

    Search(index="elastipy-example-shapes") \
        .size(20).sort("-area").execute().documents




.. parsed-literal::

    [{'shape': 'triangle', 'color': 'blue', 'area': 10.429612563121568},
     {'shape': 'triangle', 'color': 'blue', 'area': 8.631278664614928},
     {'shape': 'triangle', 'color': 'green', 'area': 8.383293158814908},
     {'shape': 'square', 'color': 'red', 'area': 8.236889913615816},
     {'shape': 'triangle', 'color': 'red', 'area': 8.157738475146177},
     {'shape': 'triangle', 'color': 'blue', 'area': 8.149289701139908},
     {'shape': 'triangle', 'color': 'red', 'area': 8.1241500335766},
     {'shape': 'square', 'color': 'green', 'area': 8.09185625330105},
     {'shape': 'triangle', 'color': 'blue', 'area': 8.08735770969464},
     {'shape': 'square', 'color': 'green', 'area': 7.977278235020664},
     {'shape': 'triangle', 'color': 'red', 'area': 7.938468252124386},
     {'shape': 'triangle', 'color': 'red', 'area': 7.886810892882312},
     {'shape': 'square', 'color': 'red', 'area': 7.884563035795223},
     {'shape': 'square', 'color': 'blue', 'area': 7.87039265833457},
     {'shape': 'triangle', 'color': 'red', 'area': 7.8174214918916025},
     {'shape': 'triangle', 'color': 'red', 'area': 7.707584538303967},
     {'shape': 'square', 'color': 'red', 'area': 7.704892192610947},
     {'shape': 'triangle', 'color': 'green', 'area': 7.641915136804204},
     {'shape': 'triangle', 'color': 'blue', 'area': 7.592409852960503},
     {'shape': 'square', 'color': 'red', 'area': 7.542068017226418}]



So this was the document response. Let's dive inside and start
aggregating on fields.

agitated aggregation
--------------------

Aggregations can be created using the ``agg_``, ``metric_`` and
``pipeline_`` prefixes. An aggregation is **attached** to the ``Search``
instance, so there is no copying like with the queries above.

.. code:: python3

    s = Search(index="elastipy-example-shapes").size(0)
    
    agg = s.agg_terms(field="shape")
    
    s.dump.body()


.. parsed-literal::

    {
      "aggregations": {
        "a0": {
          "terms": {
            "field": "shape"
          }
        }
      },
      "query": {
        "match_all": {}
      },
      "size": 0
    }




.. parsed-literal::

    <elastipy.search_print.SearchPrintWrapper at 0x7f95943ae860>



As we can see, a `terms
aggregation <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html>`__
has been added to the search body. The names of aggregations are
auto-generated, but can be explicitly stated:

.. code:: python3

    s = Search(index="elastipy-example-shapes").size(0)
    
    agg = s.agg_terms("shapes", field="shape")
    
    s.dump.body()


.. parsed-literal::

    {
      "aggregations": {
        "shapes": {
          "terms": {
            "field": "shape"
          }
        }
      },
      "query": {
        "match_all": {}
      },
      "size": 0
    }




.. parsed-literal::

    <elastipy.search_print.SearchPrintWrapper at 0x7f95943ae9e8>



Let's look at the result from elasticsearch:

.. code:: python3

    s.execute()
    s.dump.response()


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
        "total": 1000,
        "max_score": null,
        "hits": []
      },
      "aggregations": {
        "shapes": {
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": [
            {
              "key": "square",
              "doc_count": 500
            },
            {
              "key": "triangle",
              "doc_count": 500
            }
          ]
        }
      }
    }




.. parsed-literal::

    <elastipy.search_print.SearchPrintWrapper at 0x7f95943ae438>



valuable access
~~~~~~~~~~~~~~~

Because we kept the ``agg`` variable, we can use it's interface to
access the values more conveniently:

.. code:: python3

    agg.to_dict()




.. parsed-literal::

    {'square': 500, 'triangle': 500}



It supports the ``items()``, ``keys()`` and ``values()`` generators as
known from the ``dict`` type:

.. code:: python3

    for key, value in agg.items():
        print(f"{key:12} {value}")


.. parsed-literal::

    square       500
    triangle     500


It also has a ``dict_rows()`` generator which preserves the **names**
and **keys** of the aggregation:

.. code:: python3

    for row in agg.dict_rows():
        print(row)


.. parsed-literal::

    {'shapes': 'square', 'shapes.doc_count': 500}
    {'shapes': 'triangle', 'shapes.doc_count': 500}


The ``rows()`` generator flattens the ``dict_rows()`` into a CSV-style
list:

.. code:: python3

    for row in agg.rows():
        print(row)


.. parsed-literal::

    ['shapes', 'shapes.doc_count']
    ['square', 500]
    ['triangle', 500]


And we can print a nice table to the command-line:

.. code:: python3

    agg.dump.table(colors=False)


.. parsed-literal::

    shapes   │ shapes.doc_count
    ─────────┼─────────────────
    square   │ 500             
    triangle │ 500             




.. parsed-literal::

    <elastipy.aggregation.print_wrapper.PrintWrapper at 0x7f96147c5c18>



(The ``colors=False`` parameter disables console colors because they do
not work in this documentation)

--------------

Obviously, at this point a couple of users would not understand why
there is no conversion to a `pandas
DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`__
built in:

.. code:: python3

    agg.to_pandas()  # or simply agg.df()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>shapes.doc_count</th>
        </tr>
        <tr>
          <th>shapes</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>square</th>
          <td>500</td>
        </tr>
        <tr>
          <th>triangle</th>
          <td>500</td>
        </tr>
      </tbody>
    </table>
    </div>



The **index** and **columns** are assigned automatically. Also columns
containing ISO-formatted date strings will be converted to
``pandas.Timestamp``.

With ``matplotlib`` installed we can access the `pandas plotting
interface <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html>`__:

.. code:: python3

    agg.df().plot.bar()




.. parsed-literal::

    <AxesSubplot:xlabel='shapes'>




.. image:: tutorial_files/tutorial_57_1.png


Now let's look into the details when **metrics** or nested **bucket**
aggregations are involved.

deeper aggregation agitation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python3

    agg = Search(index="elastipy-example-shapes") \
        .agg_terms("shapes", field="shape") \
        .agg_terms("colors", field="color") \
        .metric_sum("area", field="area") \
        .metric_avg("avg-area", field="area") \
        .execute()

A few notes:

-  ``agg_`` methods always return the newly created aggregation, so the
   ``colors`` aggregation is nested inside the ``shapes`` aggregation.
-  ``metric_`` methods return their parent aggregation (because metrics
   do not allow a nested aggregation), so we can just continue to call
   ``metric_*`` and each time we add a metric to the ``colors``
   aggregation. If you need to get access to the metric object itself
   add the ``return_self=True`` parameter.
-  The ``execute`` method on an aggregation does not return the response
   but the aggregation itself.

Now, what does the ``to_dict`` output look like?

.. code:: python3

    agg.to_dict()




.. parsed-literal::

    {('square', 'green'): 180,
     ('square', 'red'): 168,
     ('square', 'blue'): 152,
     ('triangle', 'red'): 185,
     ('triangle', 'blue'): 169,
     ('triangle', 'green'): 146}



It has put the **keys** that lead to each value into tuples. Without a
lot of thinking we can say:

.. code:: python3

    data = agg.to_dict()
    print(f"There are {data[('triangle', 'red')]} red triangles in the database!")


.. parsed-literal::

    There are 185 red triangles in the database!


But where are the metrics gone?

Generally, ``keys()``, ``values()``, ``items()``, ``to_dict()`` and
``to_matrix()`` only access the values of the **current aggregation**
(which is ``colors`` in the example). Although all the keys of the
parent **bucket** aggregations that lead to the values are included.

The methods ``dict_rows()``, ``rows()``, ``to_pandas()`` and
``.dump.table()`` will access **all values** from the whole aggregation
branch. In this example the branch looks like this:

-  shapes
-  colors

   -  area
   -  avg-area

.. code:: python3

    agg.dump.table(digits=3, colors=False)


.. parsed-literal::

    shapes   │ shapes.doc_count │ colors │ colors.doc_count     │ area                    │ avg-area              
    ─────────┼──────────────────┼────────┼──────────────────────┼─────────────────────────┼───────────────────────
    square   │ 500              │ green  │ 180 ███████████████▋ │ 893.291 ██████████████▌ │ 4.963 ███████████████▋
    square   │ 500              │ red    │ 168 ██████████████▋  │ 801.394 █████████████   │  4.77 ███████████████ 
    square   │ 500              │ blue   │ 152 █████████████▍   │ 763.321 ████████████▌   │ 5.022 ███████████████▊
    triangle │ 500              │ red    │ 185 ████████████████ │  925.21 ███████████████ │ 5.001 ███████████████▊
    triangle │ 500              │ blue   │ 169 ██████████████▋  │ 861.256 ██████████████  │ 5.096 ████████████████
    triangle │ 500              │ green  │ 146 ████████████▊    │ 738.947 ████████████▎   │ 5.061 ███████████████▉




.. parsed-literal::

    <elastipy.aggregation.print_wrapper.PrintWrapper at 0x7f9589728208>



Now all information is in the table. Note that the ``shapes.doc_count``
column contains the same value multiple times. This is because each
``colors`` aggregation bucket splits the ``shapes`` bucket into multiple
results, without changing the overall count of the shapes, of course.

Now what is this method with the awesome name ``to_matrix``?

.. code:: python3

    names, keys, matrix = agg.to_matrix()
    print("names ", names)
    print("keys  ", keys)
    print("matrix", matrix)


.. parsed-literal::

    names  ['shapes', 'colors']
    keys   [['square', 'triangle'], ['green', 'red', 'blue']]
    matrix [[180, 168, 152], [146, 185, 169]]


It produces a heatmap! At least in two dimensions. In this example we
have two dimensions from the **bucket** aggregations ``shapes`` and
``colors``. ``to_matrix()`` will produce a matrix with any number of
dimensions, but if it's one or two, we can also convert it to a
``DataFrame``:

.. code:: python3

    agg.df_matrix()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>green</th>
          <th>red</th>
          <th>blue</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>square</th>
          <td>180</td>
          <td>168</td>
          <td>152</td>
        </tr>
        <tr>
          <th>triangle</th>
          <td>146</td>
          <td>185</td>
          <td>169</td>
        </tr>
      </tbody>
    </table>
    </div>



And having something like `seaborn <https://seaborn.pydata.org/>`__
installed we can easily plot it:

.. code:: python3

    import seaborn as sns
    
    sns.heatmap(agg.df_matrix())




.. parsed-literal::

    <AxesSubplot:>




.. image:: tutorial_files/tutorial_73_1.png


