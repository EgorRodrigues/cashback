import databases
from prettyconf import config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def get_db_uri():
    return config("DATABASE_URL")


# Databases

database = databases.Database(get_db_uri())

# SqlAlchemy

# check_same_thread argument is needed only for SQLite.
engine = create_async_engine(
    get_db_uri(), echo=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
