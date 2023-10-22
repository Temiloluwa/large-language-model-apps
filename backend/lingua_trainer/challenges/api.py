from fastapi import APIRouter, HTTPException, Depends
from typing_extensions import Annotated
from functools import lru_cache
from .models import (WEWordRequest, WESentenceRequest, Settings)
from .word_explorer import (word_explanator, sentence_generator, get_llm)

router = APIRouter()

@lru_cache()
def get_settings():
    return Settings()


@router.post("/word_explorer/word_explainer")
async def explain(
        request_data: WEWordRequest,
        settings: Annotated[Settings, Depends(get_settings)], 
        temperature: float | int = 1
    ):
    word = request_data.word
    request_api_key = request_data.api_key
    temperature = float(temperature)
    
    try:
        api_key = settings.api_key if not request_api_key else request_api_key
        gpt = get_llm(api_key, temperature)
        result = word_explanator(word, gpt)
        return {
            "status": 200,
            "body": result
        }
        
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


@router.post("/word_explorer/generate_sentences")
async def generate_sentences(
        request_data: WESentenceRequest,
        settings: Annotated[Settings, Depends(get_settings)], 
        temperature: float | int = 1
    ):
    word = request_data.word
    num_sentences = int(request_data.num_sentences)
    request_api_key = request_data.api_key
    temperature = float(temperature)
    
    try:
        api_key = settings.api_key if not request_api_key else request_api_key
        gpt = get_llm(api_key, temperature)
        result = sentence_generator(word, num_sentences, gpt)
        return {
            "status": 200,
            "body": result
        }
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))