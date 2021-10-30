import shelve

import pytest


@pytest.fixture
def shelve_session():
    session = shelve.open("test", writeback=True)
    try:
        yield session
    finally:
        session.close()
