import pytest
from unittest.mock import Mock
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"
    with app.test_client() as client:
        yield client


def test_home_page_loads_successfully(client):
    response = client.get("/")
    assert response.status_code == 200


def test_chat_returns_400_for_empty_question(client):
    response = client.post("/api/chat", json={"question": "   "})
    assert response.status_code == 400
    assert response.get_json()["answer"] == "Please type a question."


def test_chat_returns_answer_for_valid_question(client, monkeypatch):
    fake_response = Mock()
    fake_response.choices = [Mock(message=Mock(content="Try breaking reading into short sections."))]

    fake_create = Mock(return_value=fake_response)
    monkeypatch.setattr("app.client.chat.completions.create", fake_create)

    response = client.post("/api/chat", json={"question": "I struggle reading long pages."})

    assert response.status_code == 200
    data = response.get_json()
    assert "answer" in data
    assert data["answer"] == "Try breaking reading into short sections."

    with client.session_transaction() as sess:
        assert len(sess["history"]) == 2
        assert sess["history"][0]["role"] == "user"
        assert sess["history"][1]["role"] == "assistant"


def test_chat_returns_500_when_api_fails(client, monkeypatch):
    def raise_error(*args, **kwargs):
        raise Exception("Groq failure")

    monkeypatch.setattr("app.client.chat.completions.create", raise_error)

    response = client.post("/api/chat", json={"question": "Help me with Canvas."})

    assert response.status_code == 500
    assert response.get_json()["answer"] == (
        "Sorry, something went wrong on the server. Please try again."
    )


def test_clear_chat_removes_history(client):
    with client.session_transaction() as sess:
        sess["history"] = [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi"},
        ]

    response = client.post("/api/clear")

    assert response.status_code == 200
    assert response.get_json()["ok"] is True

    with client.session_transaction() as sess:
        assert "history" not in sess


def test_chat_history_is_limited_to_max_history(client, monkeypatch):
    fake_response = Mock()
    fake_response.choices = [Mock(message=Mock(content="Test reply"))]
    monkeypatch.setattr("app.client.chat.completions.create", Mock(return_value=fake_response))

    for i in range(6):
        response = client.post("/api/chat", json={"question": f"Question {i}"})
        assert response.status_code == 200

    with client.session_transaction() as sess:
        # MAX_HISTORY = 10, and each chat adds 2 entries (user + assistant)
        assert len(sess["history"]) == 10
