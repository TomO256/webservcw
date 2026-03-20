from . import login

client = login.SecureAPIClient()

def test_average_price():
    response, data = client.get("/analytics/average")
    assert response.status_code == 200
    assert "average_price" in data

def test_max_price():
    response, data = client.get("/analytics/max")
    assert response.status_code == 200

def test_min_price():
    response, data = client.get("/analytics/min")
    assert response.status_code == 200
