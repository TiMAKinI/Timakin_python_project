from pymongo import MongoClient
from collections import Counter
import settings

# Создаем подключение к MongoDB с использованием конфигурации из settings
client = MongoClient(settings.mongo_config['uri'])
db = client[settings.mongo_config['db']]
collection = db[settings.mongo_config['collection']]

def get_recent_unique_queries(limit: int = 5) -> list[dict]:
    """
    Возвращает список из последних уникальных поисковых запросов, сохранённых в MongoDB.

    Уникальность определяется по параметрам запроса (params).
    Записи сортируются по времени (timestamp) в порядке убывания.

    :param limit: Максимальное количество уникальных запросов (по умолчанию — 5)
    :return: Список словарей, каждый из которых содержит:
             - timestamp (время запроса)
             - search_type (тип запроса)
             - params (использованные параметры)
             - results_count (кол-во результатов по запросу)

    Пример:
    [
        {
            'timestamp': ..., 
            'search_type': 'keyword',
            'params': {'keyword': 'Matrix'},
            'results_count': 5
        },
        ...
    ]
    """
    cursor = collection.find().sort("timestamp", -1)  # Сортировка по времени запроса (от новых к старым)
    seen = set()  # Множество для отслеживания уже добавленных параметров
    unique_queries = []

    for entry in cursor:
        key = str(entry.get("params", {}))  # Преобразуем параметры запроса в строку для сравнения
        if key not in seen:
            seen.add(key)
            unique_queries.append(entry)
        if len(unique_queries) >= limit:
            break

    return unique_queries

def get_most_popular_queries(limit: int = 5) -> list[tuple[str, int]]:
    """
    Возвращает список самых популярных запросов на основе частоты их выполнения.

    Популярность запроса определяется количеством вхождений одинаковых параметров (params) в базе.

    :param limit: Сколько самых популярных запросов вернуть (по умолчанию — 5)
    :return: Список кортежей вида ("строка с параметрами запроса", количество повторений)

    Пример:
    [
        ("{'keyword': 'Matrix'}", 3),
        ("{'genre': 'Action', 'year_from': 2000, 'year_to': 2005}", 2)
    ]
    """
    cursor = collection.find()
    queries = [str(entry.get("params", {})) for entry in cursor]  # Собираем все параметры запросов в строковом виде
    counter = Counter(queries)  # Подсчитываем количество каждого уникального запроса
    return counter.most_common(limit)  # Возвращаем top-N популярных
    