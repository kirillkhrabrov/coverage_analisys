import pandas as pd


class PData:
    def __init__(self, data: list, columns: list, sort_by: str = None):
        """
        Class for transforming result lists of DataFrames into Pandas' dataframes

        :param:
            data (list): result list of DataFrames to be converted
            columns (list): list of columns (series) to be saved in Pandas' dataframe
            sort_by (str): param of DataFrame to be sorted by
        """
        out_data = []
        for data_frame in data:
            data_part = [getattr(data_frame, attr_name) for attr_name in columns]
            out_data.append(data_part)
        self.data = out_data
        self.columns = columns
        self.df = pd.DataFrame(self.data, columns=self.columns)
        if sort_by:
            self.df.sort_values(by=sort_by)
