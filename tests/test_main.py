def test_index_route(client):
    response = client.get("/")
    assert b"Smarthome Home" in response.data
    assert b"LED Control Kamar 1" in response.data
    assert b"Turn On" in response.data
    assert b"Turn Off" in response.data


def test_fungsi_route(client):
    response = client.get("/fungsi")
    assert response.data == b"Mantap"
