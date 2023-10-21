from fastapi import APIRouter, HTTPException
from typing import List, Dict
from .models import UserProfile

users = {}

router = APIRouter()

# User Authentication and Authorization
@router.post("/register")
async def register_user(user: UserProfile):
    """
    Register a new user account.

    Args:
        user (dict): User data including username, password, and other details.

    Returns:
        dict: A message indicating the success of the registration.
    """
    user_id = len(users) + 1
    users[user_id] = user
    return {
                "message": "User registered successfully",
                "user": user
            }

@router.post("/login")
async def login(username: str, password: str):
    """
    Authenticate and log in a user.

    Args:
        username (str): Username of the user.
        password (str): Password of the user.

    Returns:
        dict: A message indicating the success of the login.
    
    Raises:
        HTTPException: If invalid credentials are provided.
    """
    # Validate credentials
    if username in users and users[username]["password"] == password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/logout")
async def logout():
    """
    Log out the currently authenticated user.

    Returns:
        dict: A message indicating successful logout.
    """
    # Perform logout actions
    return {"message": "Logged out successfully"}