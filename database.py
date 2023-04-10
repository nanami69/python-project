import sqlite3
import os

# データベースのファイルパス
DB_FILEPATH = "summary_app.db"

# テーブル作成のためのDDL文
CREATE_TABLE_SQL = """
CREATE TABLE news_summary (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    created_at DATETIME DEFAULT (DATETIME('now', 'localtime'))
);
"""

def initialize_database():
    if os.path.exists(DB_FILEPATH):
        os.remove(DB_FILEPATH)

    # データベースファイルを作成する
    conn = sqlite3.connect(DB_FILEPATH)

    # テーブル作成のためのDDL文を実行する
    conn.execute(CREATE_TABLE_SQL)

    # 変更をコミットして、変更を保存する
    conn.commit()

    # データベースをクローズする
    conn.close()
