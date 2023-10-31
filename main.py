import os
from src.data_parser.data_parser import DataParser
from src.data_parser.data_set import DataSet
from src.analisys.coverage_analisys import CoverageAnalisys
from src.visualize.pdata import PData
from src.visualize.coverage_visualize import CoverageVisualize

PATH_TO_FACT_RESULTS = os.path.abspath('data/fact_data')
PATH_TO_EXPECTED_RESULTS = os.path.abspath('data/expected_data')

data_parser = DataParser(
    fact_results_source=PATH_TO_FACT_RESULTS,
    expected_results_source=PATH_TO_EXPECTED_RESULTS
)

fact_data_set = DataSet(path_to_source=PATH_TO_FACT_RESULTS)
expected_data_set = DataSet(path_to_source=PATH_TO_EXPECTED_RESULTS)

data_parser.set_data_frame(data_set_to_save_data_frames=fact_data_set)
data_parser.set_data_frame(data_set_to_save_data_frames=expected_data_set)

coverage_analyzer = CoverageAnalisys(
    fact_data_set=fact_data_set,
    expected_data_set=expected_data_set
)

# Топ 50 используемых API методов, отсортированных по частоте
top_50_expected_sorted_by_freq = coverage_analyzer.get_top_n_api_methods(
    data_set=expected_data_set,
    top_n=50
)

# Топ 50 используемых API методов, отсортированных по критичности
top_50_expected_sorted_by_crit = coverage_analyzer.get_top_n_api_methods(
    data_set=expected_data_set,
    top_n=50,
    sort_by='criticality'
)

# Протестированные API методы, отсортированные по частоте
fact_sorted_by_freq = coverage_analyzer.get_top_n_api_methods(
    data_set=fact_data_set
)

# Протестированные API методы, отсортированные по критичности
fact_sorted_by_crit = coverage_analyzer.get_top_n_api_methods(
    data_set=fact_data_set,
    sort_by='criticality'
)

# Не покрытые тестами query параметры из Топ 50 используемых методов
untested_queries_from_top_50_expected = coverage_analyzer.get_untested_query_params(
    expected_result_lst=top_50_expected_sorted_by_crit,
    fact_result_lst=fact_sorted_by_crit
)

# Не покрытые тестами status codes из Топ 50 используемых методов
untested_codes_from_top_50_expected = coverage_analyzer.get_untested_status_codes_params(
    expected_result_lst=top_50_expected_sorted_by_crit,
    fact_result_lst=fact_sorted_by_crit
)

# Не протестированные критичные API методы из ТОП 50
untested_from_top_50_api_methods_crit = coverage_analyzer.get_untested_used_api_methods(
    expected_result_lst=top_50_expected_sorted_by_crit
)

# Не протестированные частые API методы из ТОП 50
untested_from_top_50_api_methods_freq = coverage_analyzer.get_untested_used_api_methods(
    expected_result_lst=top_50_expected_sorted_by_freq
)


# Статистика по 15 самым протестированным API методам
top_15_fact_stat = coverage_analyzer.get_fact_stat(
    expected_result_lst=coverage_analyzer.get_top_n_api_methods(fact_data_set, 15)
)

print('end')


# # top 50 expected API Methods table
# top_50_expected_df = PData(
#     data=top_50_expected,
#     columns=["api_method", "rank"],
#     sort_by='rank'
# ).df
# CoverageVisualizer.build_info_table(
#     df=top_50_expected_df,
#     title='Топ 50 наиболее популярных API методов'
# )
#
# # top 50 fact API Methods table
# top_50_fact_df = PData(
#     data=top_50_fact,
#     columns=["api_method", "skipped", "broken", "passed", "failed", "rank"],
#     sort_by='rank'
# ).df
# CoverageVisualizer.build_info_table(
#     df=top_50_fact_df,
#     title='Топ 50 покрытых тестами API методов'
# )
#
# # untested API Methods from top table
# untested_from_top_50_df = PData(
#     data=untested_used_methods,
#     columns=["api_method", "rank"],
#     sort_by='rank'
# ).df
# CoverageVisualizer.build_info_table(
#     df=untested_from_top_50_df,
#     title='Перечень не покрытых тестами API методов'
# )
#
# # stat for top tested API methods barh
# stats_for_tested_from_top_df = PData(
#     data=coverage_visualizer.get_fact_stat(tested_15_from_top),
#     columns=["api_method", "skipped", "broken", "passed", "failed", "rank"],
#     sort_by='rank'
# ).df
# barh_stats_for_tested_from_top = CoverageVisualizer.build_info_barh_on_code_coverage(
#     df=stats_for_tested_from_top_df,
#     title='Структура прогона тестов на самые популярные API методы',
#     xlabel='Количество вызовов в тестах',
#     ylabel="Методы API",
#     x="api_method",
#     y=["broken", "skipped", "passed", "failed"])
#
# # diagramm for untested \ tested
# all_untested = coverage_visualizer.get_untested_used_api_methods()
# all_tested = coverage_visualizer.get_tested_api_methods()
# gist = CoverageVisualizer.build_info_gist_on_code_coverage(
#     values=[len(all_tested), len(all_untested)],
#     labels=["Покрыто", "Не Покрыто"],
#     title='Диаграмма покрытия API тестами'
# )
