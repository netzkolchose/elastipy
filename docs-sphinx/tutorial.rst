don't be plastic, elastipy!
===========================

Hi there, this tutorial is actually a `jupyter
notebook <https://jupyter.org/>`__ and can be found in
`examples <https://github.com/defgsus/elastipy/blob/development/examples/>`__/`tutorial.ipynb <https://github.com/defgsus/elastipy/blob/development/examples/tutorial.ipynb>`__

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
                "area": random.gauss(5, 1.3),
            }

Now create our exporter and export a couple of documents. It uses the
`bulk helper
tools <https://elasticsearch-py.readthedocs.io/en/7.10.0/helpers.html#bulk-helpers>`__
internally.

.. code:: ipython3

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

.. code:: ipython3

    from elastipy import Search, query

Now get some documents:

.. code:: ipython3

    s = Search(index="elastipy-example-shapes")

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
      "took": 2,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": 169,
        "max_score": 2.1326516,
        "hits": [
          {
            "_index": "elastipy-example-shapes",
            "_type": "_doc",
            "_id": "bn6sEHcBeebHNMb6Xmm8",
            "_score": 2.1326516,
            "_source": {
              "shape": "triangle",
              "color": "green",
              "area": 5.180598032177817
            }
          },
          {
            "_index": "elastipy-example-shapes",
            "_type": "_doc",
            "_id": "dX6sEHcBeebHNMb6Xmm8",
            "_score": 2.1326516,
            "_source": {
              "shape": "square",
              "color": "green",
              "area": 6.576369444794877
            }
          },
          {
            "_index": "elastipy-example-shapes",
            "_type": "_doc",
            "_id": "eX6sEHcBeebHNMb6Xmm8",
            "_score": 2.1326516,
            "_source": {
              "shape": "square",
              "color": "green",
              "area": 5.847317033356114
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

    [{'shape': 'triangle', 'color': 'green', 'area': 5.180598032177817},
     {'shape': 'square', 'color': 'green', 'area': 6.576369444794877},
     {'shape': 'square', 'color': 'green', 'area': 5.847317033356114}]



How many documents are there at all?

.. code:: ipython3

    Search(index="elastipy-example-shapes").execute().total_hits




.. parsed-literal::

    1000



--------------

The functions and properties are tried to make chainable in a way that
allows for short and powerful oneliners:

.. code:: ipython3

    Search(index="elastipy-example-shapes") \
        .size(20).sort("-area").execute().documents




.. parsed-literal::

    [{'shape': 'square', 'color': 'green', 'area': 8.79258550844049},
     {'shape': 'triangle', 'color': 'red', 'area': 8.661123759002336},
     {'shape': 'triangle', 'color': 'red', 'area': 8.565988754996523},
     {'shape': 'triangle', 'color': 'green', 'area': 8.563406508267303},
     {'shape': 'square', 'color': 'green', 'area': 8.490012394710579},
     {'shape': 'triangle', 'color': 'green', 'area': 8.291300656432396},
     {'shape': 'square', 'color': 'blue', 'area': 8.161546976474865},
     {'shape': 'square', 'color': 'blue', 'area': 8.05068744399311},
     {'shape': 'square', 'color': 'red', 'area': 7.938184774736011},
     {'shape': 'triangle', 'color': 'blue', 'area': 7.904676048185968},
     {'shape': 'square', 'color': 'blue', 'area': 7.885336389376041},
     {'shape': 'triangle', 'color': 'green', 'area': 7.875354412237241},
     {'shape': 'triangle', 'color': 'red', 'area': 7.807859334703004},
     {'shape': 'square', 'color': 'blue', 'area': 7.714386155264371},
     {'shape': 'triangle', 'color': 'red', 'area': 7.678549348901566},
     {'shape': 'triangle', 'color': 'red', 'area': 7.66467000510316},
     {'shape': 'square', 'color': 'red', 'area': 7.599298161531182},
     {'shape': 'square', 'color': 'green', 'area': 7.593707210512935},
     {'shape': 'triangle', 'color': 'blue', 'area': 7.581204457454557},
     {'shape': 'triangle', 'color': 'red', 'area': 7.544684677002033}]



So this was the document response. Let's dive inside and start
aggregating on fields.

agitated aggregation
--------------------

Aggregations can be created using the ``agg_``, ``metric_`` and
``pipeline_`` prefixes. An aggregation is **attached** to the ``Search``
instance, so there is no copying like with the queries above.

.. code:: ipython3

    s = Search(index="elastipy-example-shapes").size(0)
    
    agg = s.agg_terms(field="shape")
    
    s.dump_body()


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


As we can see, a `terms
aggregation <https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html>`__
has been added to the search body. The names of aggregations are
auto-generated, but can be explicitly stated:

.. code:: ipython3

    s = Search(index="elastipy-example-shapes").size(0)
    
    agg = s.agg_terms("shapes", field="shape")
    
    s.dump_body()


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


Let's look at the result from elasticsearch:

.. code:: ipython3

    s.execute()
    s.dump_response()


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
              "doc_count": 517
            },
            {
              "key": "triangle",
              "doc_count": 483
            }
          ]
        }
      }
    }


valuable access
~~~~~~~~~~~~~~~

Because we kept the ``agg`` variable, we can use it's interface to
access the values more conveniently:

.. code:: ipython3

    agg.to_dict()




.. parsed-literal::

    {'square': 517, 'triangle': 483}



It supports the ``items()``, ``keys()`` and ``values()`` generators as
known from the ``dict`` type:

.. code:: ipython3

    for key, value in agg.items():
        print(f"{key:12} {value}")


.. parsed-literal::

    square       517
    triangle     483


It also has a ``dict_rows()`` generator which preseves the **names** and
**keys** of the aggregation:

.. code:: ipython3

    for row in agg.dict_rows():
        print(row)


.. parsed-literal::

    {'shapes': 'square', 'shapes.doc_count': 517}
    {'shapes': 'triangle', 'shapes.doc_count': 483}


The ``rows()`` generator flattens the ``dict_rows()`` into a CSV-style
list:

.. code:: ipython3

    for row in agg.rows():
        print(row)


.. parsed-literal::

    ['shapes', 'shapes.doc_count']
    ['square', 517]
    ['triangle', 483]


And we can print a nice table to the command-line:

.. code:: ipython3

    agg.print.table()


.. parsed-literal::

    shapes   │ shapes.doc_count                           
    ─────────┼────────────────────────────────────────────
    square   │ 517 [1;34m███████████████████████████████████████[0m
    triangle │ 483 [1;34m████████████████████████████████████▌  [0m


Obviously, at this point a couple of users would not understand why
there is no conversion to a `pandas
DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`__
built in:

.. code:: ipython3

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
          <td>517</td>
        </tr>
        <tr>
          <th>triangle</th>
          <td>483</td>
        </tr>
      </tbody>
    </table>
    </div>



The **index** and **columns** are assigned automatically. Also columns
containing ISO-formatted date strings will be converted to
``pandas.Timestamp``.

With ``matplotlib`` installed we can access the `pandas plotting
interface <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html>`__:

.. code:: ipython3

    agg.df().plot.bar()




.. parsed-literal::

    <AxesSubplot:xlabel='shapes'>




.. image:: tutorial_files/tutorial_56_1.png


Now let's look into the details when **metrics** or nested **bucket**
aggregations are involved.

deeper aggregation agitation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    agg = Search(index="elastipy-example-shapes") \
        .agg_terms("shapes", field="shape") \
        .agg_terms("colors", field="color") \
        .metric_sum("area", field="area") \
        .metric_avg("avg-area", field="area") \
        .execute()

A few notes: - ``agg_`` methods always return the newly created
aggregation, so the ``colors`` aggregation is nested inside the
``shapes`` aggregation. - ``metric_`` methods return their parent
aggregation (because metrics do not allow a nested aggregation), so we
can just continue to call ``metric_*`` and each time we add a metric to
the ``colors`` aggregation. If you need to get access to the metric
object itself add the ``return_self=True`` parameter. - The ``execute``
method on an aggregation does not return the response but the
aggregation itself.

Now, what does the ``to_dict`` output look like?

.. code:: ipython3

    agg.to_dict()




.. parsed-literal::

    {('square', 'red'): 192,
     ('square', 'blue'): 169,
     ('square', 'green'): 156,
     ('triangle', 'green'): 166,
     ('triangle', 'blue'): 159,
     ('triangle', 'red'): 158}



It has put the **keys** that lead to each value into tuples. Without a
lot of thinking we can say:

.. code:: ipython3

    data = agg.to_dict()
    print(f"There are {data[('triangle', 'red')]} red triangles in the database!")


.. parsed-literal::

    There are 158 red triangles in the database!


But where are the metrics gone?

Generally, ``keys()``, ``values()``, ``items()``, ``to_dict()`` and
``to_matrix()`` only access the values of the **current aggregation**
(which is ``colors`` in the example). Although all the keys of the
parent **bucket** aggregations that lead to the values are included.

The methods ``dict_rows()``, ``rows()``, ``to_pandas()`` and
``print.table()`` will access **all values** from the whole aggregation
branch. In this example the branch looks like this:

-  shapes
-  colors

   -  area
   -  avg-area

.. code:: ipython3

    agg.print.table(digits=3)


.. parsed-literal::

    shapes   │ shapes.doc_count    │ colors │ colors.doc_count    │ area                    │ avg-area            
    ─────────┼─────────────────────┼────────┼─────────────────────┼─────────────────────────┼─────────────────────
    square   │ 517 [1;34m███████████████[0m │ red    │ 192 [1;34m███████████████[0m │ 963.596 [1;34m███████████████[0m │ 5.019 [1;34m█████████████▊[0m
    square   │ 517 [1;34m███████████████[0m │ blue   │ 169 [1;34m█████████████▍ [0m │ 844.461 [1;34m█████████████▎ [0m │ 4.997 [1;34m█████████████▊[0m
    square   │ 517 [1;34m███████████████[0m │ green  │ 156 [1;34m████████████▍  [0m │ 782.863 [1;34m████████████▍  [0m │ 5.018 [1;34m█████████████▊[0m
    triangle │ 483 [1;34m██████████████ [0m │ green  │ 166 [1;34m█████████████  [0m │ 825.114 [1;34m████████████▉  [0m │ 4.971 [1;34m█████████████▋[0m
    triangle │ 483 [1;34m██████████████ [0m │ blue   │ 159 [1;34m████████████▋  [0m │ 777.241 [1;34m████████████▎  [0m │ 4.888 [1;34m█████████████▌[0m
    triangle │ 483 [1;34m██████████████ [0m │ red    │ 158 [1;34m████████████▌  [0m │  805.36 [1;34m████████████▋  [0m │ 5.097 [1;34m██████████████[0m


Now all information is in the table. Note that the ``shapes.doc_count``
column contains the same value multiple times. This is because each
``colors`` aggregation bucket splits the ``shapes`` bucket into multiple
results, without changing the overall count of the shapes, of course.

Now what is this method with the awesome name ``to_matrix``?

.. code:: ipython3

    names, keys, matrix = agg.to_matrix()
    print("names ", names)
    print("keys  ", keys)
    print("matrix", matrix)


.. parsed-literal::

    names  ['shapes', 'colors']
    keys   [['square', 'triangle'], ['red', 'blue', 'green']]
    matrix [[192, 169, 156], [158, 159, 166]]


It produces a heatmap! At least in two dimensions. In this example we
have two dimensions from the **bucket** aggregations ``shapes`` and
``colors``. ``to_matrix()`` will produce a matrix with any number of
dimensions, but if it's one or two, we can also convert it to a
``DataFrame``:

.. code:: ipython3

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
          <th>red</th>
          <th>blue</th>
          <th>green</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>square</th>
          <td>192</td>
          <td>169</td>
          <td>156</td>
        </tr>
        <tr>
          <th>triangle</th>
          <td>158</td>
          <td>159</td>
          <td>166</td>
        </tr>
      </tbody>
    </table>
    </div>



And having something like `seaborn <https://seaborn.pydata.org/>`__
installed we can easily plot it:

.. code:: ipython3

    import seaborn as sns
    
    sns.heatmap(agg.df_matrix())




.. parsed-literal::

    <AxesSubplot:>




.. image:: tutorial_files/tutorial_72_1.png


