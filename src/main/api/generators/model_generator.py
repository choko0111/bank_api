import datetime
import uuid
from typing import Any, get_type_hints, get_origin, Annotated, get_args
from src.main.api.generators.creation_rule import CreationRule
import random
from datetime import datetime, timedelta
import rstr

class RandomModelGenerator:
    @staticmethod
    def generate(cls: type) -> Any:  # Метод для генерации случайного экземпляра переданного класса
        type_hints = get_type_hints(cls, include_extras=True)  # Получаем аннотации типов всех полей класса, включая Annotated
        init_data = {}  # Словарь для хранения сгенерированных значений полей

        for field_name, annotated_type in type_hints.items():  # Проходим по каждому полю класса
            rule = None  # Изначально правило генерации отсутствует
            actual_type = annotated_type  # По умолчанию реальный тип поля — это аннотированный тип

            if get_origin(annotated_type) is Annotated:  # Если поле обёрнуто в Annotated
                actual_type, *annotations = get_args(annotated_type)  # Разбираем Annotated на реальный тип и аннотации
                for ann in annotations:  # Проходим по всем аннотациям
                    if isinstance(ann, CreationRule):  # Ищем аннотацию типа CreationRule
                        rule = ann  # Сохраняем найденное правило для генерации

            if rule:  # Если найдено правило генерации через CreationRule
                value = RandomModelGenerator._generate_from_regex(rule.regex, actual_type)  # Генерируем значение по regex
            else:  # Если правила нет
                value = RandomModelGenerator._generate_value(actual_type)  # Генерируем значение по типу поля

            init_data[field_name] = value  # Добавляем сгенерированное значение в словарь

        return cls(**init_data)  # Создаём и возвращаем экземпляр класса с сгенерированными данными

    @staticmethod
    def _generate_from_regex(regex: str, field_type) -> Any:  # Генерация значения из регулярного выражения
        generated = rstr.xeger(regex)  # Используем rstr для генерации строки по regex
        if field_type is int:  # Если поле int
            return int(generated)  # Преобразуем строку в int
        if field_type is float:  # Если поле float
            return float(generated)  # Преобразуем строку в float
        return generated  # Иначе возвращаем строку

    @staticmethod
    def _generate_value(field_type: type) -> Any:  # Генерация случайного значения по типу поля
        if field_type is str:  # Если строка
            return str(uuid.uuid4())[:8]  # Генерируем случайную 8-символьную строку
        elif field_type is int:  # Если int
            return random.randint(0,1000)  # Генерируем случайное число от 0 до 1000
        elif field_type is float:  # Если float
            return round(random.uniform(0, 100.0), 2)  # Генерируем случайное число с плавающей точкой от 0 до 100
        elif field_type is bool:  # Если bool
            return random.choice([True, False])  # Генерируем случайное True или False
        elif field_type is datetime:  # Если datetime
            return datetime.now() - timedelta(seconds=random.randint(0, 100000))  # Случайная дата в прошлом
        elif field_type is list:  # Если список
            return [str(uuid.uuid4())[:5]]  # Создаём список с одной случайной строкой длиной 5
        elif isinstance(field_type, type):  # Если поле — другой пользовательский класс
            return RandomModelGenerator.generate(field_type)  # Рекурсивно генерируем экземпляр этого класса
        return None  # Если ничего не подошло, возвращаем None
