from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    message: str
    user: User

def get_user(user: User):
    return user

@app.post("/users/", response_model=UserResponse)
async def create_user(user: User = Depends(get_user)):
    return {"message": "User created successfully", "user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
