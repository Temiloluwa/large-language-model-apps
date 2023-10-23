from fastapi import APIRouter, HTTPException, Depends
from typing_extensions import Annotated
from functools import lru_cache
from fastapi.responses import StreamingResponse
from .models import (WEWordRequest, WESentenceRequest, Settings)
from .word_explorer import (word_explainer, sentence_generator, stream_examples)

router = APIRouter()

@lru_cache()
def get_settings():
    return Settings()


@router.post("/word_explorer/word_explainer")
async def explain(
        request_data: WEWordRequest, 
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
        temperature: float | int = 1
    ):
    word = request_data.word
    num_sentences = int(request_data.num_sentences)
    temperature = float(temperature)
    
    try:
        #api_key = settings.api_key if not request_api_key else request_api_key
        response = sentence_generator(word, num_sentences, temperature)
        return StreamingResponse(stream_examples(response, "}"), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request {str(e)}")
