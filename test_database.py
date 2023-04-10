import os
import sqlite3

from database import DB_FILEPATH, CREATE_TABLE_SQL, initialize_database

def setup_module(module):
    initialize_database()

def test_create_database():
    if os.path.exists(DB_FILEPATH):
        os.remove(DB_FILEPATH)

    assert not os.path.exists(DB_FILEPATH)

    conn = sqlite3.connect(DB_FILEPATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS news_summary")
    conn.execute(CREATE_TABLE_SQL)
    conn.close()

    assert os.path.exists(DB_FILEPATH)

def test_create_table():
    conn = sqlite3.connect(DB_FILEPATH)
    cursor = conn.cursor()

    # テーブルが存在するかどうか確認する
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='news_summary';").fetchone()
    assert result[0] == "news_summary"

    # テーブルのカラムが想定通りかどうか確認する
    expected_columns = ["id", "title", "summary", "created_at"]
    result = cursor.execute("PRAGMA table_info(news_summary)").fetchall()
    actual_columns = [column[1] for column in result]
    assert actual_columns == expected_columns

    conn.close()
