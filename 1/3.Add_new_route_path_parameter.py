from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class User(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    message: str
    user: User

# In-memory "database"
fake_db: Dict[str, User] = {}

def get_user(user: User):
    return user

@app.post("/users/", response_model=UserResponse)
async def create_user(user: User = Depends(get_user)):
    fake_db[user.username] = user
    return {"message": "User created successfully", "user": user}

# Introduce a route to fetch user details using path parameters.
@app.get("/users/{username}", response_model=UserResponse)
async def get_user_by_username(username: str):
    user = fake_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User found", "user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
