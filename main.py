
from safe_wrappers import (
    safe_log_search,
    safe_search_by_keyword,
    safe_search_by_genre_and_year_range,
    safe_get_all_genres,
    safe_get_min_max_years,
    safe_get_recent_unique_queries,
    safe_get_most_popular_queries
)
import user_interface as ui

def search_by_title_flow():
    """
    Процедура поиска фильмов по названию. 
    Пользователь вводит ключевое слово, затем выводится таблица с результатами постранично (по 10 за раз).
    Все успешные запросы логируются в MongoDB.
    """
    keyword = ui.input_film_name()  # Получаем ключевое слово от пользователя
    offset = 0  # Смещение для пагинации
    all_results = []  # Для подсчета общего количества результатов

    while True:
        results = safe_search_by_keyword(keyword, offset=offset)
        if not results:
            if offset == 0:
                print("Фильмы не найдены.")
            break

        ui.print_table_data(results)  # Показываем таблицу с результатами
        all_results.extend(results)  # Добавляем к общему списку результатов
        offset += 10

        next_page = input("Показать ещё 10? (нажмите Enter или 'n' для выхода): ").strip().lower()
        if next_page == 'n':
            break

    # Логируем успешный поиск
    safe_log_search(
        search_query=keyword,
        search_type="keyword",
        params={"keyword": keyword},
        results_count=len(all_results)
    )

def search_by_genre_flow():
    """
    Процедура поиска фильмов по жанру и диапазону годов.
    Пользователь выбирает жанр и указывает диапазон лет, затем отображаются результаты постранично.
    Результаты логируются в MongoDB.
    """
    genres = safe_get_all_genres()
    min_year, max_year = safe_get_min_max_years()

    print(f"\n Доступные жанры:")
    genre = ui.choose_genre(genres)

    print(f"\n Диапазон лет: {min_year} — {max_year}")
    year_from, year_to = ui.input_year_range(min_year, max_year)
    offset = 0
    all_results = []

    while True:
        results = safe_search_by_genre_and_year_range(genre, year_from, year_to, offset=offset)
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

    # Логируем запрос в MongoDB
    safe_log_search(
        search_query=f"{genre}, {year_from}-{year_to}",
        search_type="genre_year_range",
        params={"genre": genre, "year_from": year_from, "year_to": year_to},
        results_count=len(all_results)
    )

def show_popular_queries():
    """
    Показывает топ-5 самых частых поисковых запросов из MongoDB.
    """
    print("\n Топ-5 популярных запросов:")
    popular = safe_get_most_popular_queries()
    for item, count in popular:
        print(f" {item} → {count} раз")

def show_recent_queries():
    """
    Показывает последние 5 уникальных поисковых запросов (по параметрам).
    Уникальность определяется по параметрам, а не строке.
    """
    print("\n Последние уникальные запросы:")
    recent = safe_get_recent_unique_queries()
    for entry in recent:
        ts = entry.get("timestamp")
        params = entry.get("params")
        print(f" {ts} |  {params}")

def main():
    """
    Точка входа в приложение. Показывает главное меню и запускает нужную процедуру.
    """
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

if __name__ == "__main__":
    main()

