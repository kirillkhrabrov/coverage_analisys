import uuid

global test_name_snippet
global test_status
global test_step_name
global test_step_status
global param_name
global param_value
global log_file_name
global full_path
global status_code
global http_method
global date


api_parameters = [{
                    "name": "type",
                    "values": ["task", "item", "store", "chart"]
                },{
                    "name": "page_size",
                    "values": [10,20,30,50,100]
                },
{
                    "name": "page",
                    "values": [1,2,3,5,10]
                },
{
                    "name": "ordering",
                    "values": ["created_at, created_from", ]
                }
]

fact_allure_json_no_attach = {
    "name": test_name_snippet,
    "status": test_status,
    "steps": [
        {
            "name": test_step_name,
            "status": test_step_status,
            "parameters": [
                api_parameter
            ]
        }
    ],
    "uuid": uuid.uuid4()
}

fact_allure_json_attach = {
    "name": test_name_snippet,
    "status": test_status,
    "steps": [
        {
            "name": test_step_name,
            "status": test_step_status
        }
    ],
    "attachments": [
        {
            "name": "log",
            "source": log_file_name,
            "type": "text/plain"
        }
    ],
    "uuid": uuid.uuid4()
}


log_json_resp = {
    "rawResponse": {},
    "hits": {
        "hits": [
            {
                "_source": {
                    "full_path": full_path,
                    "status_code": status_code,
                    "event": "REQUEST_SUCCESS",
                    "level": "info",
                    "method": http_method,
                    "time": date
                }
            }
        ]
    }
}






