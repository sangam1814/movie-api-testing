import pytest
import requests

@pytest.fixture
def base_url():
    return "https://682ad119ab2b5004cb37d298.mockapi.io"

@pytest.fixture
def movies_endpoint(base_url):
    return f"{base_url}/movies"

@pytest.fixture
def reviews_endpoint(base_url):
    return f"{base_url}/reviews"