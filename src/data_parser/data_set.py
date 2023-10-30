from src.data_parser.data_frame import DataFrame
from src.utils.logger import Logger


class DataSet:
    def __init__(self, path_to_source):
        self.result_data_set = []
        self.path_to_source = path_to_source
        self.logger = Logger().logger
        self.fact = "fact" in path_to_source
        self.expected = "expected" in path_to_source
        self.criticality_map = \
            [
                {
                    "api_methods": [
                        '/api/v1/login/',
                        '/api/config/',
                        '/api/v5/main/'
                    ],
                    "criticality": 1
                },
                {
                    "api_methods": [
                        '/api/stores/{obj_id}/',
                        '/api/employees/'
                    ],
                    "criticality": 0.9
                },
                {
                    "api_methods": [
                        '/api/tasks/{id}/',
                        '/api/v4/tasks/{id}/',
                        '/api/v5/tasks/'
                    ],
                    "criticality": 0.8
                },
                {
                    "api_methods": [
                        '/api/basket-placing/',
                        '/api/v2/basket/items/',
                        '/api/basket-local-inventory/update_and_get_all_items/'
                    ],
                    "criticality": 0.7
                },
                {
                    "api_methods": [
                        '/api/seals/actions/{id}/'
                    ],
                    "criticality": 0.6
                },
                {
                    "api_methods": [
                        '/api-web/statistics/',
                        '/api-web/info-messages/',
                        '/api-web/info-messages-for-recipients/{id}/',
                        '/api-web/group-tasks/'
                    ],
                    "criticality": 0.5
                }
            ]

    def _increase_status(self, data_frame: DataFrame):
        for saved_data_frame in self.result_data_set:
            if saved_data_frame.api_method == data_frame.api_method:
                if data_frame.passed:
                    saved_data_frame.passed += 1
                if data_frame.failed:
                    saved_data_frame.failed += 1
                if data_frame.broken:
                    saved_data_frame.broken += 1
                if data_frame.skipped:
                    saved_data_frame.skipped += 1
                self.logger.debug(f"increased test_counter for  {saved_data_frame.api_method}")

    def _increase_rank(self, data_frame: DataFrame):
        for saved_data_frame in self.result_data_set:
            if saved_data_frame.api_method == data_frame.api_method:
                saved_data_frame.frequency += 1
                self.logger.debug(f"increased rank for {saved_data_frame.api_method}")

    def _append_query_params(self, data_frame: DataFrame):
        for saved_data_frame in self.result_data_set:
            if saved_data_frame.api_method == data_frame.api_method:
                for query_param in data_frame.query_list:
                    if query_param not in saved_data_frame.query_list:
                        saved_data_frame.query_list.append(query_param)
                        self.logger.debug(f"added query param to {saved_data_frame.api_method}")

    def _append_status_codes(self, data_frame: DataFrame):
        for saved_data_frame in self.result_data_set:
            if saved_data_frame.api_method == data_frame.api_method:
                for status_code in data_frame.status_codes:
                    if status_code not in saved_data_frame.status_codes:
                        saved_data_frame.status_codes.append(status_code)
                        self.logger.debug(f"added status code {status_code} to {saved_data_frame.api_method}")

    def _set_criticality(self, data_frame: DataFrame):
        for saved_data_frame in self.result_data_set:
            if saved_data_frame.api_method == data_frame.api_method:
                for api_methods_criticality_info in self.criticality_map:
                    for api_method in api_methods_criticality_info["api_methods"]:
                        if api_method in saved_data_frame.api_method:
                            saved_data_frame.criticality = api_methods_criticality_info["criticality"]
                            self.logger.debug(f"changed criticallity {api_methods_criticality_info['criticality']}"
                                              f" to {saved_data_frame.api_method}")

    def append_data_frame(self, data_frame: DataFrame):
        if data_frame.api_method not in [data_frame.api_method for data_frame in self.result_data_set]:
            self.result_data_set.append(data_frame)

        self._increase_rank(data_frame=data_frame)
        self._increase_status(data_frame=data_frame)
        self._append_query_params(data_frame=data_frame)
        self._append_status_codes(data_frame=data_frame)
        self._set_criticality(data_frame=data_frame)
