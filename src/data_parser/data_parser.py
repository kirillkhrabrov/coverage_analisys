class DataParser:
    PATTERN_HTTP_REQ = r'(GET|POST|PUT|DELETE|PATCH).*(\/api\S*);?'
    PATTERN_UUID4 = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}'
    PATTERN_OBJ_ID = r'\/[^v]?\d{1,5}\D?\/'

    def __init__(self, fact_results_source=None, expected_results_source=None):
        self.fact_results_source = fact_results_source
        self.expected_results_source = expected_results_source

    @staticmethod
    def _form_attachments_files_list(json_content_to_parse):
        try:
            return [attach["source"] for attach in json_content_to_parse.get("attachments") if 'log' in attach["name"]]
        except Exception:
            logger.write_text_log('info', 'No attachments')

    @staticmethod
    def _get_expected_api_requests():
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

    def _read_file(self, result_file_name, json_need_to_be_corrected=False):
        try:
            with open(os.path.join(self.fact_results_source, result_file_name), "r", encoding='utf-8') as f:
                content = f.read()
                if json_need_to_be_corrected:
                    content = json.loads(content.replace('"', '\"'))
                logger.write_text_log("info", f"Parsed {result_file_name}")
                return content

        except Exception as e:
            logger.write_text_log("error", str(e))

    def _get_files_from_results_dir(self):
        try:
            for file_name in os.listdir(self.fact_results_source):
                if os.path.isfile(os.path.join(self.fact_results_source, file_name)) and "result" in file_name:
                    yield file_name
                    logger.write_text_log("info", f"Read {file_name}")

        except Exception as e:
            logger.write_text_log("error", str(e))

    def set_fact_data_frame(self, data_set_to_save_data_frames: DataSet):
        for result_file in self._get_files_from_results_dir():
            result_json_content = self._read_file(
                result_file_name=result_file,
                json_need_to_be_corrected=True
            )

            attachments = DataParser._form_attachments_files_list(json_content_to_parse=result_json_content)

            if attachments:
                for log_file in attachments:
                    log_content = self._read_file(result_file_name=log_file)
                    http_req_logs = re.findall(DataParser.PATTERN_HTTP_REQ, log_content)

                    for http_log in http_req_logs:
                        http_method = http_log[0]
                        corrected_http_log = http_log[1][:-1] if http_log[1][-1] == ';' else http_log[1]
                        http_url_query = corrected_http_log.split("?")
                        http_after_masked_uuid = re.sub(
                            DataParser.PATTERN_UUID4,
                            "{id}",
                            http_url_query[0]
                        )
                        http_after_masked_obj_id = re.sub(
                            DataParser.PATTERN_OBJ_ID,
                            "/{obj_id}/",
                            http_after_masked_uuid
                        )
                        if http_after_masked_obj_id[-1] != '/':
                            http_after_masked_obj_id += '/'

                        data_frame = DataFrame(
                            api_method=f'{http_method} {http_after_masked_obj_id}',
                            test_status=result_json_content.get("status"),
                            query_list=http_url_query[1].split("&") if len(http_url_query) > 1 else []
                        )

                        data_set_to_save_data_frames.append_data_frame(data_frame=data_frame)

    def set_expected_data_frame(self, data_set_to_save_data_frames: DataSet):
        for log_result in self._get_expected_api_requests():
            full_path = log_result["_source"]["full_path"].split("?")
            http_after_masked_uuid = re.sub(
                DataParser.PATTERN_UUID4,
                "{id}",
                full_path[0]
            )
            http_after_masked_obj_id = re.sub(
                DataParser.PATTERN_OBJ_ID,
                "/{obj_id}/",
                http_after_masked_uuid
            )
            if http_after_masked_obj_id[-1] != '/':
                http_after_masked_obj_id += '/'
            data_frame = DataFrame(
                api_method=f'{log_result["_source"]["method"]} {http_after_masked_obj_id}',
                query_list=full_path[1].split("&") if len(full_path) > 1 else []
            )
            data_set_to_save_data_frames.append_data_frame(data_frame=data_frame)