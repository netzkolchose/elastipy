## elastipy

A python wrapper to make elasticsearch queries and aggregations more fun.

Actually i'm just learning this stuff and have the following requests:
- some generic convenient data access to nested bucketed aggregations and such
- the IDE/auto-completion should help a bit with all the elasticsearch parameters

This library is a bit similar to [elasticsearch-dsl](https://github.com/elastic/elasticsearch-dsl-py).
The focus, however, is more on documented and typed python interfaces.

Right now it looks like this:
```python
from elastipy import Search, query

q = Search(index="world")
q = q.term("topic", "yet-another-api") | query.Term("topic", "yet-another-operator-overload")

languages_per_country = q.agg_terms(field="country").agg_terms(field="language")

response = q.execute()

languages_per_country.to_dict()
```
might result in:
```python
{
    ("DE", "Python"): 3197,
    ("DE", "C++"): 1701,
    ("DE", "php"): 52,
    ("ES", "Python"): 5104,
    ("ES", "C++"): 1201,
    ("ES", "php"): 77,
    ...
}
```

It is *not much* there yet - and i'm still learning. Though the little wrapper code is already copied from 
one project to another so it shall be captured here and painted with unittests.

The big steps to success are right now:
  - make sure that all the combinations of queries work as expected
  - wrap the query [online documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
into the [definition.py](definition/query/definition.py) file so all required classes get generated 
  