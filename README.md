### Imp Points:
- REST API -> FastAPI
- pydantic
- Starlette
- uvicorn

## Explanation of Key Features in main.py:

### Pydantic Models:

- **Item**: This model defines the structure of an item with fields like `name`, `price`, and `tax`.
- **ItemUpdate**: A model for updating items where all fields are optional. This allows partial updates.

### CRUD Operations:

- **Create Item**: `POST /items/` adds a new item to the in-memory database. If the item already exists, it raises a `400 Bad Request`.
- **Get All Items**: `GET /items/` returns a list of all items.
- **Get Single Item**: `GET /items/{item_name}` retrieves an item by its name, and raises `404 Not Found` if the item doesn't exist.
- **Update Item**: `PUT /items/{item_name}` updates an item with the new data provided.
- **Delete Item**: `DELETE /items/{item_name}` removes an item from the database.

### Background Tasks:

- A background task (`log_to_file`) is used to log the creation, update, or deletion of an item to a file. This simulates non-blocking operations like logging, sending emails, etc.

### Error Handling:

- **HTTPException**: This is used to return errors with appropriate status codes like `400 Bad Request` or `404 Not Found`.

### Auto-Generated Documentation:

- **Swagger UI**: Automatically available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
- **ReDoc**: Available at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).
 
![image](https://github.com/user-attachments/assets/a5bfcd80-bd80-444e-ad9b-a376a6b55a69)

![image](https://github.com/user-attachments/assets/6ccec502-d62c-4589-b8a0-835295a5d8a0)     

![image](https://github.com/user-attachments/assets/26e8bc85-cd91-4a2e-9310-01d940d46c02)    

### To Run
```
pip3 install fastapi uvicorn
python3 -m uvicorn main:app --reload
```

### To Test
```
pip3 install pytest pytest-asyncio httpx
python3 -m pytest -v
```
OR    
```
python3 requests.py
```
