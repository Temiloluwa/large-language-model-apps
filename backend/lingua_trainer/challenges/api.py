import openai
from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from functools import lru_cache
from fastapi.responses import StreamingResponse
from .models import (WEWordRequest, WESentenceRequest, Settings)
from .word_explorer import (word_explainer, sentence_generator, stream_tokens)

router = APIRouter()

@lru_cache()
def get_settings(use_default=True):
    # set api key
    openai.api_key = Settings().DEFAULT_API_KEY if use_default else Settings().CLIENT_API_KEY
    return Settings()


@router.post("/word_explorer/word_explainer")
async def explain(
        request_data: WEWordRequest, 
        settings: Annotated[Settings, Depends(get_settings)],
        temperature: float | int = 1
    ):
    word = request_data.word
    temperature = float(temperature)
    
    try:
        result = word_explainer(word, temperature)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request {str(e)}")


@router.post("/word_explorer/generate_sentences")
async def generate_sentences(
        request_data: WESentenceRequest,
        settings: Annotated[Settings, Depends(get_settings)], 
        temperature: float | int = 1
    ):
    word = request_data.word
    num_sentences = int(request_data.num_sentences)
    temperature = float(temperature)
    
    try:
        response = sentence_generator(word, num_sentences, temperature)
        return StreamingResponse(stream_tokens(response), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request {str(e)}")
