# history / changes

## ??? (2022/03)

- support for elasticsearch 8.0.0
- support [highlighting](https://www.elastic.co/guide/en/elasticsearch/reference/current/highlighting.html)

## v0.2.1 (2021/04)

- fix in setup.py 

## v0.2.0 (2021/02)

- clean up test interface and create `test.py`
- add [travis-ci](https://travis-ci.com/github/netzkolchose/elastipy) and 
[read-the-docs](https://elastipy.readthedocs.io/en/latest/).
- move tutorial code to jupyter notebooks and unify quickref in README and in docs
- move all aggregation print helpers to `Aggregation.dump`
- clean up `Aggregation.items` and all those data accessors
- add `Aggregation.to_matrix`
- add interface for all `Search` parameters. This might change though..
- apply rst doc standards to the auto-generated documentation from the yamls
- put pandas plotting interface into `Aggregation.plot`  

## v0.1.0 (2021/01)

- complete rework and renaming of interface
- auto-generated methods and classes
- clean-up of Exporter  
- nice table print

## v0.0.1 (2020/12)

- initial crappy release
