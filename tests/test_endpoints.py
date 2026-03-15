from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_summarize_missing_api_key():
    response = client.post(
        "/summarize",
        json={"text": "This is a test text.", "max_words": 50},
    )
    assert response.status_code == 422


def test_classify_missing_api_key():
    response = client.post(
        "/classify",
        json={"text": "This is a test text.", "labels": ["positive", "negative"]},
    )
    assert response.status_code == 422


def test_summarize_with_mock():
    with patch("app.main.summarize_text") as mock:
        mock.return_value = {"summary": "This is a summary.", "word_count": 4}
        response = client.post(
            "/summarize",
            json={"text": "This is a long text.", "max_words": 50},
            headers={"x-api-key": "fake-key"},
        )
        assert response.status_code == 200
        assert response.json()["summary"] == "This is a summary."


def test_classify_with_mock():
    with patch("app.main.classify_text") as mock:
        mock.return_value = {"label": "positive", "reason": "The text sounds positive."}
        response = client.post(
            "/classify",
            json={"text": "I love this!", "labels": ["positive", "negative"]},
            headers={"x-api-key": "fake-key"},
        )
        assert response.status_code == 200
        assert response.json()["label"] == "positive"