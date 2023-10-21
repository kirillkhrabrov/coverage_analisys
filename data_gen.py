import uuid
import json
from datetime import datetime, timedelta
from random import randint, choice
import os

test_status = ["passed", "passed", "passed", "passed", "passed", "failed", "skipped", "broken", "passed", "passed",
               "passed", "passed", "passed", ]
Date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

file = open('fake_api.json')
fake_api_file = json.load(file)

fake_api = []

for obj in fake_api_file:
    if obj not in fake_api:
        fake_api.append(obj)


def choose_test_status():
    return choice(["passed"] * 75 + ["failed"] * 5 + ["skipped"] + ["broken"])


def choose_code(api_method):
    if api_method["method"] == "GET" or 'login' in api_method["url"]:
        return choice([200] * 150 + [500])
    elif api_method["method"] == "POST" and 'login' not in api_method["url"]:
        return choice([201] * 70 + [400])
    elif api_method["method"] == "DELETE":
        return choice([204] * 70 + [400] + [500])
    elif api_method["method"] == "PATCH":
        return choice([204] * 70 + [400])


def form_step_fact_result_json(num_of_iters):
    for i in range(num_of_iters):
        with open(f'{os.path.join(os.getcwd(), "data/fact_data/")}{uuid.uuid4()}_step_fact_result.json',
                  'w') as res_file:
            fact_allure_json_no_attach = {
                "name": f'Test case ID {str(uuid.uuid4())[-8:]}',
                "status": None,
                "steps": [],
                "uuid": str(uuid.uuid4())
            }

            test_statuses = []

            for j in range(randint(1, 15)):
                chosen_api_method = choice(fake_api[:500])
                status = choose_test_status()
                test_statuses.append(status)
                step = {
                    "name": f'Call API method {chosen_api_method["method"]} {chosen_api_method["url"]}',
                    "status": status,
                    "steps": [
                        {
                            "name": f'Check status code {choose_code(chosen_api_method)}',
                            "status": status
                        }
                    ]
                }

                fact_allure_json_no_attach["steps"].append(step)

            if "failed" in test_statuses:
                fact_allure_json_no_attach["status"] = "failed"
            elif "skipped" in test_statuses:
                fact_allure_json_no_attach["status"] = "skipped"
            elif "broken" in test_statuses:
                fact_allure_json_no_attach["status"] = "broken"
            else:
                fact_allure_json_no_attach["status"] = "passed"

            res_file.write(str(fact_allure_json_no_attach))


def form_log_fact_result_json(num_of_iters):
    for i in range(num_of_iters):
        with open(f'{os.path.join(os.getcwd(), "data/fact_data/")}{uuid.uuid4()}_log_fact_result.json',
                  'w') as res_file:
            fact_allure_json_with_attach = {
                "name": f'Test case ID {str(uuid.uuid4())[-8:]}',
                "status": None,
                "steps": [],
                "attachments": [],
                "uuid": str(uuid.uuid4())
            }
            log_file_name = f'{uuid.uuid4()}_attachment.txt'
            test_statuses = []
            attachment = {
                "name": "log",
                "source": log_file_name,
                "type": "text/plain"
            }
            fact_allure_json_with_attach["attachments"].append(attachment)
            log_attachment_string = ''
            time = (datetime.now() - timedelta(days=randint(0, 7))).strftime(Date_format)

            for j in range(randint(1, 12)):
                chosen_api_method = choice(fake_api[:100])
                status = choose_test_status()
                test_statuses.append(status)
                status_code = choose_code(chosen_api_method)

                step = {
                    "name": f'Call API method {chosen_api_method["method"]} {chosen_api_method["url"]}',
                    "status": status,
                    "steps": [
                        {
                            "name": f'Check status code {status_code}',
                            "status": status
                        }
                    ]
                }

                fact_allure_json_with_attach["steps"].append(step)
                log_attachment_string += f'{str(time)}:[INFO] {chosen_api_method["method"]} {chosen_api_method["url"]} Response status code: {status_code} \n'
                time = (datetime.now() + timedelta(seconds=1, microseconds=randint(10000, 90000))).strftime(
                    Date_format)

            if "failed" in test_statuses:
                fact_allure_json_with_attach["status"] = "failed"
            elif "skipped" in test_statuses:
                fact_allure_json_with_attach["status"] = "skipped"
            elif "broken" in test_statuses:
                fact_allure_json_with_attach["status"] = "broken"
            else:
                fact_allure_json_with_attach["status"] = "passed"

            with open(f'{os.path.join(os.getcwd(), "data/fact_data/")}{log_file_name}', 'w') as attach_file:
                attach_file.write(log_attachment_string)

            res_file.write(str(fact_allure_json_with_attach))


def form_expected_log_json(num_of_iters):
    for i in range(num_of_iters):
        with open(f'{os.path.join(os.getcwd(), "data/expected_data/")}{uuid.uuid4()}_expected_log.json',
                  'w') as log_file:
            log_json_resp = {
                "rawResponse": {},
                "hits": {
                    "hits": []
                }
            }
            for j in range(100):
                chosen_api_method = choice(fake_api[:100])

                hit = {
                    "_source": {
                        "full_path": chosen_api_method["url"],
                        "status_code": choose_code(chosen_api_method),
                        "event": "REQUEST_SUCCESS",
                        "level": "info",
                        "method": chosen_api_method["method"],
                        "time": (datetime.now() - timedelta(days=randint(0, 7))).strftime(Date_format)
                    }
                }
                log_json_resp["hits"]["hits"].append(hit)

            log_file.write(str(log_json_resp))

form_log_fact_result_json(2)