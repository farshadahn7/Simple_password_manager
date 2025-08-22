from decouple import config

db_connection_data = {
    "db_name": config("DB_NAME"),
    "db_user": config("DB_USER"),
    "db_pass": config("DB_PASS"),
    "db_host": config("DB_HOST"),
    "db_port": config("DB_PORT"),
}
