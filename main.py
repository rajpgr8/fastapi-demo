from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# In-memory storage for items (simulating a database)
items_db = {}

# Pydantic model for Item
class Item(BaseModel):
    name: str
    price: float
    tax: Optional[float] = None

# Pydantic model for updating an item (all fields optional)
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None

# Background task to log actions to a file (simulating an async task)
def log_to_file(action: str, item_name: str):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{action} - Item: {item_name}\n")

@app.post("/items/", status_code=201)
def create_item(item: Item, background_tasks: BackgroundTasks):
    """Create a new item in the database"""
    if item.name in items_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    items_db[item.name] = item
    background_tasks.add_task(log_to_file, "Created", item.name)
    return {"message": "Item created successfully", "item": item}

@app.get("/items/", response_model=List[Item])
def get_items():
    """Get all items in the database"""
    return list(items_db.values())

@app.get("/items/{item_name}", response_model=Item)
def get_item(item_name: str):
    """Get an item by its name"""
    if item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_name]

@app.put("/items/{item_name}", response_model=Item)
def update_item(item_name: str, item_update: ItemUpdate, background_tasks: BackgroundTasks):
    """Update an item"""
    if item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update the item in the database
    stored_item = items_db[item_name]
    update_data = item_update.dict(exclude_unset=True)
    updated_item = stored_item.copy(update=update_data)
    items_db[item_name] = updated_item

    background_tasks.add_task(log_to_file, "Updated", item_name)
    return updated_item

@app.delete("/items/{item_name}")
def delete_item(item_name: str, background_tasks: BackgroundTasks):
    """Delete an item"""
    if item_name not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del items_db[item_name]
    background_tasks.add_task(log_to_file, "Deleted", item_name)
    return {"message": "Item deleted successfully"}

# Health check route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Item Management System"}
