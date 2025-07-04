from log_writer import log_search
from mysql_connector import (
    search_by_keyword,
    search_by_genre_and_year_range,
    get_all_genres,
    get_min_max_years
)
from log_stats import get_recent_unique_queries, get_most_popular_queries
from error_utils import log_error

# Обернутый безопасный вызов логгера поиска с отловом ошибок
@log_error(display=True)
def safe_log_search(*args, **kwargs):
    """
    Безопасная обертка для функции логирования поисковых запросов.
    При возникновении исключения — выводит сообщение об ошибке и пишет в лог.

    :param args: позиционные аргументы, передаваемые в log_search
    :param kwargs: именованные аргументы для log_search
    """
    log_search(*args, **kwargs)

# Безопасный вызов поиска по ключевому слову
@log_error(display=True)
def safe_search_by_keyword(keyword, offset=0):
    """
    Безопасная обертка для поиска фильмов по ключевому слову (в названии).
    Возвращает до 10 фильмов, начиная с указанного смещения.

    :param keyword: ключевое слово для поиска (например, 'Matrix')
    :param offset: смещение для пагинации (по умолчанию 0)
    :return: список кортежей с данными о фильмах (title, release_year, description)
    """
    return search_by_keyword(keyword, offset)

# Безопасный вызов поиска по жанру и диапазону лет
@log_error(display=True)
def safe_search_by_genre_and_year_range(genre, year_from, year_to, offset=0):
    """
    Безопасная обертка для поиска фильмов по жанру и диапазону лет.
    Возвращает до 10 фильмов на одной странице (offset указывает смещение).

    :param genre: название жанра (например, 'Comedy')
    :param year_from: начальный год выпуска
    :param year_to: конечный год выпуска
    :param offset: смещение для пагинации
    :return: список кортежей с данными о фильмах
    """
    return search_by_genre_and_year_range(genre, year_from, year_to, offset)

# Безопасный вызов получения всех жанров
@log_error(display=True)
def safe_get_all_genres():
    """
    Безопасная обертка для получения списка всех жанров из базы данных.

    :return: список строк с названиями жанров
    """
    return get_all_genres()

# Безопасный вызов получения минимального и максимального года
@log_error(display=True)
def safe_get_min_max_years():
    """
    Безопасная обертка для получения диапазона лет (min и max) фильмов в базе.

    :return: кортеж (min_year, max_year)
    """
    return get_min_max_years()

# Безопасный вызов получения последних уникальных запросов
@log_error(display=True)
def safe_get_recent_unique_queries():
    """
    Безопасная обертка для получения последних уникальных поисковых запросов из MongoDB.

    :return: список словарей с параметрами последних уникальных запросов
    """
    return get_recent_unique_queries()

# Безопасный вызов получения популярных запросов
@log_error(display=True)
def safe_get_most_popular_queries():
    """
    Безопасная обертка для получения списка самых популярных запросов из MongoDB.

    :return: список кортежей вида ("параметры", количество повторений)
    """
    return get_most_popular_queries()
