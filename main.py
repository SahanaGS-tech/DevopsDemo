from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(title="Demo API", 
              description="A simple FastAPI application",
              version="1.0.0")

# Create a data model
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

# Sample data
items_db = [
    Item(id=1, name="Laptop", description="Powerful development machine", price=1299.99),
    Item(id=2, name="Smartphone", description="Latest model", price=799.99),
    Item(id=3, name="Headphones", price=149.99)
]

# Root endpoint
@app.get("/")
def read_root():
    # Intentionally introducing a failure
    raise HTTPException(status_code=500, detail="Intentional server error for testing purposes")

# Get all items
@app.get("/items", response_model=List[Item])
def read_items():
    return items_db

# Get a specific item by ID
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    return {"error": "Item not found"}

# Create a new item
@app.post("/items", response_model=Item)
def create_item(item: Item):
    items_db.append(item)
    return item
