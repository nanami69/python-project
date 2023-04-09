from index import app, generate_summary

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

def test_generate_summary():
    prompt = "ニューヨークで人気のある観光スポット"
    summary = generate_summary(prompt)
    assert isinstance(summary, str)
    assert len(summary) > 0