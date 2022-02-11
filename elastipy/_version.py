from elasticsearch import VERSION as ES_VERSION

version = (0, 2, 1)

version_str = "%s.%s.%s" % version


if ES_VERSION[0] not in (7, 8):
    raise ValueError(
        f"Unsupported elasticsearch-py major version {ES_VERSION}"
        f", expecting 7 or 8"
    )
