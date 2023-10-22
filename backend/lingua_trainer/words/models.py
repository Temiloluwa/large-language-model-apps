from pydantic import BaseModel

class Word(BaseModel):
    user_id: str
    word_value: str