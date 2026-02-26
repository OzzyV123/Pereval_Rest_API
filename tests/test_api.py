from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_submit_and_get_pereval():
    payload = {
        "beauty_title": "пер.",
        "title": "Тестовый",
        "other_titles": "",
        "connect": "",
        "user": {
            "email": "api@test.ru",
            "fam": "API",
            "name": "Test",
            "otc": "",
            "phone": "+79999999999"
        },
        "coords": {
            "latitude": 45.0,
            "longitude": 7.0,
            "height": 1200
        },
        "level": {
            "winter": "",
            "summer": "1А",
            "autumn": "1А",
            "spring": ""
        },
        "images": []
    }

    r = client.post("/submitData", json=payload)
    assert r.status_code == 200

    pereval_id = r.json()["id"]

    r2 = client.get(f"/submitData/{pereval_id}")
    assert r2.status_code == 200
    assert r2.json()["title"] == "Тестовый"