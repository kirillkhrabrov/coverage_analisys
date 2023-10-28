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
    def __init__(self, fact_results_source=None, expected_results_source=None):
        """
        Class for traversing through files, parsing files, collect info
        about api methods.

        :param:
                fact_results_source (str): path to fact data files
                expected_results_source (str): path to expect data files
        """
        self.fact_results_source = fact_results_source
        self.expected_results_source = expected_results_source
        self.logger = Logger().logger

    @staticmethod
    def _get_elk_response() -> dict:
        """
        Method for getting info about api methods over ELK API request.
        KibanaRequest.KIBANA_AUTH_URL - ELK internal search method's endpoint
        KibanaRequest.REQUEST_HEADERS - ELK Request headesrs, auth included
        KibanaRequest.AUTH_REQUEST_PAYLOAD -ELK Request payloads with params snippet

        :returns:
            json with real agents' API methods calls
        """
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
        """
        Method for traversing through directory with reports< log files,
        yielding file to read

        :param:
            path_to_source (str): path to fact / expected data files

        :returns:
            yielded file from fact / expected data directory
        """
        try:
            if os.listdir(path_to_source):
                for file in os.listdir(path_to_source):
                    self.logger.debug(f"Get {file} from {path_to_source}")
                    yield file
            self.logger.debug(f"{path_to_source} is empty")

        except Exception as e:
            self.logger.error(f"Cannot get files from dir: {path_to_source} -> {str(e)}")

    def __read_file(self, file_name: str, path_to_source: str) -> str or dict:
        """
        Method for reading the content of file.
        If this file is JSON format, method replaces
        single quotes with doubles

        :param:
            file_name (str): name of file to be read
            path_to_source (str): path to fact / expected data files

        :returns:
            file content as string or dict in case of file to be JSON
        """
        try:
            with open(os.path.join(path_to_source, file_name), "r", encoding='utf-8') as f:
                content = f.read()
                if 'json' in file_name:
                    content = json.loads(content.replace("'", '"'))
                self.logger.debug(f"Read {file_name}")
                return content

        except Exception as e:
            self.logger.error(f"Cannot read file: {file_name} -> {str(e)}")

    def __form_attachments_files_list_from_file(self, file_name: str, file_content_to_parse: str or dict) -> list:
        """
        Method to check if {file_content_to_parse} is parsed as dict
        and contains "attachments".
        If this is true, method returns the name of attachment files

        :param:
            file_name (str): name of file to be read
            file_content_to_parse (str, dict): file content expected to be converted into dict

        :returns:
            file from fact / expected data directory
        """
        if isinstance(file_content_to_parse, dict):
            try:
                attach_list = file_content_to_parse.get("attachments")
                self.logger.debug(f'Form attach files from {file_name}')
                return [attach["source"] for attach in attach_list if 'log' in attach["name"]]

            except Exception as e:
                self.logger.debug(f'No attachments in file {file_name} -> {str(e)}')

    def __return_api_info_from_log_file(self, log_file_content: str) -> list:
        """
        Method to return parsed api method from .txt log_file
        At first method finds all HTTP methods + HTTP path in log file
        After that HTTP path splits into HTTP endpoint and query params if they exist
        Then changes UUID4 ids to impersonal {id}
        After that changes proprietary ids to {obj_id}
        HTTP status code and query params are cached

        :param:
            log_file_content (str): file content converted to dict

        :returns:
            list of API methods info
        """
        PATTERN_HTTP_REQ = r'(GET|POST|PUT|DELETE|PATCH).*(\/api\S*).*code.*(\d{3})'
        PATTERN_UUID4 = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}'
        PATTERN_OBJ_ID = r'\/[^v]?\d{1,5}\D?\/'
        api_methods_info = []

        try:
            self.logger.debug(f'Trying to return api info log_file_content')
            log_file_content_matches = re.findall(PATTERN_HTTP_REQ, str(log_file_content))
            for found_group_matches in log_file_content_matches:
                http_method = found_group_matches[0]
                http_path_after_masked_uuid = re.sub(
                    PATTERN_UUID4,
                    "{id}",
                    found_group_matches[1])
                http_path_after_masked_obj_id = re.sub(
                    PATTERN_OBJ_ID,
                    "/{obj_id}/",
                    http_path_after_masked_uuid
                )
                http_query_list = http_path_after_masked_obj_id.split('?')[1].split("&") if len(http_path_after_masked_obj_id.split('?')) > 1 else []
                http_path_after_masked_obj_id = http_path_after_masked_obj_id.split('?')[0]
                http_status_code = [int(found_group_matches[2])]

                api_method_info = (
                    http_method,
                    http_path_after_masked_obj_id,
                    http_query_list,
                    http_status_code
                )
                api_methods_info.append(api_method_info)
                self.logger.debug(f'Parsed {api_method_info} from log_file_content')

            return api_methods_info

        except Exception as e:
            self.logger.error(f'Cannot parse  {log_file_content} -> {str(e)}')

    def __return_api_info_from_fact_json_file(self, file_name: str, json_file_fact_content: dict) -> list:
        """
        Method to return parsed api method from .json file for fact result
        At first method traverse through all step names,
        finds all HTTP methods + HTTP path in fact result file
        After that HTTP path splits into HTTP endpoint and query params if they exist
        Then changes UUID4 ids to impersonal {id}
        After that changes proprietary ids to {obj_id}
        HTTP status code and query params are cached

        :param:
            file_name (str): name of file to be read
            json_file_fact_content (dict): file content converted to dict

        :returns:
            list of API methods info
        """
        PATTERN_HTTP_REQ = r'(GET|POST|PUT|DELETE|PATCH).*(\/api\S*)'
        PATTERN_STATUS_CODE = r'(\d{3})'
        PATTERN_UUID4 = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}'
        PATTERN_OBJ_ID = r'\/[^v]?\d{1,5}\D?\/'
        api_methods_info = []
        try:
            self.logger.debug(f'Trying to return api info json_file_fact_content')
            for step in json_file_fact_content["steps"]:
                step_name_matches = re.findall(PATTERN_HTTP_REQ, str(step["name"]))[0]

                http_method = step_name_matches[0]
                http_path_after_masked_uuid = re.sub(
                    PATTERN_UUID4,
                    "{id}",
                    step_name_matches[1])
                http_path_after_masked_obj_id = re.sub(
                    PATTERN_OBJ_ID,
                    "/{obj_id}/",
                    http_path_after_masked_uuid
                )
                http_query_list = http_path_after_masked_obj_id.split('?')[1].split("&") if len(http_path_after_masked_obj_id.split('?')) > 1 else []
                http_path_after_masked_obj_id = http_path_after_masked_obj_id.split('?')[0]
                status_code = re.findall(PATTERN_STATUS_CODE, str(step["steps"][0]["name"]))[0]
                http_status_code = [int(status_code)]

                api_method_info = (
                    http_method,
                    http_path_after_masked_obj_id,
                    http_query_list,
                    http_status_code
                )
                self.logger.debug(f'Parsed {api_method_info} from json_file_fact_content {file_name}')
                api_methods_info.append(api_method_info)

            return api_methods_info

        except Exception as e:
            self.logger.error(f'Cannot parse  {file_name} -> {str(e)}')

    def __return_api_info_from_expected_json_file(self, file_name: str, json_file_expected_content: dict) -> list:
        """
        Method to return parsed api method from .json file for expected result
        At first method traverse through all hits section,
        finds all HTTP methods + HTTP path in expected result file
        After that HTTP path splits into HTTP endpoint and query params if they exist
        Then changes UUID4 ids to impersonal {id}
        After that changes proprietary ids to {obj_id}
        HTTP status code and query params are cached

        :param:
            file_name (str): name of file to be read
            json_file_expected_content (dict): file content converted to dict

        :returns:
            list of API methods info
        """
        PATTERN_UUID4 = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}'
        PATTERN_OBJ_ID = r'\/[^v]?\d{1,5}\D?\/'
        api_methods_info = []

        try:
            self.logger.debug(f'Trying to return api info json_file_expected_content')
            for hit in json_file_expected_content["hits"]["hits"]:
                api_method_info = hit["_source"]
                http_method = api_method_info["method"]
                http_path_after_masked_uuid = re.sub(
                    PATTERN_UUID4,
                    "{id}",
                    api_method_info["full_path"])
                http_path_after_masked_obj_id = re.sub(
                    PATTERN_OBJ_ID,
                    "/{obj_id}/",
                    http_path_after_masked_uuid
                )
                http_query_list = http_path_after_masked_obj_id.split('?')[1].split("&") if len(http_path_after_masked_obj_id.split('?')) > 1 else []
                http_path_after_masked_obj_id = http_path_after_masked_obj_id.split('?')[0]
                http_status_code = [int(api_method_info["status_code"])]

                api_method_info = (
                    http_method,
                    http_path_after_masked_obj_id,
                    http_query_list,
                    http_status_code
                )
                self.logger.debug(f'Parsed {api_method_info} from json_file_expected_content {file_name}')
                api_methods_info.append(api_method_info)

            return api_methods_info

        except Exception as e:
            self.logger.error(f'Cannot parse {file_name} -> {str(e)}')

    def _set_data_frame_from_attach(self,  file_name: str, file_content: str or dict, data_set_to_save_data_frames: DataSet):
        """
        Method to implement DataFrame object with provided api methods info
        and save it to passed into method data set
        The source of api method is log file

        :param:
            file_name (str): name of passed into method file
            file_content (str, dict): file content expected to be converted into dict
            data_set_to_save_data_frames (DataSet): DataSet instance to save implemented DataFrame objects to
        """
        attachments = self.__form_attachments_files_list_from_file(
            file_name=file_name,
            file_content_to_parse=file_content
        )
        if attachments:
            self.logger.debug(f'Try to set_data_frame_from_attach from {file_name}')
            for log_file in attachments:
                parsed_api_methods_info = self.__return_api_info_from_log_file(
                    log_file_content=self.__read_file(
                        file_name=log_file,
                        path_to_source=data_set_to_save_data_frames.path_to_source
                    )
                )

                for parsed_api_method_info in parsed_api_methods_info:

                    data_frame = DataFrame(
                        api_method=f'{parsed_api_method_info[0]} {parsed_api_method_info[1]}',
                        test_status=file_content.get("status"),
                        query_list=parsed_api_method_info[2],
                        status_code=parsed_api_method_info[3]
                    )

                    data_set_to_save_data_frames.append_data_frame(data_frame=data_frame)

        self.logger.debug(f'Parsing of {file_name} is complete')

    def _set_data_frame_from_json(self, file_name: str, file_content: str or dict, data_set_to_save_data_frames: DataSet):
        """
        Method to implement DataFrame object with provided api methods info
        and save it to passed into method data set
        The source of api method is json file

        :param:
            file_name (str): name of passed into method file
            file_content (str, dict): file content expected to be converted into dict
            data_set_to_save_data_frames (DataSet): DataSet instance to save implemented DataFrame objects to
        """
        if isinstance(file_content, dict) and "attachments" not in file_content:
            self.logger.debug(f'Try to set_data_frame_from_json from {file_name}')
            if data_set_to_save_data_frames.fact:
                parsed_api_methods_info = self.__return_api_info_from_fact_json_file(
                    file_name=file_name,
                    json_file_fact_content=file_content
                )

                for parsed_api_method_info in parsed_api_methods_info:

                    data_frame = DataFrame(
                        api_method=f'{parsed_api_method_info[0]} {parsed_api_method_info[1]}',
                        test_status=file_content.get("status"),
                        query_list=parsed_api_method_info[2],
                        status_code=parsed_api_method_info[3]
                    )

                    data_set_to_save_data_frames.append_data_frame(data_frame=data_frame)

            if data_set_to_save_data_frames.expected:
                parsed_api_methods_info = self.__return_api_info_from_expected_json_file(
                    file_name=file_name,
                    json_file_expected_content=file_content
                )

                for parsed_api_method_info in parsed_api_methods_info:

                    data_frame = DataFrame(
                        api_method=f'{parsed_api_method_info[0]} {parsed_api_method_info[1]}',
                        query_list=parsed_api_method_info[2],
                        status_code=parsed_api_method_info[3]
                    )

                    data_set_to_save_data_frames.append_data_frame(data_frame=data_frame)

        self.logger.debug(f'Parsing of {file_name} is complete')

    def set_data_frame(self, data_set_to_save_data_frames: DataSet):
        """
        Method to save api methods info into provided DataSet (fact or expected)

        :param:
            data_set_to_save_data_frames (DataSet): DataSet instance to save implemented DataFrame objects to
        """
        source = data_set_to_save_data_frames.path_to_source
        for file in self.__get_files_from_dir(source):
            file_content = self.__read_file(
                file_name=file,
                path_to_source=source
            )

            self._set_data_frame_from_attach(
                file_name=file,
                file_content=file_content,
                data_set_to_save_data_frames=data_set_to_save_data_frames
            )

            self._set_data_frame_from_json(
                file_name=file,
                file_content=file_content,
                data_set_to_save_data_frames=data_set_to_save_data_frames
            )
