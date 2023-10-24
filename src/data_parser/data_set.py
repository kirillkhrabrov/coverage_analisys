from src.data_parser.data_frame import DataFrame
from src.utils.logger import Logger

class DataSet:
    def __init__(self, path_to_source):
        self.result_data_set = []
        self.path_to_source = path_to_source
        self.logger = Logger().logger

    def _increase_status(self, data_frame: DataFrame):
        for saved_data_frame in self.result_data_set:
            if saved_data_frame.api_method == data_frame.api_method:
                if data_frame.passed > 0:
                    saved_data_frame.passed += 1
                if data_frame.failed > 0:
                    saved_data_frame.failed += 1
                if data_frame.broken > 0:
                    saved_data_frame.broken += 1
                if data_frame.skipped > 0:
                    saved_data_frame.skipped += 1
                self.logger.debug(f"increased test_counter for  {saved_data_frame.api_method}")

    def _increase_rank(self, data_frame: DataFrame):
        for saved_data_frame in self.result_data_set:
            if saved_data_frame.api_method == data_frame.api_method:
                saved_data_frame.rank += 1
                self.logger.debug(f"increased rank for {saved_data_frame.api_method}")

    def _append_query_params(self, data_frame: DataFrame):
        for saved_data_frame in self.result_data_set:
            if saved_data_frame.api_method == data_frame.api_method:
                for query_param in data_frame.query_list:
                    if query_param not in saved_data_frame.query_list:
                        saved_data_frame.query_list.append(query_param)
                        self.logger.debug(f"added query param to {saved_data_frame.api_method}")

    def append_data_frame(self, data_frame: DataFrame):
        if data_frame.api_method not in [data_frame.api_method for data_frame in self.result_data_set]:
            self.result_data_set.append(data_frame)

        self._increase_rank(data_frame=data_frame)
        self._increase_status(data_frame=data_frame)
        self._append_query_params(data_frame=data_frame)
