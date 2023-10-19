import os
from dotenv import load_dotenv
from queryverse.utils import ApiKeyNotFoundError

load_dotenv()

def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key is None:
        raise ApiKeyNotFoundError("API key not found")
    return api_key