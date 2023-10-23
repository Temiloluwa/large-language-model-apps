from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class WEWordRequest(BaseModel):
    word: str = Field(title="Input word", max_length=20)
    #api_key: str | None = Field(title="API key", default=None)


class WESentenceRequest(BaseModel):
    word: str = Field(title="Input word", max_length=20)
    num_sentences: int = Field(title="Number of sentences to generate", le=10, gt=0)
    #api_key: str | None = Field(title="API key", default=None)


class Settings(BaseSettings):
    api_key: str = ""

    # update this to use docker secrets: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
    model_config = SettingsConfigDict(env_file=".env")
