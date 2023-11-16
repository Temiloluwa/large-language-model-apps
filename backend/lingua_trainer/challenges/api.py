import os
import base64
from typing import Annotated
from functools import lru_cache
from fastapi import APIRouter, HTTPException, Depends
from queryverse.llm import OpenAILLM
from fastapi.responses import StreamingResponse
from .models import (WEWordRequest, WESentenceRequest, Settings)
from .word_explorer import (word_explainer, sentence_generator, stream_tokens)

router = APIRouter()


@lru_cache
def get_gpt():
    """ Get LLM for lingua trainer"""
    # set open api key as environmental variable from docker secrets
    api_key = Settings().OPENAI_API_KEY
    # decode base64 encode string
    os.path.environ["OPENAI_API_KEY"] = base64.b64decode(api_key).decode("utf-8")
    gpt = OpenAILLM(is_async=True)
    
    return gpt


@router.post("/word_explorer/word_explainer")
async def explain(
        request_data: WEWordRequest, 
        temperature: float | int = 1,
        gpt: Annotated[OpenAILLM, Depends(get_gpt)]):
    word = request_data.word
    temperature = float(temperature)
    
    try:
        result = await word_explainer(gpt, word, temperature)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request {str(e)}")


@router.post("/word_explorer/generate_sentences")
async def generate_sentences(
        request_data: WESentenceRequest,
        temperature: float | int = 1,
        gpt: Annotated[OpenAILLM, Depends(get_gpt)]):

    word = request_data.word
    num_sentences = int(request_data.num_sentences)
    temperature = float(temperature)
    
    try:
        response = await sentence_generator(gpt, word, num_sentences, temperature)
        return StreamingResponse(stream_tokens(response), media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad Request {str(e)}")
