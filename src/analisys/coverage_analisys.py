import os
import matplotlib.pyplot as plt
import pandas as pd
from utils.data_coverage_parser.data_parser import DataSet

class CoverageAnalisys:
    def __init__(self, fact_data_set: DataSet, expected_data_set: DataSet):
        self.fact_data_set = fact_data_set.result_data_set
        self.expected_data_set = expected_data_set.result_data_set

    @staticmethod
    def get_top_n_api_methods(data_set: DataSet, top_n: int):
        data_set_to_sort = data_set.result_data_set
        data_set_to_sort.sort(key=lambda data_frame: data_frame.rank, reverse=True)
        return data_set_to_sort[:top_n]

    def get_tested_unused_api_methods(self, expected_data_set=None, fact_data_set=None):
        expected_list, fact_list = self.expected_data_set, self.fact_data_set
        if expected_data_set:
            expected_list = expected_data_set
        if fact_data_set:
            fact_list = fact_data_set

        return list(filter(
            lambda data_frame: data_frame.api_method not in [
                data_frame.api_method for data_frame in expected_list
            ],
            fact_list
        ))

    def get_untested_used_api_methods(self, expected_data_set=None, fact_data_set=None):
        expected_list, fact_list = self.expected_data_set, self.fact_data_set
        if expected_data_set:
            expected_list = expected_data_set
        if fact_data_set:
            fact_list = fact_data_set

        return list(filter(
            lambda data_frame: data_frame.api_method not in [
                data_frame.api_method for data_frame in fact_list
            ],
            expected_list
        ))

    def get_tested_api_methods(self, expected_data_set=None, fact_data_set=None):
        expected_list, fact_list = self.expected_data_set, self.fact_data_set
        if expected_data_set:
            expected_list = expected_data_set
        if fact_data_set:
            fact_list = fact_data_set

        return list(filter(
            lambda data_frame: data_frame.api_method in [
                data_frame.api_method for data_frame in fact_list
            ],
            expected_list
        ))

    def get_fact_stat(self, expected_data_set: list):
        return [
            data_frame for data_frame in self.fact_data_set if data_frame.api_method in [
                expected_data_frame.api_method for expected_data_frame in expected_data_set
            ]
        ]