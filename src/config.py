import databases
from prettyconf import config


def get_db_uri():
    driver = config("DB_DRIVER", default="sqlite")

    if driver == "sqlite":
        return "sqlite:///db_test.db"

    host = config("DB_HOST", default="localhost")
    port = config("DB_PORT")
    password = config("DB_PASSWORD", default="password")
    user = config("DB_USER", default="user")
    db_name = config("DB_NAME", default="db_test")

    return f"{driver}://{user}:{password}@{host}:{port}/{db_name}"


database = databases.Database(get_db_uri())
