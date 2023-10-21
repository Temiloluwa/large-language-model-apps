from pydantic import BaseModel

class UserProfile(BaseModel):
    user_id: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    username: str 
    email: str 
    password: str
