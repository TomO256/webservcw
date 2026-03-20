from . import login

client = login.SecureAPIClient()

def test_list_prices():
    response, data = client.get("/prices")
    assert response.status_code == 200
    assert isinstance(data, list)

def test_create_price():
    payload = {
        "date": "2024-01-01",
        "price_usd": 82.5,
        "source": "Test",
        "note": "Unit test"
    }
    response, data = client.post("/prices", payload)
    assert response.status_code == 201
    assert data["price_usd"] == 82.5

def test_filter_prices():
    response, data = client.get("/prices/filter?mini=50&maxi=100")
    assert response.status_code == 200
    assert isinstance(data, list)

def test_sort_prices():
    response, data = client.get("/prices/sort?sort_by=price_usd&order=desc")
    assert response.status_code == 200
