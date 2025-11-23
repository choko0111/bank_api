import os  # Работа с операционной системой, проверка существования файлов
import configparser  # Работа с конфигурационными ini-файлами
from pathlib import Path  # Удобная работа с путями файлов
from typing import List, Dict, Type, Optional  # Аннотации типов


# Разделяем: ключ - поле из request, значение - поле из response
class ComparisonRule:
    def __init__(self, response_class_name: str, field_pairs: List[str]):
        self._response_class_name = response_class_name  # Название класса response, с которым будем сравнивать
        self.field_pairs = field_pairs  # Список пар "request_field=response_field"
        self._field_mapping: Dict[str, str] = {}  # Словарь для быстрого доступа к парам полей

        for pair in field_pairs:  # Итерируем пары
            parts = pair.split('=')  # Разделяем по знаку '='
            if len(parts) == 2:  # Если есть и request, и response
                self._field_mapping[parts[0].strip()] = parts[1].strip()  # Добавляем в словарь с обрезкой пробелов
            else:
                self._field_mapping[pair.strip()] = pair.strip()  # Если '=' нет, используем одно и то же имя для обоих полей

    @property
    def response_class_name(self) -> str:
        return self._response_class_name  # Возвращает имя класса response

    @property
    def field_mapping(self) -> Dict[str, str]:
        return self._field_mapping.copy()  # Возвращает копию словаря полей, чтобы его нельзя было изменить извне


# Класс для загрузки правил сравнения из конфигурации
class ModelComparisonConfigLoader:
    def __init__(self, comparison: str):
        self.rules: Dict[str, ComparisonRule] = {}  # Словарь request_class_name -> ComparisonRule
        self._load_config(comparison)  # Загружаем конфигурацию при создании объекта

    def _load_config(self, comparison: str):
        # Формируем путь к файлу конфигурации (resources/model_comparison.properties)
        path = Path(__file__).parents[5] / 'resources' / f'{comparison}'

        if not os.path.exists(path):  # Проверяем, что файл существует
            raise FileNotFoundError(f'Config file not found: model_comparison.properties')

        config = configparser.ConfigParser()  # Создаем объект для чтения конфигурации
        config.optionxform = str  # Сохраняем регистр ключей (по умолчанию configparser делает их маленькими)
        config.read(path)  # Читаем файл конфигурации

        for key in config.defaults():  # Проходим по всем ключам (имена request-классов)
            value = config.defaults()[key]  # Получаем значение: "ResponseClass: field1=response1, field2=response2..."
            target = value.split(':')  # Разделяем на имя response-класса и список полей
            if len(target) != 2:  # Если формат неверный, пропускаем
                continue

            response_class = target[0].strip()  # Имя response-класса
            field_list = [field.strip() for field in target[1].split(',')]  # Список пар полей с обрезкой пробелов

            # Создаем правило сравнения и сохраняем его по ключу request-класса
            self.rules[key.strip()] = ComparisonRule(response_class, field_list)

    def get_rule_for(self, request_class: Type) -> Optional[ComparisonRule]:  # Принимаем класс запроса
        return self.rules.get(request_class.__name__)  # Возвращаем правило сравнения или None, если не найдено
