def main_menu() -> int:
    prompt = """
    Меню:
    1. Поиск фильма по названию
    2. Поиск по жанру и диапазону годов выпуска
    3. Показать популярные запросы
    4. Показать последние запросы
    0. ВЫХОД

    Выберите пункт меню (0–4): 
    """
    while True:
        try:
            choice = int(input(prompt))
            if choice in range(0, 5):
                return choice
            print("Введите число от 0 до 4.")
        except ValueError:
            print("Ошибка: нужно ввести число.")


def input_film_name() -> str:
    return input('Введите название фильма или его часть: ').strip()


def choose_genre(genres: list[str]) -> str:
    print("\nДоступные жанры:")
    for idx, name in enumerate(genres, start=1):
        print(f"{idx}. {name}")
    while True:
        try:
            choice = int(input("Введите номер жанра: "))
            if 1 <= choice <= len(genres):
                return genres[choice - 1]
            print(f"Введите число от 1 до {len(genres)}.")
        except ValueError:
            print("Ошибка: нужно ввести число.")


def input_year_range(min_year: int, max_year: int) -> tuple[int, int]:
    print(f"\nВведите диапазон годов выпуска (от {min_year} до {max_year})")
    while True:
        try:
            year_from = int(input("Год от: "))
            year_to = int(input("Год до: "))
            if min_year <= year_from <= max_year and min_year <= year_to <= max_year and year_from <= year_to:
                return year_from, year_to
            else:
                print(f"Введите корректный диапазон от {min_year} до {max_year}.")
        except ValueError:
            print("Ошибка: нужно ввести число.")


def wait_for_input(message: str = "Нажмите Enter для продолжения...") -> None:
    input(message)


def print_table_data(data: list[tuple]) -> None:
    if not data:
        print("Нет результатов.")
        return
    for items in data:
        print(' | '.join(map(str, items)))
    print("-" * 40)