from fastapi import APIRouter, HTTPException
from typing import List, Dict

words = {}
challenges = []
leaderboard = []

router = APIRouter()

# Word and Phrase Management
@router.get("/")
async def get_words():
    """
    Get a list of uploaded words and phrases.

    Returns:
        dict: Dictionary containing uploaded words and phrases.
    """
    return words


@router.post("/")
async def upload_words(word_data: List[dict]):
    """
    Upload new words and phrases.

    Args:
        word_data (List[dict]): List of word and phrase data to be uploaded.

    Returns:
        dict: A message indicating the success of the word upload.
    """
    for word in word_data:
        words[word["id"]] = word
    return {"message": "Words uploaded successfully"}


@router.get("/{word_id}")
async def get_word(word_id: int):
    """
    Get details of a specific word or phrase.

    Args:
        word_id (int): ID of the word or phrase.

    Returns:
        dict: Details of the word or phrase.

    Raises:
        HTTPException: If the word or phrase is not found.
    """
    if word_id in words:
        return words[word_id]
    else:
        raise HTTPException(status_code=404, detail="Word not found")


@router.put("/{word_id}")
async def update_word(word_id: int, updated_word: dict):
    """
    Update details of a specific word or phrase.

    Args:
        word_id (int): ID of the word or phrase.
        updated_word (dict): Updated details of the word or phrase.

    Returns:
        dict: A message indicating the success of the word update.

    Raises:
        HTTPException: If the word or phrase is not found.
    """
    if word_id in words:
        words[word_id].update(updated_word)
        return {"message": "Word updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Word not found")



@router.delete("/{word_id}")
async def delete_word(word_id: int):
    """
    Delete a specific word or phrase.

    Args:
        word_id (int): ID of the word or phrase.

    Returns:
        dict: A message indicating the success of the word deletion.

    Raises:
        HTTPException: If the word or phrase is not found.
    """
    if word_id in words:
        del words[word_id]
        return {"message": "Word deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Word not found")


