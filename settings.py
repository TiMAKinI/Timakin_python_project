# Конфигурационные данные для подключения к базам данных

# Настройки подключения к базе MySQL
# Здесь хранятся данные для подключения к учебной базе данных Sakila
# Используется для поиска информации о фильмах

database_mysql = {
    'host': 'ich-db.edu.itcareerhub.de',  # Адрес сервера базы данных
    'user': 'ich1',                       # Имя пользователя
    'password': 'password',              # Пароль
    'database': 'sakila',                # Имя базы данных
    'charset': 'utf8mb4'                 # Кодировка для поддержки Юникода
}

# Настройки подключения к MongoDB
# Используется для логирования поисковых запросов
# Включает URI подключения и параметры доступа к коллекции логов
mongo_config = {
    "uri": "mongodb://ich_editor:verystrongpassword"
           "@mongo.itcareerhub.de/?readPreference=primary"
           "&ssl=false&authMechanism=DEFAULT&authSource=ich_edit",
    "db": "ich_edit",  # Название базы данных MongoDB
    "collection": "final_project_100125_Ilia_Timakin"  # Коллекция для логов
}
