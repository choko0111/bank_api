from typing import Any, Dict, List  # Импорт универсального типа Any, словаря и списка
from dataclasses import dataclass  # Импорт декоратора для простого класса с данными


@dataclass
class Mismatch:
    field_name: str  # Название поля, где обнаружено несоответствие
    expected: Any  # Ожидаемое значение
    actual: Any  # Фактическое значение


class ComparisonResult:
    def __init__(self, mismatches: List[Mismatch]):
        self._mismatches = mismatches  # Сохраняем список найденных несоответствий

    def is_success(self) -> bool:
        return not self.mismatches  # Возвращает True, если список несоответствий пуст (успешное сравнение)

    @property
    def mismatches(self) -> List[Mismatch]:
        return self._mismatches  # Позволяет получить список несоответствий извне


class ModelComparator:
    @staticmethod
    def compare_fields(
            request: Any,  # Объект запроса
            response: Any,  # Объект ответа
            field_mapping: Dict[str, str]  # Словарь отображений полей request -> response
    ):
        mismatches = []  # Инициализация списка для хранения найденных несоответствий
        for request_field, response_field in field_mapping.items():  # Итерируем пары полей
            request_value = ModelComparator.get_field_value(request, request_field)  # Получаем значение поля из запроса
            response_value = ModelComparator.get_field_value(response, response_field)  # Получаем значение поля из ответа

            if str(request_value) != str(response_value):  # Сравниваем значения (строковое сравнение для универсальности)
                mismatches.append(Mismatch(f'{request_field} -> {response_field}', request_value, response_value))  # Добавляем несоответствие в список

        return ComparisonResult(mismatches)  # Возвращаем объект с результатами сравнения

    @staticmethod
    def get_field_value(obj: Any, field_name: str):
        current_class = obj.__class__  # Начинаем с класса объекта

        while current_class:  # Поднимаемся по иерархии наследования
            if hasattr(obj, field_name):  # Проверяем, есть ли нужное поле
                return getattr(obj, field_name)  # Возвращаем значение поля
            current_class = current_class.__base__  # Переходим к родительскому классу

        raise AttributeError(f'Field {field_name} not found in class {obj.__class__.__name__}')  # Если поле не найдено, выбрасываем ошибку
