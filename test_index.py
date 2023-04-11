from index import app, generate_summary
from database import DB_FILEPATH
import sqlite3

def test_index():
    with app.test_client() as client:
        response = client.get('/index')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data

def test_sub():
    with app.test_client() as client:
        response = client.get('/sub')
        assert response.status_code == 200
        assert b'This is Sub Page!' in response.data

def test_list():
    with app.test_client() as client:
        response = client.get('/list')
        assert response.status_code == 200

        # データベースから取得したデータが正しくテンプレートに反映されているかを確認する
        conn = sqlite3.connect(DB_FILEPATH)
        cursor = conn.cursor()
        select_sql = """
            SELECT title, summary FROM news_summary
        """
        cursor.execute(select_sql)
        expected_data = cursor.fetchall()
        conn.close()

        for expected_row in expected_data:
            assert expected_row[0] in str(response.data) # タイトルが含まれているか確認
            assert expected_row[1] in str(response.data) # サマリが含まれているか確認

def test_generate_summary():
    prompt = "ニューヨークで人気のある観光スポット"
    summary = generate_summary(prompt)
    assert isinstance(summary, str)
    assert len(summary) > 0