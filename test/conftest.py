import os
import sqlite3

import pytest


@pytest.fixture()
def db():
    db_path = 'todo.db'
    db_conn = sqlite3.connect(db_path)
    yield db_conn
    db_conn.close()
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture()
def db_fixture():
    db_path = 'todo.db'
    db_conn = sqlite3.connect(db_path)

    cur = db_conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS todo (todo_text TEXT);')
    db_conn.commit()

    yield db_conn
    db_conn.close()
    if os.path.exists(db_path):
        os.remove(db_path)


def pytest_configure(config):
    config.addinivalue_line("markers", "slow")
    config.addinivalue_line("markers", "fast")
