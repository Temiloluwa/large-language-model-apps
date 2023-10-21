from fastapi import APIRouter, HTTPException
from typing import List, Dict
from .models import UserProfile

users = []
router = APIRouter()


@router.get("/profile/{user_id}")
async def get_user_profile(user_id: str):
    """
    Get user profile information.

    Args:
        user_id (int): ID of the user.

    Returns:
        dict: User profile information.

    Raises:
        HTTPException: If the user is not found.
    """
    if user_id in users:
        return users[user_id]
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/profile/{user_id}")
async def update_user_profile(user_id: str, updated_profile: UserProfile):
    """
    Update user profile information.

    Args:
        user_id (int): ID of the user.
        updated_profile (dict): Updated user profile data.

    Returns:
        dict: A message indicating the success of the profile update.

    Raises:
        HTTPException: If the user is not found.
    """
    if user_id in users:
        users[user_id] = updated_profile.dict()
        return {"message": "Profile updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
