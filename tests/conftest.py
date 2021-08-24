import pytest
import shelve


@pytest.fixture
def shelve_session():
    session = shelve.open("test", writeback=True)
    try:
        yield session
    finally:
        session.close()
