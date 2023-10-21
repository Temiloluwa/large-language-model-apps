import os
from dotenv import load_dotenv
from queryverse.utils import ApiKeyNotFoundError


def get_api_key(api_key:str = None) -> str:
    """_summary_

    Args:
        api_key (str, optional): _description_. Defaults to None.

    Raises:
        ApiKeyNotFoundError: _description_

    Returns:
        str: _description_
    """
    
    if not api_key:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY", "")
    
    if api_key is None or not api_key:
        raise ApiKeyNotFoundError("API key not found")
    else:
        return api_key