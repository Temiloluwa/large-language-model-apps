from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class WEWordRequest(BaseModel):
    word: str = Field(title="Input word", max_length=20)

class WESentenceRequest(BaseModel):
    word: str = Field(title="Input word", max_length=20)
    num_sentences: int = Field(title="Number of sentences to generate", le=10, gt=0)


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    