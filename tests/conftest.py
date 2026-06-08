"""
Pytest configuration and shared fixtures for all tests.
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from copy import deepcopy

# Add the src directory to the path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient connected to the FastAPI app.
    This allows testing the app without running a server.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Fixture that provides a deep copy of the sample activities data.
    This ensures each test gets fresh data and doesn't affect other tests.
    """
    return deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(sample_activities):
    """
    Fixture that resets the activities data before each test.
    This ensures test isolation - each test starts with clean data.
    The autouse=True means it runs automatically before each test.
    """
    # Clear existing activities
    activities.clear()
    # Repopulate with sample data
    activities.update(sample_activities)
    yield
    # Cleanup after test (optional, but good practice)
    activities.clear()
    activities.update(sample_activities)
