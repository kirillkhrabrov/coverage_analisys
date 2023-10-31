import os
import matplotlib.pyplot as plt
import pandas as pd
from src.data_parser.data_set import DataSet

class PData:
    def __init__(self, data: list, columns: list, sort_by=None):
        out_data = []
        for data_frame in data:
            data_part = [getattr(data_frame, attr_name) for attr_name in columns]
            out_data.append(data_part)
        self.data = out_data
        self.columns = columns
        self.df = pd.DataFrame(self.data, columns=self.columns)
        if sort_by:
            self.df.sort_values(by=sort_by)