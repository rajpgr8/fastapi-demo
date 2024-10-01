import pytest
from fastapi.testclient import TestClient
from main import app, User

# Create a TestClient to simulate requests to the FastAPI app
client = TestClient(app)

# Sample user data for testing
test_user = {"username": "john_doe", "email": "john@example.com"}
test_user_invalid = {"username": "john_doe", "email": "invalid-email"}

def test_create_user():
    response = client.post("/users/", json=test_user)
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully", "user": test_user}

def test_create_user_duplicate():
    client.post("/users/", json=test_user)  # Create the user first
    response = client.post("/users/", json=test_user)  # Try to create it again
    assert response.status_code == 400
    assert response.json() == {"message": "Username already taken"}

def test_get_user_by_username():
    client.post("/users/", json=test_user)  # Create the user first
    response = client.get("/users/john_doe")
    assert response.status_code == 200
    assert response.json() == {"message": "User found", "user": test_user}

def test_get_user_not_found():
    response = client.get("/users/non_existent_user")
    assert response.status_code == 404
    assert response.json() == {"message": "User not found"}

def test_delete_user():
    client.post("/users/", json=test_user)  # Create the user first
    response = client.delete("/users/john_doe")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully", "user": test_user}

def test_delete_user_not_found():
    response = client.delete("/users/non_existent_user")
    assert response.status_code == 404
    assert response.json() == {"message": "User not found"}

def test_update_user():
    client.post("/users/", json=test_user)  # Create the user first
    updated_user = {"username": "john_doe", "email": "john_new@example.com"}
    response = client.put("/users/john_doe", json=updated_user)
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully", "user": updated_user}

def test_update_user_not_found():
    updated_user = {"username": "non_existent_user", "email": "john_new@example.com"}
    response = client.put("/users/non_existent_user", json=updated_user)
    assert response.status_code == 404
    assert response.json() == {"message": "User not found"}

def test_get_users():
    client.post("/users/", json=test_user)  # Create the user first
    response = client.get("/users/?email=john@example.com")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["user"] == test_user

