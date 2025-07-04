
import logging
from functools import wraps
import user_interface as ui  # Импорт модуля с функцией для отображения ошибок пользователю

# Настройка логгера для записи ошибок в файл "errors.log"
logging.basicConfig(
    filename="errors.log",       # Имя файла для логов
    level=logging.ERROR,          # Записывать только ошибки и более критичные события
    format="%(asctime)s | %(levelname)s | %(message)s",  # Формат записи: время | уровень | сообщение
    encoding='utf-8'             # Кодировка файла для корректного отображения русских символов
)

def log_error(display=True):
    """
    Декоратор для оборачивания функций с целью отлова исключений (ошибок) и их логирования.

    :param display: Если True, при возникновении ошибки она будет показана пользователю через UI.
                    Если False, ошибка просто залогируется, но не показывается.
    :return: Обёртка, которая ловит исключения, логирует и при необходимости отображает ошибку.
    
    Использование:
    @log_error(display=True)
    def some_function(...):
        ...
    """
    def decorator(func):
        @wraps(func)  # Сохраняет имя и докстринги оригинальной функции
        def wrapper(*args, **kwargs):
            try:
                # Выполнение обернутой функции
                return func(*args, **kwargs)
            except Exception as e:
                # Если произошла ошибка — логируем с полной трассировкой
                logging.exception(e)

                # Если нужно — показываем ошибку пользователю через UI
                if display:
                    ui.show_error(f"Ошибка: {e}")

                # Функция при ошибке возвращает None (по умолчанию),
                # можно изменить логику при необходимости
        return wrapper
    return decorator
    
