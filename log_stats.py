from pymongo import MongoClient
from collections import Counter
import settings

client = MongoClient(settings.mongo_config['uri'])
db = client[settings.mongo_config['db']]
collection = db[settings.mongo_config['collection']]

def get_recent_unique_queries(limit: int = 5) -> list[dict]:
    """
    Возвращает последние N уникальных запросов (по параметрам запроса).
    """
    cursor = collection.find().sort("timestamp", -1)
    seen = set()
    unique_queries = []

    for entry in cursor:
        key = str(entry.get("params", {}))
        if key not in seen:
            seen.add(key)
            unique_queries.append(entry)
        if len(unique_queries) >= limit:
            break

    return unique_queries

def get_most_popular_queries(limit: int = 5) -> list[tuple[str, int]]:
    """
    Возвращает top-N популярных запросов по частоте (по 'params').
    """
    cursor = collection.find()
    queries = [str(entry.get("params", {})) for entry in cursor]
    counter = Counter(queries)
    return counter.most_common(limit)