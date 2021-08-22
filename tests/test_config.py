from src.config import get_db_uri


def test_get_db_uri(monkeypatch):
    monkeypatch.setenv("DB_DRIVER", "sqlite")
    db_uri = get_db_uri()
    assert db_uri == "sqlite:///db_test.db"
