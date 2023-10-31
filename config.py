class KibanaRequest:
    """
        Class for storing Kibana request params
    """
    KIBANA_AUTH_URL = "{KIBANA_AUTH_URL}"
    KIBANA_REQ_URL = "{KIBANA_REQ_URL}"
    AUTH_REQUEST_PAYLOAD = "{AUTH_REQUEST_PAYLOAD}"

    REQUEST_PAYLOAD = {
        "params": {
            "index": "{index}",
            "body": {
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [],
                        "should": [],
                        "must_not": []
                    }
                },
                "size": "{result_size}"
            }
        }
    }

    REQUEST_HEADERS = {
        'kbn-xsrf': 'anything',
        'Content-Type': 'application/json'
    }
