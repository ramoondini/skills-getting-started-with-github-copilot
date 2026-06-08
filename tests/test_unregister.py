"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
"""

import pytest


def test_unregister_successful(client):
    """Test successfully unregistering from an activity."""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant from the activity."""
    email = "michael@mergington.edu"
    
    # Verify participant is there initially
    activities_response = client.get("/activities")
    participants_before = activities_response.json()["Chess Club"]["participants"]
    assert email in participants_before
    
    # Unregister
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify participant is removed
    activities_response = client.get("/activities")
    participants_after = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants_after


def test_unregister_nonexistent_activity_fails(client):
    """Test that unregistering from a non-existent activity returns 404."""
    response = client.delete(
        "/activities/Nonexistent Activity/unregister",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_unregister_not_registered_fails(client):
    """Test that unregistering when not registered returns 400."""
    email = "notstudent@mergington.edu"  # Not signed up for anything
    
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"].lower()


def test_unregister_from_one_activity_keeps_others(client):
    """Test that unregistering from one activity keeps registrations for others."""
    email = "student@mergington.edu"
    
    # Sign up for two activities
    client.post("/activities/Chess Club/signup", params={"email": email})
    client.post("/activities/Programming Class/signup", params={"email": email})
    
    # Unregister from Chess Club
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify removed from Chess Club but still in Programming Class
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    
    assert email not in activities_data["Chess Club"]["participants"]
    assert email in activities_data["Programming Class"]["participants"]


def test_unregister_then_signup_again_allowed(client):
    """Test that a student can sign up after unregistering."""
    email = "michael@mergington.edu"
    
    # Unregister
    response1 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up again
    response2 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify signed up
    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants
