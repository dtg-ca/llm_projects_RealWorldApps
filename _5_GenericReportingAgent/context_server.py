from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os   
from typing import Dict, Any

# Initialize FastAPI app
app = FastAPI()

# shared context stored as a dictionary
shared_context: Dict[str, Any] = {}

# Define a Pydantic model for updating context
class ContextUpdate(BaseModel):
    key: str
    value: Any

# Endpoint to update shared context 
@app.post("/update_context")
async def update_context(update: ContextUpdate):
    """
    Update the shared context with a new key-value pair.
    """
    try:
        shared_context[update.key] = update.value
        return {"message": "Context updated successfully", "context": shared_context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint to retrieve the entire shared context
@app.get("/get_context")
async def get_context():
    """
    Retrieve the current shared context.
    """
    try:
        return {"context": shared_context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to retrieve a specific key from the shared context
@app.get("/get_context/{key}")
async def get_context_key(key: str):
    """
    Retrieve the value for a specific key in the shared context.
    """
    try:
        value = shared_context.get(key, None)
        if value is None:
            raise HTTPException(status_code=404, detail=f"Key '{key}' not found in context.")
        return {key: value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))