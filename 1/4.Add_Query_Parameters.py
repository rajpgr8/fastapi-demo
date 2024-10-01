from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI()

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
    fake_db[user.username] = user
    return {"message": "User created successfully", "user": user}

@app.get("/users/{username}", response_model=UserResponse)
async def get_user_by_username(username: str):
    user = fake_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User found", "user": user}

# Allow filtering users by email via query parameters.
@app.get("/users/", response_model=List[UserResponse])
async def get_users(email: Optional[str] = Query(None)):
    users = [user for user in fake_db.values() if not email or user.email == email]
    return [{"message": "Users found", "user": user} for user in users]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
