import os
import requests
import base64
import json
import re

from config import KibanaRequest
from src.data_parser.data_set import DataSet
from src.data_parser.data_frame import DataFrame
from src.utils.logger import Logger


class DataParser:
    PATTERN_HTTP_REQ = r'(GET|POST|PUT|DELETE|PATCH).*(\/api\S*).*code.*(\d{3})'
    PATTERN_UUID4 = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}'
    PATTERN_OBJ_ID = r'\/[^v]?\d{1,5}\D?\/'

    def __init__(self, fact_results_source=None, expected_results_source=None):
        self.fact_results_source = fact_results_source
        self.expected_results_source = expected_results_source
        self.logger = Logger().logger

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
                    self.logger.debug(f"Get {file} from {path_to_source}")
                    yield file
            self.logger.debug(f"{path_to_source} is empty")

        except Exception as e:
            self.logger.error(f"Cannot get files from dir: {path_to_source} -> {str(e)}")

    def __read_file(self, file_name, path_to_source):
        try:
            with open(os.path.join(path_to_source, file_name), "r", encoding='utf-8') as f:
                content = f.read()
                if 'json' in file_name:
                    content = json.loads(content.replace("'", '"'))
                self.logger.debug(f"Read {file_name}")
                return content

        except Exception as e:
            self.logger.error(f"Cannot read file: {file_name} -> {str(e)}")

    def __form_attachments_files_list_from_file(self, file_content_to_parse):
        try:
            attach_list = file_content_to_parse.get("attachments")
            return [attach["source"] for attach in attach_list if 'log' in attach["name"]]
        except Exception as e:
            self.logger.debug(f'No attachments in file -> {str(e)}')

    def __parse_log_file(self, log_file_content):
        log_file_content_matches = re.findall(DataParser.PATTERN_HTTP_REQ, str(log_file_content))
        try:
            for found_group_matches in log_file_content_matches:
                http_method = found_group_matches[0]
                http_path_after_masked_uuid = re.sub(
                    DataParser.PATTERN_UUID4,
                    "{id}",
                    found_group_matches[1])
                http_path_after_masked_obj_id = re.sub(
                    DataParser.PATTERN_OBJ_ID,
                    "/{obj_id}/",
                    http_path_after_masked_uuid
                )
                http_query_list = http_path_after_masked_obj_id.split('?')[1].split("&") if len(http_path_after_masked_obj_id.split('?')) > 1 else []
                http_status_code = found_group_matches[2]

                print('end pasring')

                return (
                    http_method,
                    http_path_after_masked_obj_id,
                    http_query_list,
                    http_status_code
                )
        except Exception as e:
            self.logger.error(f'Cannot parse  {log_file_content} -> {str(e)}')






        # data_frame = DataFrame(
        #     api_method=f'{http_method} {http_after_masked_obj_id}',
        #     test_status=result_json_content.get("status"),
        #     query_list=http_url_query[1].split("&") if len(http_url_query) > 1 else []
        # )
        #
        # data_set_to_save_data_frames.append_data_frame(data_frame=data_frame)

    def set_data_frame(self, data_set_to_save_data_frames: DataSet):
        source = data_set_to_save_data_frames.path_to_source
        files = list(self.__get_files_from_dir(source))
        for file in files:
            file_content = self.__read_file(
                file_name=file,
                path_to_source=source
            )

            attachments = self.__form_attachments_files_list_from_file(
                file_content_to_parse=file_content
            )

            if attachments:
                for log_file in attachments:
                    parsed_http = self.__parse_log_file(
                        log_file_content=self.__read_file(
                            file_name=log_file,
                            path_to_source=source
                        )
                    )




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
