"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_for_activity_successful(client):
    """Test successfully signing up for an activity."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity."""
    email = "newstudent@mergington.edu"
    
    # Sign up
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify the participant was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    participants = activities_data["Chess Club"]["participants"]
    
    assert email in participants


def test_signup_duplicate_prevented(client):
    """Test that signing up twice for the same activity is prevented."""
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    
    # Try to sign up again
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_fails(client):
    """Test that signing up for a non-existent activity returns 404."""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_multiple_students_same_activity(client):
    """Test that multiple students can sign up for the same activity."""
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # First student signs up
    response1 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email1}
    )
    assert response1.status_code == 200
    
    # Second student signs up
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email2}
    )
    assert response2.status_code == 200
    
    # Verify both are in the activity
    activities_response = client.get("/activities")
    participants = activities_response.json()["Programming Class"]["participants"]
    
    assert email1 in participants
    assert email2 in participants


def test_signup_different_activities(client):
    """Test that a student can sign up for multiple different activities."""
    email = "student@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify both signups worked
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    
    assert email in activities_data["Chess Club"]["participants"]
    assert email in activities_data["Programming Class"]["participants"]
