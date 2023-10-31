from src.data_parser.data_set import DataSet


class CoverageAnalisys:
    def __init__(self, fact_data_set: DataSet, expected_data_set: DataSet):
        """
        Class to form result lists of DataFrames with API method info.
        Result lists can be sorted, formed in different ways due to its purporse

        :param:
            fact_data_set (DataSet): DataSet with fact result info
            expected_data_set (DataSet): DataSet with expected result info
        """
        self.fact_data_set_result = fact_data_set.result_data_set
        self.expected_data_set_result = expected_data_set.result_data_set

    @staticmethod
    def get_top_n_api_methods(data_set: DataSet, top_n: int = None, sort_by: str = 'frequency') -> list:
        """
        Method to form result list with given length, or sorted field

        :param:
            data_set (DataSet): DataSet to be sorted, saved with given length
            top_n (int): length of result list to be saved
            sort_by (str): DESC sorted field

        :returns:
            result list of given length, with DataFrames DESC sorted by {sort_by} param
        """
        data_set_to_sort = data_set.result_data_set
        data_set_to_sort.sort(
            key=lambda data_frame: data_frame.frequency if sort_by == 'frequency' else data_frame.criticality,
            reverse=True
        )
        return data_set_to_sort[:top_n]

    def get_untested_status_codes_params(self, expected_result_lst: list = None, fact_result_lst: list = None) -> list:
        """
        Method to form result list DataFrames with untested status codes in DataFrame.status_codes attr

        :param:
            expected_result_lst (list): list of DataFrames with expected result info
            fact_result_lst (list): list of DataFrames with fact result info

        :returns:
            result list of DataFrames with untested status codes in DataFrame.status_codes attr
        """
        expected_list, fact_list = self.expected_data_set_result, self.fact_data_set_result
        if expected_result_lst:
            expected_list = expected_result_lst
        if fact_result_lst:
            fact_list = fact_result_lst

        result_data_set = []
        for expected_data_frame in expected_list:
            for fact_data_frame in fact_list:
                if expected_data_frame.api_method == fact_data_frame.api_method:
                    copied_expected_data_frame = expected_data_frame
                    copied_expected_data_frame.status_codes = list(
                        set(expected_data_frame.status_codes) - set(fact_data_frame.status_codes)
                    )
                    if copied_expected_data_frame.status_codes:
                        result_data_set.append(copied_expected_data_frame)
        return result_data_set

    def get_untested_query_params(self, expected_result_lst: list = None, fact_result_lst: list = None) -> list:
        """
        Method to form result list DataFrames with untested query params in DataFrame.query_params attr

        :param:
            expected_result_lst (list): list of DataFrames with expected result info
            fact_result_lst (list): list of DataFrames with fact result info

        :returns:
            result list of DataFrames with untested query params in DataFrame.query_params attr
        """
        expected_list, fact_list = self.expected_data_set_result, self.fact_data_set_result
        if expected_result_lst:
            expected_list = expected_result_lst
        if fact_result_lst:
            fact_list = fact_result_lst

        result_data_set = []
        for expected_data_frame in expected_list:
            for fact_data_frame in fact_list:
                if expected_data_frame.api_method == fact_data_frame.api_method:
                    copied_expected_data_frame = expected_data_frame
                    copied_expected_data_frame.query_list = list(
                        set(expected_data_frame.query_list) - set(fact_data_frame.query_list)
                    )
                    if copied_expected_data_frame.query_list:
                        result_data_set.append(copied_expected_data_frame)
        return result_data_set

    def get_untested_used_api_methods(self, expected_result_lst: list = None, fact_result_lst: list = None) -> list:
        """
        Method to form DataFrames with info about untested API methods

        :param:
            expected_result_lst (list): list of DataFrames with expected result info
            fact_result_lst (list): list of DataFrames with fact result info

        :returns:
            result list of DataFrames with info about untested API methods
        """
        expected_list, fact_list = self.expected_data_set_result, self.fact_data_set_result
        if expected_result_lst:
            expected_list = expected_result_lst
        if fact_result_lst:
            fact_list = fact_result_lst

        return list(filter(
            lambda data_frame: data_frame.api_method not in [
                data_frame.api_method for data_frame in fact_list
            ],
            expected_list
        ))

    def get_tested_api_methods(self, expected_result_lst: list = None, fact_result_lst: list = None) -> list:
        """
        Method to form DataFrames with info about tested API methods

        :param:
            expected_result_lst (list): list of DataFrames with expected result info
            fact_result_lst (list): list of DataFrames with fact result info

        :returns:
            result list of DataFrames with info about tested API methods
        """
        expected_list, fact_list = self.expected_data_set_result, self.fact_data_set_result
        if expected_result_lst:
            expected_list = expected_result_lst
        if fact_result_lst:
            fact_list = fact_result_lst

        return list(filter(
            lambda data_frame: data_frame.api_method in [
                data_frame.api_method for data_frame in fact_list
            ],
            expected_list
        ))

    def get_fact_stat(self, expected_result_lst: list = None) -> list:
        """
        Method to form DataFrames with info about test run results of expected API methods

        :param:
            expected_result_lst (list): list of DataFrames with expected result info
            fact_result_lst (list): list of DataFrames with fact result info

        :returns:
            result list of DataFrames with info about tested API methods
        """
        return [
            data_frame for data_frame in self.fact_data_set_result if data_frame.api_method in [
                expected_data_frame.api_method for expected_data_frame in expected_result_lst
            ]
        ]
