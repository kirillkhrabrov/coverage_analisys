import os
import zipfile
import requests
import base64
import json

from config import KibanaRequest
from src.data_parser.data_set import DataSet
from src.data_parser.data_frame import DataFrame
from src.utils.logger import Logger


class DataParser:
    PATTERN_HTTP_REQ = r'(GET|POST|PUT|DELETE|PATCH).*(\/api\S*);?'
    PATTERN_UUID4 = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}'
    PATTERN_OBJ_ID = r'\/[^v]?\d{1,5}\D?\/'

    def __init__(self, fact_results_source=None, expected_results_source=None):
        self.fact_results_source = fact_results_source
        self.expected_results_source = expected_results_source
        self.logger = Logger().logger

    # TODO
    # update regex
    # parse file types

    @staticmethod
    def _get_elk_response():
        auth_response = requests.request(
            "POST",
            KibanaRequest.KIBANA_AUTH_URL,
            headers=KibanaRequest.REQUEST_HEADERS,
            data=json.dumps(json.loads(base64.b64decode(
                KibanaRequest.AUTH_REQUEST_PAYLOAD,
                altchars=None,
                validate=False)))
        )

        KibanaRequest.REQUEST_HEADERS["Cookie"] = auth_response.headers["set-cookie"].split(';')[0]

        log_req_result = requests.request(
            "POST",
            KibanaRequest.KIBANA_REQ_URL,
            headers=KibanaRequest.REQUEST_HEADERS,
            data=json.dumps(KibanaRequest.REQUEST_PAYLOAD))

        return log_req_result.json()["rawResponse"]["hits"]["hits"]

    def __get_files_from_dir(self, path_to_source):
        try:
            if os.listdir(path_to_source):
                for file in os.listdir(path_to_source):
                    if ".zip" in file:
                        with zipfile.ZipFile(os.path.join(path_to_source, file), 'r') as zip_ref:
                            zip_ref.extractall(path_to_source)
                            self.logger.info(f"Extracted from  {file}")
                            continue
                    yield file
                    self.logger.debug(f"Read {file}")
            self.logger.debug(f"{path_to_source} is empty")

        except Exception as e:
            self.logger.error(f"Cannot get files from dir: {str(e)}")

    def __read_file(self, file_name, path_to_source):
        try:
            with open(os.path.join(path_to_source, file_name), "r", encoding='utf-8') as f:
                content = f.read()
                self.logger.debug(f"Parsed {file_name}")
                return content

        except Exception as e:
            self.logger.error(f"Cannot read file: {str(e)}")

    def __form_attachments_files_list_from_file(self, file_content_to_parse):
        try:
            return [attach["source"] for attach in file_content_to_parse.get("attachments") if 'log' in attach["name"]]
        except Exception:
            self.logger.debug(f'No attachments in file')

    def set_data_frame(self, data_set_to_save_data_frames: DataSet):
        source = data_set_to_save_data_frames.path_to_source
        for result_file in self.__get_files_from_dir(source):
            result_json_content = self.__read_file(
                file_name=result_file,
                path_to_source=source
            )

            print(result_json_content)
    #         attachments = DataParser._form_attachments_files_list(json_content_to_parse=result_json_content)
    #
    #         if attachments:
    #             for log_file in attachments:
    #                 log_content = self._read_file(result_file_name=log_file)
    #                 http_req_logs = re.findall(DataParser.PATTERN_HTTP_REQ, log_content)
    #
    #                 for http_log in http_req_logs:
    #                     http_method = http_log[0]
    #                     corrected_http_log = http_log[1][:-1] if http_log[1][-1] == ';' else http_log[1]
    #                     http_url_query = corrected_http_log.split("?")
    #                     http_after_masked_uuid = re.sub(
    #                         DataParser.PATTERN_UUID4,
    #                         "{id}",
    #                         http_url_query[0]
    #                     )
    #                     http_after_masked_obj_id = re.sub(
    #                         DataParser.PATTERN_OBJ_ID,
    #                         "/{obj_id}/",
    #                         http_after_masked_uuid
    #                     )
    #                     if http_after_masked_obj_id[-1] != '/':
    #                         http_after_masked_obj_id += '/'
    #
    #                     data_frame = DataFrame(
    #                         api_method=f'{http_method} {http_after_masked_obj_id}',
    #                         test_status=result_json_content.get("status"),
    #                         query_list=http_url_query[1].split("&") if len(http_url_query) > 1 else []
    #                     )
    #
    #                     data_set_to_save_data_frames.append_data_frame(data_frame=data_frame)
    #
    # def set_expected_data_frame(self, data_set_to_save_data_frames: DataSet):
    #     for log_result in self._get_expected_api_requests():
    #         full_path = log_result["_source"]["full_path"].split("?")
    #         http_after_masked_uuid = re.sub(
    #             DataParser.PATTERN_UUID4,
    #             "{id}",
    #             full_path[0]
    #         )
    #         http_after_masked_obj_id = re.sub(
    #             DataParser.PATTERN_OBJ_ID,
    #             "/{obj_id}/",
    #             http_after_masked_uuid
    #         )
    #         if http_after_masked_obj_id[-1] != '/':
    #             http_after_masked_obj_id += '/'
    #         data_frame = DataFrame(
    #             api_method=f'{log_result["_source"]["method"]} {http_after_masked_obj_id}',
    #             query_list=full_path[1].split("&") if len(full_path) > 1 else []
    #         )
    #         data_set_to_save_data_frames.append_data_frame(data_frame=data_frame)
