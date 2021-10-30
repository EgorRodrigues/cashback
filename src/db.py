import databases
from prettyconf import config


def get_db_uri():
    return config("DATABASE_URL")


database = databases.Database(get_db_uri())
