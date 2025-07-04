from prettytable import PrettyTable

def main_menu() -> int:
    """
    Отображает главное меню и возвращает выбор пользователя в виде целого числа.
    Пользователь должен выбрать один из пунктов меню (0–4).
    """
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
    """
    Запрашивает у пользователя ввод названия фильма или его части.
    Возвращает строку без пробелов по краям.
    """
    return input('Введите название фильма или его часть: ').strip()


def choose_genre(genres: list[str]) -> str:
    """
    Отображает список жанров и предлагает пользователю выбрать один из них по номеру.
    Возвращает строку — выбранный жанр.
    """
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
    """
    Запрашивает у пользователя ввод диапазона годов (от min_year до max_year).
    Возвращает кортеж из двух целых чисел (начальный и конечный год).
    """
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
    """
    Ожидает нажатие клавиши Enter от пользователя.
    Используется как пауза между действиями.
    """
    input(message)


def print_table_data(data: list[tuple], fields: list[str] = None) -> None:
    """
    Форматирует и выводит данные в виде таблицы с помощью библиотеки PrettyTable.

    :param data: Список кортежей с данными для строк таблицы
    :param fields: (опционально) список названий столбцов
    """
    if not data:
        print("Нет результатов.")
        return

    table = PrettyTable()
    if fields:
        table.field_names = fields
    else:
        # Если имена полей не заданы, генерируем по количеству колонок в первой строке
        table.field_names = [f"Колонка {i+1}" for i in range(len(data[0]))]

    for row in data:
        table.add_row(row)

    print(table)
    
