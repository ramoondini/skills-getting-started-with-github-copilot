"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify we get a dictionary with activities
    assert isinstance(data, dict)
    assert len(data) > 0
    
    # Verify we have the expected activities
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_has_correct_structure(client):
    """Test that each activity has the correct data structure."""
    response = client.get("/activities")
    data = response.json()
    
    # Check the first activity
    chess_club = data["Chess Club"]
    
    # Verify all required fields are present
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    
    # Verify data types
    assert isinstance(chess_club["description"], str)
    assert isinstance(chess_club["schedule"], str)
    assert isinstance(chess_club["max_participants"], int)
    assert isinstance(chess_club["participants"], list)


def test_get_activities_participants_are_emails(client):
    """Test that participants are email addresses."""
    response = client.get("/activities")
    data = response.json()
    
    # Check that participants are strings (emails)
    for activity_name, activity_data in data.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email validation
            assert ".edu" in participant  # Our test emails end with .edu


def test_get_activities_max_participants_is_positive(client):
    """Test that max_participants is a positive integer."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert activity_data["max_participants"] > 0
