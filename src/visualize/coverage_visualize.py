import os
import matplotlib.pyplot as plt
import pandas as pd
from utils.data_coverage_parser.data_parser import DataSet

class CoverageAnalisys:
    @staticmethod
    def build_info_table(**kwargs):
        fig, table_ax = plt.subplots(figsize=(11, 11))
        fig.patch.set_visible(False)
        table_ax.axis('off')
        table_ax.axis('tight')
        table_ax.table(
            colColours=['#CACACA'] * 6,
            cellText=kwargs["df"].values,
            colLabels=kwargs["df"].columns,
            loc='center'
        )
        table_ax.set_title(label=kwargs["title"])

        plt.tight_layout()
        plt.savefig(os.path.abspath('pandas_results') + f'/{kwargs["title"]}.svg')


    @staticmethod
    def build_info_gist_on_code_coverage(**kwargs):
        fig, gist_ax = plt.subplots()
        gist_ax.pie(
            x=kwargs["values"],
            labels=kwargs["labels"],
            colors=('green', 'red'),
            explode=(0.2, 0),
            autopct='%1.1f%%',
            shadow=True
        )
        fig.suptitle(t=kwargs["title"])

        plt.tight_layout()
        plt.savefig(os.path.abspath('pandas_results') + f'/{kwargs["title"]}.svg')


    @staticmethod
    def build_info_barh_on_code_coverage(width=0.8, **kwargs):
        df = kwargs["df"]
        fig, barh_ax = plt.subplots(figsize=(25, 25))
        barh_ax = df.plot.barh(
            title=kwargs["title"],
            ylabel=kwargs["ylabel"],
            xlabel=kwargs["xlabel"],
            x=kwargs["x"],
            y=kwargs["y"],
            width=width
        )
        barh_ax.spines[['right', 'top']].set_visible(False)
        barh_ax.grid(linestyle='-', linewidth=0.1)

        plt.tight_layout()
        plt.savefig(os.path.abspath('pandas_results') + f'/{kwargs["title"]}.svg')