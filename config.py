class URLs:
    # адреса стендов
    TEST = 'https://mrmtsx-test.x5.ru/'
    PREPROD = 'https://mrmtsx-preprod.x5.ru/'


class Date:
    DATE_FORMAT_LONG = "%Y-%m-%dT%H:%M:%S.000000Z"
    DATE_FORMAT_SHORT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    TIME_FORMAT_SHORT = "%H:%M"


class KibanaRequest:
    KIBANA_AUTH_URL = "https://sre-logs.x5.ru/auth/login"

    KIBANA_REQ_URL = "https://sre-logs.x5.ru/internal/search/es"

    AUTH_REQUEST_PAYLOAD = 'eyJ1c2VybmFtZSI6ICJraXJpbGwua2hyYWJyb3YiLCJwYXNzd29yZCI6ICI2YXB7cXU1NCJ9'

    REQUEST_PAYLOAD = {
        "params": {
            "index": "project_mrmtsx_prod-idx-2*",
            "body": {
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_phrase": {
                                    "event": "REQUEST_SUCCESS"
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": (datetime.today() - timedelta(days=7)).strftime(Date.DATE_FORMAT_LONG),
                                        "lte": datetime.today().strftime(Date.DATE_FORMAT_LONG),
                                        "format": "strict_date_optional_time"
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": [
                            {
                                "match_phrase": {
                                    "path_template": "health/"
                                }
                            },
                            {
                                "match_phrase": {
                                    "path_template": "/metrics"
                                }
                            },
                            {
                                "match_phrase": {
                                    "path_template": "/admin"
                                }
                            },
                            {
                                "match_phrase": {
                                    "path_template": "/biosmart"
                                }
                            }
                        ]
                    }
                },
                "size": 10000
            }
        }
    }

    REQUEST_HEADERS = {
        'kbn-xsrf': 'anything',
        'Content-Type': 'application/json'
    }