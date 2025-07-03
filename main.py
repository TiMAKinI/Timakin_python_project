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
    keyword = ui.input_film_name()
    offset = 0
    all_results = []

    while True:
        try:
            results = search_by_keyword(keyword, offset=offset)
        except Exception as e:
            print(f"Ошибка при запросе к базе данных: {e}")
            break

        if not results:
            if offset == 0:
                print(" Фильмы не найдены.")
            break

        ui.print_table_data(results)
        all_results.extend(results)
        offset += 10

        next_page = input("Показать ещё 10? (нажмите Enter или 'n' для выхода): ").strip().lower()
        if next_page == 'n':
            break

    try:
        log_search(
            search_query=keyword,
            search_type="keyword",
            params={"keyword": keyword},
            results_count=len(all_results)
        )
    except Exception as e:
        print(f" Ошибка при сохранении лога: {e}")


def search_by_genre_flow():
    try:
        genres = get_all_genres()
        min_year, max_year = get_min_max_years()
    except Exception as e:
        print(f"Ошибка при получении данных из базы: {e}")
        return

    genre = ui.choose_genre(genres)
    year_from, year_to = ui.input_year_range(min_year, max_year)

    offset = 0
    all_results = []

    while True:
        try:
            results = search_by_genre_and_year_range(genre, year_from, year_to, offset=offset)
        except Exception as e:
            print(f"Ошибка при запросе к базе данных: {e}")
            break

        if not results:
            if offset == 0:
                print(" Фильмы не найдены.")
            break

        ui.print_table_data(results)
        all_results.extend(results)
        offset += 10

        next_page = input("Показать ещё 10? (нажмите Enter или 'n' для выхода): ").strip().lower()
        if next_page == 'n':
            break

    try:
        log_search(
            search_query=f"{genre}, {year_from}-{year_to}",
            search_type="genre_year_range",
            params={"genre": genre, "year_from": year_from, "year_to": year_to},
            results_count=len(all_results)
        )
    except Exception as e:
        print(f" Ошибка при сохранении лога: {e}")


def show_popular_queries():
    try:
        print("\n Топ-5 популярных запросов:")
        popular = get_most_popular_queries()
        for item, count in popular:
            print(f" {item} → {count} раз")
    except Exception as e:
        print(f"Ошибка при получении популярных запросов: {e}")


def show_recent_queries():
    try:
        print("\n Последние уникальные запросы:")
        recent = get_recent_unique_queries()
        for entry in recent:
            ts = entry.get("timestamp")
            params = entry.get("params")
            print(f" {ts} |  {params}")
    except Exception as e:
        print(f"Ошибка при получении последних запросов: {e}")


def main():
    while True:
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
            print("\n Выход из приложения. До свидания!")
            break
        else:
            print(" Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()