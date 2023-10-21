import uvicorn
from fastapi import FastAPI
from .auth import auth_router
from .lingua_trainer import (users_router, words_router, challenges_router)
from .utils import load_api_kwargs

app =  FastAPI(**load_api_kwargs())

app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])
app.include_router(users_router, prefix="/api/v1/user", tags=["User"])
app.include_router(words_router, prefix="/api/v1/words", tags=["Words"])
app.include_router(challenges_router, prefix="/api/v1/challenges", tags=["Challenges"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
