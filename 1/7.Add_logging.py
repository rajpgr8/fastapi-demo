from fastapi import FastAPI, Depends, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    message: str
    user: User

fake_db: Dict[str, User] = {}

def get_user(user: User):
    return user

@app.post("/users/", response_model=UserResponse)
async def create_user(user: User = Depends(get_user)):
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="Username already taken")
    fake_db[user.username] = user
    logger.info(f"User created: {user.username}")
    return {"message": "User created successfully", "user": user}

@app.get("/users/{username}", response_model=UserResponse)
async def get_user_by_username(username: str):
    user = fake_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User found", "user": user}

@app.get("/users/", response_model=List[UserResponse])
async def get_users(email: Optional[str] = Query(None)):
    users = [user for user in fake_db.values() if not email or user.email == email]
    return [{"message": "Users found", "user": user} for user in users]

# Custom exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)