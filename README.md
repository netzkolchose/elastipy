## elastipy

A python wrapper to make elasticsearch queries and aggregations more fun.

Actually i'm just learning this stuff and have the following requests:
- some generic convenient data access to nested bucketed aggregations and such
- the IDE/auto-completion should help a bit with all the elasticsearch parameters

Right now it looks like this:
```python
from elastipy import Query

query = Query(index="world").match("topic", "yet-another-api")
languages_per_country = query.agg_terms(field="country").agg_terms(field="language")

response = query.execute()

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

It is not much there yet - and i'm still learning. Though the little wrapper code is already copied from 
one project to another so it shall be captured here and painted with unittests.
  