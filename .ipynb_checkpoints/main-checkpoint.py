# main.py

from mysql_connector import (
    search_by_keyword,
    search_by_genre_and_year_range,
    get_all_genres,
    get_min_max_years
)
from log_writer import log_search
from log_stats import get_recent_unique_queries, get_most_popular_queries
import user_interface as ui


def search_by_title_flow():
    """Обрабатывает поиск по названию фильма."""
    keyword = ui.film_name()
    offset = 0
    all_results = []

    while True:
        results = search_by_keyword(keyword, offset=offset)
        if not results:
            if offset == 0:
                print("Фильмы не найдены.")
            break

        ui.print_table_data(results)
        all_results.extend(results)
        offset += 10

        next_page = input("Показать ещё 10? (нажмите Enter или 'n' для выхода): ").strip().lower()
        if next_page == 'n':
            break

    # логирование
    log_search(query=keyword, search_type="keyword", params={"keyword": keyword}, count=len(all_results))


def search_by_genre_flow():
    """Обрабатывает поиск по жанру и диапазону лет."""
    genres = get_all_genres()
    min_year, max_year = get_min_max_years()
    
    print(f"Доступные жанры:")
    genre = ui.choose_genre(genres)
    print(f"Допустимый диапазон лет: {min_year} - {max_year}")
    
    year_from, year_to = ui.genre_and_year_of_release()
    offset = 0
    all_results = []

    while True:
        results = search_by_genre_and_year_range(genre, year_from, year_to, offset=offset)
        if not results:
            if offset == 0:
                print("Фильмы не найдены.")
            break

        ui.print_table_data(results)
        all_results.extend(results)
        offset += 10

        next_page = input("Показать ещё 10? (нажмите Enter или 'n' для выхода): ").strip().lower()
        if next_page == 'n':
            break

    # логирование
    log_search(
        query=f"{genre}, {year_from}-{year_to}",
        search_type="genre_year",
        params={"genre": genre, "year_from": year_from, "year_to": year_to},
        count=len(all_results)
    )


def show_popular_queries():
    print("\nТоп популярных запросов:")
    popular = get_most_popular_queries()
    for item, count in popular:
        print(f"{item} → {count} раз")


def show_recent_queries():
    print("\nПоследние уникальные запросы:")
    recent = get_recent_unique_queries()
    for entry in recent:
        ts = entry.get("timestamp")
        params = entry.get("params")
        print(f"{ts} | {params}")


def main():
    while True:
        try:
            choice = ui.main_menu()

            if choice == 1:
                search_by_title_flow()
            elif choice == 2:
                search_by_genre_flow()
            elif choice == 3:
                show_popular_queries()
            elif choice == 4:
                show_recent_queries()
            elif choice == 0:
                print("Выход из приложения. До свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()