from index import app

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