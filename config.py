class Date:
    DATE_FORMAT_LONG = "%Y-%m-%dT%H:%M:%S.000000Z"
    DATE_FORMAT_SHORT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    TIME_FORMAT_SHORT = "%H:%M"


class KibanaRequest:
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
