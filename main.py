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
top_50_expected_sorted_by_freq_df = PData(
    data=top_50_expected_sorted_by_freq,
    columns=["api_method", "frequency"],
    sort_by='frequency'
).df
CoverageVisualize.build_info_table(
    df=top_50_expected_sorted_by_freq_df,
    title='Топ 50 используемых API методов, отсортированных по частоте'
)

# Топ 50 используемых API методов, отсортированных по критичности
top_50_expected_sorted_by_crit = coverage_analyzer.get_top_n_api_methods(
    data_set=expected_data_set,
    top_n=50,
    sort_by='criticality'
)
top_50_expected_sorted_by_crit_df = PData(
    data=top_50_expected_sorted_by_crit,
    columns=["api_method", "criticality"],
    sort_by='criticality'
).df
CoverageVisualize.build_info_table(
    df=top_50_expected_sorted_by_crit_df,
    title='Топ 50 используемых API методов, отсортированных по критичности'
)

# Протестированные API методы, отсортированные по частоте
fact_sorted_by_freq = coverage_analyzer.get_top_n_api_methods(
    data_set=fact_data_set
)
fact_sorted_by_freq_df = PData(
    data=fact_sorted_by_freq,
    columns=["api_method", "skipped", "broken", "passed", "failed", "frequency"],
    sort_by='frequency'
).df
CoverageVisualize.build_info_table(
    df=fact_sorted_by_freq_df,
    title='Протестированные API методы, отсортированные по частоте'
)

# Протестированные API методы, отсортированные по критичности
fact_sorted_by_crit = coverage_analyzer.get_top_n_api_methods(
    data_set=fact_data_set,
    sort_by='criticality'
)
fact_sorted_by_crit_df = PData(
    data=fact_sorted_by_crit,
    columns=["api_method", "skipped", "broken", "passed", "failed", "criticality"],
    sort_by='criticality'
).df
CoverageVisualize.build_info_table(
    df=fact_sorted_by_crit_df,
    title='Протестированные API методы, отсортированные по критичности'
)

# Не покрытые тестами query параметры из Топ 50 критичных используемых методов
untested_queries_from_top_50_expected = coverage_analyzer.get_untested_query_params(
    expected_result_lst=top_50_expected_sorted_by_crit,
    fact_result_lst=fact_sorted_by_crit
)
untested_queries_from_top_50_expected_df = PData(
    data=untested_queries_from_top_50_expected,
    columns=["api_method", "query_list", "criticality"],
    sort_by='criticality'
).df
CoverageVisualize.build_info_table(
    df=untested_queries_from_top_50_expected_df,
    title='Не покрытые тестами query параметры из Топ 50 критичных используемых методов'
)

# Не покрытые тестами status codes из Топ 50 критичных используемых методов
untested_codes_from_top_50_expected = coverage_analyzer.get_untested_status_codes_params(
    expected_result_lst=top_50_expected_sorted_by_crit,
    fact_result_lst=fact_sorted_by_crit
)
untested_codes_from_top_50_expected_df = PData(
    data=untested_codes_from_top_50_expected,
    columns=["api_method", "status_codes", "criticality"],
    sort_by='criticality'
).df
CoverageVisualize.build_info_table(
    df=untested_codes_from_top_50_expected_df,
    title='Не покрытые тестами status codes из Топ 50 критичных используемых методов'
)

# Не протестированные критичные API методы из ТОП 50
untested_from_top_50_api_methods_crit = coverage_analyzer.get_untested_used_api_methods(
    expected_result_lst=top_50_expected_sorted_by_crit
)
untested_from_top_50_api_methods_crit_df = PData(
    data=untested_from_top_50_api_methods_crit,
    columns=["api_method", "criticality"],
    sort_by='criticality'
).df
CoverageVisualize.build_info_table(
    df=untested_from_top_50_api_methods_crit_df,
    title='Не протестированные критичные API методы из ТОП 50'
)

# Не протестированные частые API методы из ТОП 50
untested_from_top_50_api_methods_freq = coverage_analyzer.get_untested_used_api_methods(
    expected_result_lst=top_50_expected_sorted_by_freq
)
untested_from_top_50_api_methods_freq_df = PData(
    data=untested_from_top_50_api_methods_freq,
    columns=["api_method", "frequency"],
    sort_by='frequency'
).df
CoverageVisualize.build_info_table(
    df=untested_from_top_50_api_methods_freq_df,
    title='Не протестированные частые API методы из ТОП 50'
)

# Структура прогона тестов на самые популярные API методы
top_15_fact_stat = coverage_analyzer.get_fact_stat(
    expected_result_lst=coverage_analyzer.get_top_n_api_methods(fact_data_set, 15)
)
stats_for_tested_from_top_df = PData(
    data=coverage_analyzer.get_fact_stat(top_15_fact_stat),
    columns=["api_method", "skipped", "broken", "passed", "failed", "frequency"],
    sort_by='frequency'
).df
barh_stats_for_tested_from_top = CoverageVisualize.build_info_barh_on_code_coverage(
    df=stats_for_tested_from_top_df,
    title='Структура прогона тестов на самые популярные API методы',
    xlabel='Количество вызовов в тестах',
    ylabel="Методы API",
    x="api_method",
    y=["broken", "skipped", "passed", "failed"])


# Диаграмма покрытия API тестами
all_untested = coverage_analyzer.get_untested_used_api_methods()
all_tested = coverage_analyzer.get_tested_api_methods()
gist = CoverageVisualize.build_info_gist_on_code_coverage(
    values=[len(all_tested), len(all_untested)],
    labels=["Покрыто", "Не Покрыто"],
    title='Диаграмма покрытия API тестами'
)
