import pymysql
from typing import List, Tuple
import settings


def get_mysql_connection():
    """Создает и возвращает подключение к MySQL."""
    return pymysql.connect(
        host=settings.database_mysql['host'],
        user=settings.database_mysql['user'],
        password=settings.database_mysql['password'],
        database=settings.database_mysql['database'],
        charset=settings.database_mysql['charset'],
        cursorclass=pymysql.cursors.Cursor
    )


def search_by_keyword(keyword: str, offset: int = 0, limit: int = 10) -> List[Tuple]:
    """Ищет фильмы по ключевому слову (в названии)."""
    query = """
    SELECT title, release_year, description
    FROM film
    WHERE title LIKE %s
    ORDER BY title
    LIMIT %s OFFSET %s
    """
    params = (f"%{keyword}%", limit, offset)

    with get_mysql_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()


def get_all_genres() -> List[str]:
    """Возвращает список всех жанров."""
    query = "SELECT name FROM category ORDER BY name"

    with get_mysql_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]


def get_min_max_years() -> Tuple[int, int]:
    """Возвращает минимальный и максимальный год выпуска фильмов."""
    query = "SELECT MIN(release_year), MAX(release_year) FROM film"

    with get_mysql_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()


def search_by_genre_and_year_range(genre: str, year_from: int, year_to: int, offset: int = 0, limit: int = 10) -> List[Tuple]:
    """Ищет фильмы по жанру и диапазону годов."""
    query = """
    SELECT f.title, f.release_year, f.description
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s AND f.release_year BETWEEN %s AND %s
    ORDER BY f.title
    LIMIT %s OFFSET %s
    """
    params = (genre, year_from, year_to, limit, offset)

    with get_mysql_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()