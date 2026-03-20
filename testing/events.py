from . import login

client = login.SecureAPIClient()

def test_list_events():
    response, data = client.get("/events")
    assert response.status_code == 200
    assert isinstance(data, list)

def test_event_type():
    response, data = client.get("/events/type?event_type=war")
    assert response.status_code == 200
