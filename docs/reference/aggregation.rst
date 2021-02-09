Aggregation
===========

Aggregations can be created on the :link:`Search` object or inside
an existing :link:`Aggregation`.

.. CODE::

    from elastipy import Search

    s = Search()
    agg = s.agg_terms("name_of_agg", field="field", size=100)


supported aggregations
----------------------

.. include:: ./agg_index.rst


value access
------------

.. automethod:: elastipy.aggregation.Aggregation.keys
    :noindex:

.. automethod:: elastipy.aggregation.Aggregation.values
    :noindex:

.. automethod:: elastipy.aggregation.Aggregation.items
    :noindex:


.. automethod:: elastipy.aggregation.Aggregation.rows
    :noindex:

.. automethod:: elastipy.aggregation.Aggregation.dict_rows
    :noindex:

.. automethod:: elastipy.aggregation.Aggregation.to_dict
    :noindex:

.. automethod:: elastipy.aggregation.Aggregation.to_pandas
    :noindex:

.. automethod:: elastipy.aggregation.Aggregation.to_matrix
    :noindex:


aggregation interface
---------------------

The ``Search`` class as well as created aggregations themselves support the
following interface.


.. autoclass:: elastipy.aggregation.Aggregation
   :members:
   :inherited-members:
   :show-inheritance:


printing utilities
------------------

.. autoclass:: elastipy.aggregation.aggregation_dump.AggregationDump
   :members:
   :inherited-members:
   :show-inheritance:


plotting
--------

.. autoclass:: elastipy.plot.aggregation_plot_pd.PandasPlotWrapper
   :members:
   :inherited-members:
   :show-inheritance:
