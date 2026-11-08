
import pytest
import redis
from unittest.mock import MagicMock, patch

from app import create_app


@pytest.fixture
def mock_redis():
    client = MagicMock()
    client.ping.return_value = True
    client.incr.return_value = 1
    return client


@pytest.fixture
def client(mock_redis):
    with patch("app.routes.redis.Redis", return_value=mock_redis):
        app = create_app()
        app.config["TESTING"] = True
        yield app.test_client()


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Docker Compose Flask Application is running!"
    }


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy",
        "redis": "connected"
    }


def test_visits_endpoint(client):
    response = client.get("/visits")

    assert response.status_code == 200
    assert response.get_json() == {"visits": 1}


def test_health_endpoint_when_redis_is_unavailable(mock_redis):
    mock_redis.ping.side_effect = redis.RedisError("Redis unavailable")

    with patch("app.routes.redis.Redis", return_value=mock_redis):
        app = create_app()
        app.config["TESTING"] = True
        response = app.test_client().get("/health")

    assert response.status_code == 503
    assert response.get_json() == {
        "status": "unhealthy",
        "redis": "disconnected"
    }
