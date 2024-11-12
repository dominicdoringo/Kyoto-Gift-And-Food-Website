# tests/test_user.py

import pytest
import uuid
from app.models.user import User

def generate_unique_user_data():
    unique_id = str(uuid.uuid4())
    return {
        "username": f"testuser_{unique_id}",
        "email": f"testuser_{unique_id}@example.com",
        "password": "password123"
    }

def test_register_user(client, db):
    user_data = generate_unique_user_data()
    response = client.post(
        "/users/register",
        json=user_data
    )
    assert response.status_code == 201, "User registration failed"
    data = response.json()
    assert data["username"] == user_data["username"], "Username mismatch"
    assert data["email"] == user_data["email"], "Email mismatch"
    assert data["is_verified"] is False, "User should not be verified upon registration"

def test_login(client, db):
    # Register a user
    user_data = generate_unique_user_data()
    response = client.post(
        "/users/register",
        json=user_data
    )
    assert response.status_code == 201, "User registration failed"
    
    # Retrieve the user from the database
    user = db.query(User).filter(User.username == user_data["username"]).first()
    assert user is not None, "User not found in the database"

    # Simulate email verification
    verification_code = user.verification_code
    response = client.get(f"/users/verify-email/{verification_code}")
    assert response.status_code == 200, "Email verification failed"

    # Attempt to log in
    response = client.post(
        "/users/token",
        data={"username": user_data["username"], "password": user_data["password"]}
    )
    assert response.status_code == 200, "User login failed"
    data = response.json()
    assert "access_token" in data, "Access token not returned"
    assert data["token_type"] == "bearer", "Incorrect token type"

def test_get_current_user(client, db):
    # Register and verify a user
    user_data = generate_unique_user_data()
    response = client.post(
        "/users/register",
        json=user_data
    )
    assert response.status_code == 201, "User registration failed"
    
    user = db.query(User).filter(User.username == user_data["username"]).first()
    assert user is not None, "User not found in the database"
    
    verification_code = user.verification_code
    response = client.get(f"/users/verify-email/{verification_code}")
    assert response.status_code == 200, "Email verification failed"

    # Log in
    response = client.post(
        "/users/token",
        data={"username": user_data["username"], "password": user_data["password"]}
    )
    assert response.status_code == 200, "User login failed"
    access_token = response.json()["access_token"]

    # Get current user info
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200, "Failed to retrieve current user info"
    data = response.json()
    assert data["username"] == user_data["username"], "Username mismatch in current user info"
    assert data["email"] == user_data["email"], "Email mismatch in current user info"

def test_update_user_info(client, db):
    # Register and verify a user
    user_data = generate_unique_user_data()
    response = client.post(
        "/users/register",
        json=user_data
    )
    assert response.status_code == 201, "User registration failed"
    
    user = db.query(User).filter(User.username == user_data["username"]).first()
    assert user is not None, "User not found in the database"
    
    verification_code = user.verification_code
    response = client.get(f"/users/verify-email/{verification_code}")
    assert response.status_code == 200, "Email verification failed"

    # Log in
    response = client.post(
        "/users/token",
        data={"username": user_data["username"], "password": user_data["password"]}
    )
    assert response.status_code == 200, "User login failed"
    access_token = response.json()["access_token"]

    # Update user info
    headers = {"Authorization": f"Bearer {access_token}"}
    updated_data = {
        "username": f"updated_{user_data['username']}",
        "email": f"updated_{user_data['email']}"
    }
    response = client.put(
        f"/users/{user.id}",
        json=updated_data,
        headers=headers
    )
    assert response.status_code == 200, "User info update failed"
    data = response.json()
    assert data["username"] == updated_data["username"], "Username not updated correctly"
    assert data["email"] == updated_data["email"], "Email not updated correctly"

def test_change_password(client, db):
    # Register and verify a user
    user_data = generate_unique_user_data()
    response = client.post(
        "/users/register",
        json=user_data
    )
    assert response.status_code == 201, "User registration failed"
    
    user = db.query(User).filter(User.username == user_data["username"]).first()
    assert user is not None, "User not found in the database"
    
    verification_code = user.verification_code
    response = client.get(f"/users/verify-email/{verification_code}")
    assert response.status_code == 200, "Email verification failed"

    # Log in
    response = client.post(
        "/users/token",
        data={"username": user_data["username"], "password": user_data["password"]}
    )
    assert response.status_code == 200, "User login failed"
    access_token = response.json()["access_token"]

    # Change password
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put(
        f"/users/{user.id}/password",
        json={
            "old_password": user_data["password"],
            "new_password": "newpassword"
        },
        headers=headers
    )
    assert response.status_code == 200, "Password change failed"
    assert response.json()["message"] == "Password updated successfully", "Incorrect success message"

    # Attempt to log in with new password
    response = client.post(
        "/users/token",
        data={"username": user_data["username"], "password": "newpassword"}
    )
    assert response.status_code == 200, "Login with new password failed"
    assert "access_token" in response.json(), "Access token not returned after password change"

def test_delete_user_account(client, db):
    # Register and verify a user
    user_data = generate_unique_user_data()
    response = client.post(
        "/users/register",
        json=user_data
    )
    assert response.status_code == 201, "User registration failed"
    
    user = db.query(User).filter(User.username == user_data["username"]).first()
    assert user is not None, "User not found in the database"
    
    verification_code = user.verification_code
    response = client.get(f"/users/verify-email/{verification_code}")
    assert response.status_code == 200, "Email verification failed"

    # Log in
    response = client.post(
        "/users/token",
        data={"username": user_data["username"], "password": user_data["password"]}
    )
    assert response.status_code == 200, "User login failed"
    access_token = response.json()["access_token"]

    # Delete account
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete(f"/users/{user.id}", headers=headers)
    assert response.status_code == 204, "User account deletion failed"

    # Verify user is deleted from the database
    deleted_user = db.query(User).filter(User.id == user.id).first()
    assert deleted_user is None, "User was not deleted from the database"

def test_user_cannot_access_others_info(client, db):
    # Register and verify user1
    user1_data = generate_unique_user_data()
    response = client.post(
        "/users/register",
        json=user1_data
    )
    assert response.status_code == 201, "User1 registration failed"
    
    user1 = db.query(User).filter(User.username == user1_data["username"]).first()
    assert user1 is not None, "User1 not found in the database"
    
    verification_code1 = user1.verification_code
    response = client.get(f"/users/verify-email/{verification_code1}")
    assert response.status_code == 200, "User1 email verification failed"

    # Log in as user1
    response = client.post(
        "/users/token",
        data={"username": user1_data["username"], "password": user1_data["password"]}
    )
    assert response.status_code == 200, "User1 login failed"
    access_token1 = response.json()["access_token"]

    # Register and verify user2
    user2_data = generate_unique_user_data()
    response = client.post(
        "/users/register",
        json=user2_data
    )
    assert response.status_code == 201, "User2 registration failed"
    
    user2 = db.query(User).filter(User.username == user2_data["username"]).first()
    assert user2 is not None, "User2 not found in the database"
    
    verification_code2 = user2.verification_code
    response = client.get(f"/users/verify-email/{verification_code2}")
    assert response.status_code == 200, "User2 email verification failed"

    # Log in as user2
    response = client.post(
        "/users/token",
        data={"username": user2_data["username"], "password": user2_data["password"]}
    )
    assert response.status_code == 200, "User2 login failed"
    access_token2 = response.json()["access_token"]

    # User1 attempts to access User2's details
    headers1 = {"Authorization": f"Bearer {access_token1}"}
    response = client.get(f"/users/{user2.id}", headers=headers1)
    assert response.status_code == 403, "User1 should not access User2's details"
    assert response.json()["detail"] == "Not authorized to view this user", "Incorrect error message for unauthorized access"

    # User1 attempts to update User2's details
    response = client.put(
        f"/users/{user2.id}",
        json={"username": "hacker"},
        headers=headers1
    )
    assert response.status_code == 403, "User1 should not update User2's details"
    assert response.json()["detail"] == "Not authorized to update this user", "Incorrect error message for unauthorized update"

def test_email_verification_failure(client):
    # Attempt to verify with an invalid code
    response = client.get("/users/verify-email/invalidcode")
    assert response.status_code == 400, "Should return 400 for invalid verification code"
    assert response.json()["detail"] == "Invalid verification code.", "Incorrect error message for invalid verification code"

def test_duplicate_registration(client):
    # Register a user
    user_data = generate_unique_user_data()
    response = client.post(
        "/users/register",
        json={
            "username": "duplicateuser",
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201, "First user registration failed"

    # Attempt to register again with the same username
    response = client.post(
        "/users/register",
        json={
            "username": "duplicateuser",
            "email": "newemail@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 400, "Duplicate username registration should fail"
    assert response.json()["detail"] == "Username or email already registered", "Incorrect error message for duplicate username"

    # Attempt to register again with the same email
    response = client.post(
        "/users/register",
        json={
            "username": "newuser",
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 400, "Duplicate email registration should fail"
    assert response.json()["detail"] == "Username or email already registered", "Incorrect error message for duplicate email"

def test_password_change_with_wrong_old_password(client, db):
    # Register and verify a user
    user_data = generate_unique_user_data()
    response = client.post(
        "/users/register",
        json={
            "username": "testuser8",
            "email": "testuser8@example.com",
            "password": "correctpassword"
        }
    )
    assert response.status_code == 201, "User registration failed"
    
    user = db.query(User).filter(User.username == "testuser8").first()
    assert user is not None, "User not found in the database"
    
    verification_code = user.verification_code
    response = client.get(f"/users/verify-email/{verification_code}")
    assert response.status_code == 200, "Email verification failed"

    # Log in
    response = client.post(
        "/users/token",
        data={"username": "testuser8", "password": "correctpassword"}
    )
    assert response.status_code == 200, "User login failed"
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
    assert response.status_code == 400, "Password change with wrong old password should fail"
    assert response.json()["detail"] == "Old password is incorrect", "Incorrect error message for wrong old password"



def test_register_cart_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "test_cart_user",
            "email": "test_cart_user@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "test_cart_user"
    assert data["email"] == "test_cart_user@example.com"
    assert data["is_verified"] == False

def test_verify_cart_user_email(client, db):
    # Get the cart user from the database
    user = db.query(User).filter(User.username == "test_cart_user").first()
    assert user is not None, "Cart user not found"
    verification_code = user.verification_code
    response = client.get(f"/users/verify-email/{verification_code}")
    assert response.status_code == 200
    assert response.json()["message"] == "Email successfully verified."

    # Ensure the user is verified
    db.refresh(user)
    assert user.is_verified is True
