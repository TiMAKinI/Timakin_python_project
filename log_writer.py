import settings
from pymongo import MongoClient
from datetime import datetime

_client = MongoClient(settings.mongo_config['uri'])
_db = _client[settings.mongo_config['db']]
_collection = _db[settings.mongo_config['collection']]

def log_search(search_query: str, search_type: str, params: dict, results_count: int) -> None:
    """
    Сохраняет в MongoDB информацию о поисковом запросе.

    :param search_query: описание запроса (например, строка поиска или 'Comedy, 2005–2010')
    :param search_type: тип запроса ('keyword' или 'genre_year_range')
    :param params: словарь параметров запроса (например, {'keyword': 'matrix'})
    :param results_count: сколько результатов вернул запрос
    """
    record = {
        'timestamp': datetime.utcnow(),
        'search_type': search_type,
        'params': params,
        'results_count': results_count
    }
    _collection.insert_one(record)