Search
======

The `Search` class is the main entry for all queries and aggregation
requests against *elasticsearch*.

supported queries
-----------------

.. include:: ./query_index.rst


search interface
----------------

The ``Search`` class combines the ``query`` and the ``aggregation``
interface.


.. autoclass:: elastipy.Search
   :members:
   :inherited-members:
   :show-inheritance:


search parameters
-----------------

.. autoclass:: elastipy.generated_search_param.SearchParameters
   :members:
   :inherited-members:


printing utilities
------------------

.. autoclass:: elastipy.search_dump.SearchDump
   :members:
   :inherited-members:

.. autoclass:: elastipy.response_dump.ResponseDump
   :members:
   :inherited-members:
