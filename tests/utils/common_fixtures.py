import pytest
import asyncio

from mammon_api.db import Base, replenishment

__all__ = [
    'async_loop',
    'preload_database'
]


@pytest.fixture(scope='session')
def async_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
def preload_database():
    """Database preload, cleanup, table initialization"""
    Base.metadata.drop_all()
    replenishment.init_tables()
    yield
