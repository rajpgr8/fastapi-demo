from fastapi.testclient import TestClient
from main import app
import pytest

# Create a test client using the FastAPI app
client = TestClient(app)

# Test creating a new item
def test_create_item():
    response = client.post(
        "/items/",
        json={
            "name": "Laptop",
            "price": 1200.50,
            "tax": 120.50
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        "message": "Item created successfully",
        "item": {
            "name": "Laptop",
            "price": 1200.50,
            "tax": 120.50
        }
    }

# Test getting all items
def test_get_all_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Laptop"

# Test getting a single item by name
def test_get_item():
    response = client.get("/items/Laptop")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"
    assert response.json()["price"] == 1200.50

# Test updating an item
def test_update_item():
    response = client.put(
        "/items/Laptop",
        json={"price": 1300.00}
    )
    assert response.status_code == 200
    assert response.json()["price"] == 1300.00

# Test deleting an item
def test_delete_item():
    response = client.delete("/items/Laptop")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}

# Test getting an item that does not exist
def test_get_non_existent_item():
    response = client.get("/items/NonExistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

# Test creating an item that already exists
def test_create_duplicate_item():
    client.post(
        "/items/",
        json={
            "name": "Phone",
            "price": 500.00,
            "tax": 50.00
        }
    )
    response = client.post(
        "/items/",
        json={
            "name": "Phone",
            "price": 500.00,
            "tax": 50.00
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}

# Test deleting an item that doesn't exist
def test_delete_non_existent_item():
    response = client.delete("/items/NonExistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

