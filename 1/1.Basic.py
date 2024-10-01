from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for the data
class User(BaseModel):
    username: str
    email: str

# Create a dependency that validates user data
def get_user(user: User):
    return user

# Define a route that uses the dependency
@app.post("/users/")
async def create_user(user: User = Depends(get_user)):
    return {"username": user.username, "email": user.email}

