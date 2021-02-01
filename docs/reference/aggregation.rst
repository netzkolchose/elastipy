Aggregation
===========

Aggregations can be created on the ``Search`` object or inside
an existing ``Aggregation``.


supported aggregations
----------------------

.. include:: ./agg_index.rst


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
