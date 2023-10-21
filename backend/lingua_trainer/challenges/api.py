from fastapi import APIRouter, HTTPException
from typing import List, Dict

challenges = []

router = APIRouter()

@router.get("/")
async def get_challenges():
    """
    Get the list of challenges based on uploaded words and phrases.

    Returns:
        list: List of challenges.
    """
    return challenges
