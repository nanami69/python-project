from index import sum
from index import app
import sys

def test_sum(mocker):
    mocker.patch.object(sys, 'argv', ['test_index.py', '2', '3'])
    result = sum(int(sys.argv[1]), int(sys.argv[2]))
    assert result == 5

    result = sum(2,3)
    assert result == 5

def test_index():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data

def test_sub():
    with app.test_client() as client:
        response = client.get('/sub')
        assert response.status_code == 200
        assert b'This is Sub Page!' in response.data