Данный проект создан как демонстрация возможного варианта автоматизации визуализации тестового покрытия API на практике.

## Глоссарий
Фактический результат (ФР/FR) - методы API, покрытые авто-тестами  
Ожидаемый результат (ОР/ER) - реально используемые методы API

---
## Структура

`- ./fact_expected_data_examples` - Содержит архивы с примерами файлов для ОР и ФР  
`- ./src`  
`-- ./src/analisys`  
`--- ./src/analisys/coverage_analisys.py` - модуль абстракции CoverageAnalisys, необходимого для формирования результирующего массива информации о API методах  
`-- ./src/data_parser`  
`--- ./src/data_parser/data_frame.py` - модуль абстракции DataFrame, необходимой для сохранения информации об API методе  
`--- ./src/data_parser/data_parser.py` - модуль абстракции DataParser, необходимой для обработки файлов, содержащих информацию об ОР и ФР  
`--- ./src/data_parser/data_set.py` - модуль абстракции DataSet, необходимой для объединения группы инстансов DataFrame в единый массив информации об ОР и ФР  
`-- ./src/utils`  
`--- ./src/utils/logger.py` - модуль абстракции Logger, необходимой для логгирования  
`-- ./src/visualize`  
`--- ./src/visualize/coverage_cisualize.py` - модуль абстракции CoverageVisualize, необходимой для построения таблиц, гистграмм и диаграмм  
`--- ./src/visualize/pdata.py` - модуль абстракции PData, необходимой для конвертации массивов DataFrame в инстансы датафреймов библиотеки pandas  
`./config.py` - содержит пример конфигурации запроса в ELK для получения ожидаемого результата анализа API методов  
`./main.py` - содержит перечень получаемых результирующих массивов данных, и способы их визуализации

---
## Пример использования
1. Установить зависимости `pip install -r requirements.txt`
2. Создать директорию `./pandas_results`. 
3. Распаковать содержимое архива `./fact_expected_data_examples/expected_data.rar` в директорию `./data/expected_data`
4. Распаковать содержимое архива `./fact_expected_data_examples/fact_data.rar` в директорию `./data/fact_data`
5. Запустить `./main.py`
6. В директории `./pandas_results` появятся результаты отработки скрипта
7. Возникшие ошибки будут залоггированы в `./log.txt`

---
## Описание примеров expected_data
- хранятся в `./data/expected_data`
- шаблон нейминга: `UUID4_expected_log.json`
- содержат инфомрацию об ОР - тех методах API, которые вызываются клиентом на проде

---
## Описание примеров fact_data
- хранятся в `./data/fact_data`
- шаблон нейминга: `UUID4_log_fact_result.json` -> содержат информацию по формату файла allure_reports о выполнении теста с прикрепленными файлами логами `UUID4_attachment.txt`
- шаблон нейминга: `UUID4_attachment.txt` -> файлы, на которые содержатся ссылки в `UUID4_log_fact_result.json`
- шаблон нейминга: `UUID4_step_fact_result.json` -> содержат информацию по формату файла allure_reports о выполнении теста с информацией о вызовах API методов в описании шага теста
