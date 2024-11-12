# tests/test_user.py

import pytest
from app.models.user import User

def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "testuser1",
            "email": "testuser1@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser1"
    assert data["email"] == "testuser1@example.com"
    assert data["is_verified"] is False

def test_login(client, db):
    # Register a user
    client.post(
        "/users/register",
        json={
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "password123"
        }
    )
    # Retrieve the user from the database
    user = db.query(User).filter(User.username == "testuser2").first()
    assert user is not None
    # Simulate email verification
    verification_code = user.verification_code
    response = client.get(f"/users/verify-email/{verification_code}")
    assert response.status_code == 200

    # Attempt to log in
    response = client.post(
        "/users/token",
        data={"username": "testuser2", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user(client, db):
    # Register and verify a user
    client.post(
        "/users/register",
        json={
            "username": "testuser3",
            "email": "testuser3@example.com",
            "password": "password123"
        }
    )
    user = db.query(User).filter(User.username == "testuser3").first()
    verification_code = user.verification_code
    client.get(f"/users/verify-email/{verification_code}")

    # Log in
    response = client.post(
        "/users/token",
        data={"username": "testuser3", "password": "password123"}
    )
    access_token = response.json()["access_token"]

    # Get current user info
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser3"
    assert data["email"] == "testuser3@example.com"

def test_update_user_info(client, db):
    # Register and verify a user
    client.post(
        "/users/register",
        json={
            "username": "testuser4",
            "email": "testuser4@example.com",
            "password": "password123"
        }
    )
    user = db.query(User).filter(User.username == "testuser4").first()
    verification_code = user.verification_code
    client.get(f"/users/verify-email/{verification_code}")

    # Log in
    response = client.post(
        "/users/token",
        data={"username": "testuser4", "password": "password123"}
    )
    access_token = response.json()["access_token"]

    # Update user info
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put(
        f"/users/{user.id}",
        json={
            "username": "updateduser4",
            "email": "updateduser4@example.com"
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser4"
    assert data["email"] == "updateduser4@example.com"

def test_change_password(client, db):
    # Register and verify a user
    client.post(
        "/users/register",
        json={
            "username": "testuser5",
            "email": "testuser5@example.com",
            "password": "oldpassword"
        }
    )
    user = db.query(User).filter(User.username == "testuser5").first()
    verification_code = user.verification_code
    client.get(f"/users/verify-email/{verification_code}")

    # Log in
    response = client.post(
        "/users/token",
        data={"username": "testuser5", "password": "oldpassword"}
    )
    access_token = response.json()["access_token"]

    # Change password
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put(
        f"/users/{user.id}/password",
        json={
            "old_password": "oldpassword",
            "new_password": "newpassword"
        },
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

    # Attempt to log in with new password
    response = client.post(
        "/users/token",
        data={"username": "testuser5", "password": "newpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()



def test_delete_user_account(client, db):
    # Register and verify a user
    client.post(
        "/users/register",
        json={
            "username": "testuser7",
            "email": "testuser7@example.com",
            "password": "password123"
        }
    )
    user = db.query(User).filter(User.username == "testuser7").first()
    verification_code = user.verification_code
    client.get(f"/users/verify-email/{verification_code}")

    # Log in
    response = client.post(
        "/users/token",
        data={"username": "testuser7", "password": "password123"}
    )
    access_token = response.json()["access_token"]

    # Delete account
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete(f"/users/{user.id}", headers=headers)
    assert response.status_code == 204

    # Verify user is deleted from the database
    deleted_user = db.query(User).filter(User.id == user.id).first()
    assert deleted_user is None

def test_user_cannot_access_others_info(client, db):
    # Register and verify user1
    client.post(
        "/users/register",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "password1"
        }
    )
    user1 = db.query(User).filter(User.username == "user1").first()
    verification_code1 = user1.verification_code
    client.get(f"/users/verify-email/{verification_code1}")
    response = client.post(
        "/users/token",
        data={"username": "user1", "password": "password1"}
    )
    access_token1 = response.json()["access_token"]

    # Register and verify user2
    client.post(
        "/users/register",
        json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "password2"
        }
    )
    user2 = db.query(User).filter(User.username == "user2").first()
    verification_code2 = user2.verification_code
    client.get(f"/users/verify-email/{verification_code2}")
    response = client.post(
        "/users/token",
        data={"username": "user2", "password": "password2"}
    )
    access_token2 = response.json()["access_token"]

    # User1 attempts to access User2's details
    headers1 = {"Authorization": f"Bearer {access_token1}"}
    response = client.get(f"/users/{user2.id}", headers=headers1)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to view this user"

    # User1 attempts to update User2's details
    response = client.put(
        f"/users/{user2.id}",
        json={"username": "hacker"},
        headers=headers1
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to update this user"

def test_email_verification_failure(client):
    # Attempt to verify with an invalid code
    response = client.get("/users/verify-email/invalidcode")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid verification code."

def test_duplicate_registration(client):
    # Register a user
    client.post(
        "/users/register",
        json={
            "username": "duplicateuser",
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )
    # Attempt to register again with the same username
    response = client.post(
        "/users/register",
        json={
            "username": "duplicateuser",
            "email": "newemail@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already registered"

    # Attempt to register again with the same email
    response = client.post(
        "/users/register",
        json={
            "username": "newuser",
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already registered"

def test_password_change_with_wrong_old_password(client, db):
    # Register and verify a user
    client.post(
        "/users/register",
        json={
            "username": "testuser8",
            "email": "testuser8@example.com",
            "password": "correctpassword"
        }
    )
    user = db.query(User).filter(User.username == "testuser8").first()
    verification_code = user.verification_code
    client.get(f"/users/verify-email/{verification_code}")

    # Log in
    response = client.post(
        "/users/token",
        data={"username": "testuser8", "password": "correctpassword"}
    )
    access_token = response.json()["access_token"]

    # Attempt to change password with incorrect old password
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put(
        f"/users/{user.id}/password",
        json={
            "old_password": "wrongpassword",
            "new_password": "newpassword"
        },
        headers=headers
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Old password is incorrect"
