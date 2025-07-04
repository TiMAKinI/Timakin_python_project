import settings
from pymongo import MongoClient
from datetime import datetime

# Создаем подключение к MongoDB с использованием конфигурации из settings
_client = MongoClient(settings.mongo_config['uri'])
_db = _client[settings.mongo_config['db']]
_collection = _db[settings.mongo_config['collection']]

def log_search(search_query: str, search_type: str, params: dict, results_count: int) -> None:
    """
    Сохраняет информацию о выполненном поисковом запросе в базу данных MongoDB.

    :param search_query: Описание запроса (например, строка поиска или 'Comedy, 2005–2010')
    :param search_type: Тип запроса ('keyword' — по ключевому слову, 'genre_year_range' — по жанру и году)
    :param params: Параметры запроса (словарь с данными запроса)
    :param results_count: Количество найденных результатов

    Пример документа, сохраняемого в MongoDB:
    {
        'timestamp': datetime.datetime(2025, 7, 3, 12, 0),
        'search_type': 'keyword',
        'params': {'keyword': 'Matrix'},
        'results_count': 5
    }
    """
    record = {
        'timestamp': datetime.utcnow(),  # Время запроса (UTC)
        'search_type': search_type,
        'params': params,
        'results_count': results_count
    }
    _collection.insert_one(record)  # Сохраняем запись в MongoDB