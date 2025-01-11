import pytest
from fastapi.testclient import TestClient
from Backend.main import app  # Import from the same folder without 'Backend'
from Backend.settings import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Backend.db import Base
from Backend.models import User
from Backend.schemas import UserCreate, ChatMessageCreate, ChatMessageResponse
from Backend.db import Base

Base.metadata.clear()
# Setting up a testing database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use SQLite for testing

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)

# Test user creation
def test_create_user(client):
    response = client.post(
        "/api/users",
        json={"email": "testuser@example.com", "hashed_password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test token generation
def test_generate_token(client):
    # First, create a user to be able to generate a token
    client.post(
        "/api/users",
        json={"email": "testuser@example.com", "hashed_password": "password123"},
    )

    response = client.post(
        "/api/token",
        data={"username": "testuser@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test fetching the current user
def test_get_user(client):
    # First, create a user to get the token
    client.post(
        "/api/users",
        json={"email": "testuser@example.com", "hashed_password": "password123"},
    )

    response = client.post(
        "/api/token",
        data={"username": "testuser@example.com", "password": "password123"},
    )

    token = response.json()["access_token"]
    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

# Test sending and receiving messages
def test_create_message(client):
    # First, create a user and get a token
    client.post(
        "/api/users",
        json={"email": "testuser@example.com", "hashed_password": "password123"},
    )

    response = client.post(
        "/api/token",
        data={"username": "testuser@example.com", "password": "password123"},
    )

    token = response.json()["access_token"]

    # Send a message
    response = client.post(
        "/api/messages",
        json={"content": "Hello, bot!"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["user_message"] == "Hello, bot!"

# Test deleting a message
def test_delete_message(client):
    # First, create a user and get a token
    client.post(
        "/api/users",
        json={"email": "testuser@example.com", "hashed_password": "password123"},
    )

    response = client.post(
        "/api/token",
        data={"username": "testuser@example.com", "password": "password123"},
    )

    token = response.json()["access_token"]

    # Send a message
    response = client.post(
        "/api/messages",
        json={"content": "Message to be deleted"},
        headers={"Authorization": f"Bearer {token}"},
    )

    message_id = response.json()["id"]

    # Now, delete the message
    response = client.delete(
        f"/api/messages/{message_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204  # No content
