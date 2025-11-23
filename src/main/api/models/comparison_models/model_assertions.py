from typing import Any
from src.main.api.models.comparison_models.model_comparison_configuration import ModelComparisonConfigLoader
from src.main.api.models.comparison_models.model_comparator import ModelComparator


class ModelAssertions:
    def __init__(self, request: Any, response: Any):
        self.request = request  # Сохраняем объект запроса для последующего сравнения
        self.response = response  # Сохраняем объект ответа для последующего сравнения

    def match(self) -> 'ModelAssertions':
        config_loader = ModelComparisonConfigLoader('model_comparison.properties')  # Загружаем конфигурацию правил сравнения моделей из файла
        rule = config_loader.get_rule_for(type(self.request))  # Получаем правило сравнения для класса запроса

        if rule is not None:  # Проверяем, что правило существует
            result = ModelComparator.compare_fields(
                self.request,  # Передаем объект запроса
                self.response,  # Передаем объект ответа
                rule.field_mapping  # Передаем отображение полей для сравнения (request -> response)
            )
            if not result.is_success():  # Если сравнение полей прошло с ошибками
                raise AssertionError(f'Model comparison failed with mismatches fields: \n{result.mismatches}')  # Выбрасываем исключение с перечнем несовпадений
        else:  # Если правило не найдено
            raise AssertionError(f'No comparison rule found for request {self.request.__class__.__name__}')  # Выбрасываем исключение о отсутствии правила

        return self  # Возвращаем self для возможности цепочки вызовов (fluent interface)