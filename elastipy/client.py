
def get_elastic_client(timeout=30):
    from elasticsearch import Elasticsearch, Transport, Connection

    url = "localhost"
    port = 9200

    params = dict(
        hosts=[{'host': url, 'port': port}],
        scheme="http",
        timeout=timeout,
    )

    return Elasticsearch(**params)
