import os
import json
import pytest

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from codereviewai.main import app, get_openai_response, GitHubAPI

load_dotenv()

API_KEY = os.environ["API_KEY"]
API_KEY_NAME = os.environ["API_KEY_NAME"]
API_TOKEN_GITHUB = os.environ["API_TOKEN_GITHUB"]
OPENAI_KEY = os.environ["OPENAI_KEY"]

repo_data = {
    "assignment_description": "A sample repo for testing",
    "github_repo_url": "https://github.com/sample/repo",
    "candidate_level": "Junior",
}

client = TestClient(app)


def test_get_api_key_success():
    """Test successful API key authentication."""
    response = client.get("/test-auth", headers={API_KEY_NAME: API_KEY})
    assert response.status_code == 200
    assert response.json() == {"api_key": API_KEY}


def test_get_api_key_failure():
    """Test failure in API key authentication with an incorrect key."""
    response = client.get("/test-auth", headers={API_KEY_NAME: "wrong_api_key"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


@pytest.fixture
def mock_redis():
    """Mock Redis instance for testing cache functionalities."""
    with patch("main.rd", new_callable=MagicMock) as mock_rd:
        yield mock_rd


def test_cache_set(mock_redis):
    """Test setting a value in the cache using Redis."""
    cache_key = "some_cache_key"
    value = {
        "message": "This is a mock review of the code.",
        "repository": {"github_repo_url": "https://github.com/sample/repo"},
    }

    mock_redis.set(cache_key, json.dumps(value), ex=60)
    mock_redis.set.assert_called_once_with(cache_key, json.dumps(value), ex=60)


def test_cache_get(mock_redis):
    """Test getting a value from the cache using Redis."""
    cache_key = "some_cache_key"
    value = {
        "message": "This is a mock review of the code.",
        "repository": {"github_repo_url": "https://github.com/sample/repo"},
    }

    mock_redis.get.return_value = json.dumps(value)
    result = json.loads(mock_redis.get(cache_key))
    mock_redis.get.assert_called_once_with(cache_key)
    assert result == value


@pytest.fixture
def mock_gitHub_api():
    """Mock GitHubAPI's get_all_files method for testing."""
    with patch(
        "codereviewai.main.GitHubAPI.get_all_files",
        return_value=("mock_repo_content", "mock_repo_files"),
    ) as mock:
        yield mock


@pytest.fixture
def mock_get_openai_response():
    """Mock get_openai_response function for testing."""
    with patch(
        "codereviewai.main.get_openai_response", return_value="This is a mock review."
    ) as mock:
        yield mock


def test_review(mock_gitHub_api, mock_get_openai_response, mock_redis):
    """Test the review endpoint by simulating a complete review process."""
    response = client.post("/review", json=repo_data, headers={API_KEY_NAME: API_KEY})
    assert response.status_code == 200
    assert response.json() == {
        "message": "This is a mock review.",
        "repository": repo_data,
    }
