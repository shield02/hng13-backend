from stage0.app.app import app

def test_me_endpoint_returns_valid_json():
    client = app.test_client()
    response = client.get("/me")

    # Status code
    assert response.status_code == 200

    # Content type
    assert response.content_type == "application/json"

    # Body structure
    data = response.get_json()
    assert "status" in data
    assert "user" in data
    assert "timestamp" in data
    assert "fact" in data

    # Check subfields
    user = data["user"]
    assert "email" in user
    assert "name" in user
    assert "stack" in user

def test_me_endpoint_handles_catfact_failure(monkeypatch):
    """Simulate Cat Facts API being down and ensure fallback works."""

    def mock_get(*args, **kwargs):
        class MockResponse:
            ok = False
            def json(self):
                return {}
        return MockResponse()

    # Patch requests.get
    import requests
    monkeypatch.setattr(requests, "get", mock_get)

    client = app.test_client()
    response = client.get("/me")
    data = response.get_json()

    assert response.status_code == 200
    assert "Cats" in data["fact"]  # fallback string still appears
