
    # log_writer.py

import settings
from pymongo import MongoClient
from datetime import datetime

# Инициализация клиента и коллекции MongoDB
_client = MongoClient(settings.mongo_config['uri'])
_db = _client[settings.mongo_config['db']]
_collection = _db[settings.mongo_config['collection']]


def log_search(query: str, search_type: str, count: int) -> None:
    """
    Сохраняет в MongoDB информацию о поисковом запросе.

    :param query: строка поискового запроса (например, 'matrix' или 'Comedy, 2005–2010')
    :param search_type: тип запроса ('keyword' или 'genre_year_range')
    :param count: количество результатов, найденных по запросу
    """
    record = {
        'timestamp': datetime.utcnow(),
        'query': query,
        'type': search_type,
        'results_count': count
    }

    _collection.insert_one(record)