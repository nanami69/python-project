from index import app, generate_summary, generate_question, request_openai_api
from flask import url_for
from database import DB_FILEPATH
import sqlite3
import pytest
import requests
from unittest import mock

@pytest.fixture()
def requests_mock():
    with mock.patch('index.requests') as mock_requests:
        yield mock_requests

def test_index():
    with app.test_client() as client:
        response = client.get('/index')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data

def test_root():
    with app.test_request_context():
        response = app.test_client().get('/')
        assert response.status_code == 302
        assert response.headers['Location'] == url_for('index')

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

def test_generate_question():
    prompt = "ニューヨークで人気のある観光スポット"
    question, question_en = generate_question(prompt)
    assert isinstance(question, str)
    assert len(question) > 0
    assert isinstance(question_en, str)
    assert len(question_en) > 0

def test_request_openai_api_successful(requests_mock):
    # Mock API response
    prompt_text = "Sample prompt"
    expected_result = "Sample response"
    requests_mock.post.return_value.json.return_value = {"choices": [{"text": expected_result}]}

    # Call function and check result
    result = request_openai_api(prompt_text)
    assert result == expected_result

def test_request_openai_api_error(requests_mock):
    # Mock API response with error status code
    prompt_text = "Sample prompt"
    requests_mock.post.return_value.status_code = 500
    requests_mock.post.side_effect = requests.exceptions.HTTPError()

    # Call function and check that it raises an exception
    with pytest.raises(ValueError, match="Invalid response from API: "):
        request_openai_api(prompt_text)