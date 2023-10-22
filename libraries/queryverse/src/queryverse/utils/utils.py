import os
from dotenv import load_dotenv


def load_env_var(env_name: str = "OPENAI_API_KEY", 
                env_path: str | None = None) -> str:
    """
        Load an environment variable from a .env file

    Args:
        env_name: The name of the environment variable
        env_path: The path to the env file
    
    Returns:
        str: value of the environment variable
    """
    if env_path and os.path.exists(env_path):
        load_dotenv(env_path)

    else:
        load_dotenv()
    
    env_var = os.getenv(env_name, "")

    
    return env_var