# This code is a FastAPI application that serves a product recommender using granite 3.2:8b from Ollama.
# It includes an HTML interface for user interaction and handles requests to the Ollama API.
# This code and application is only for demonstration purposes and should not be used for actual medical advice. 

from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json
import pandas as pd

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# API Configuration
OLLAMA_URL = "http://127.0.0.1:1234/v1/completions"  # Updated URL for Ollama API
MODEL_NAME = "ibm/granite-3.2-8b"  # Using this model for customer support chatbot


# Sample Product Database (Can be expanded)
products = [
    {"id": 1, "category": "Electronics", "name": "Wireless Earbuds"},
    {"id": 2, "category": "Electronics", "name": "Smartphone"},
    {"id": 3, "category": "Electronics", "name": "Laptop"},
    {"id": 4, "category": "Fashion", "name": "Leather Jacket"},
    {"id": 5, "category": "Fashion", "name": "Running Shoes"},
    {"id": 6, "category": "Home", "name": "Smart Vacuum Cleaner"},
    {"id": 7, "category": "Home", "name": "Air Purifier"},
]

# Convert to DataFrame for easy filtering
df = pd.DataFrame(products)

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/recommend")
def recommend_products(preferences: str = Form(...)):
    headers = {"Content-Type": "application/json"}

    # Generate recommendation prompt
    prompt = f"""You are an AI product recommender. Based on the user's preferences, suggest the best matching products.
    
    User Preferences: {preferences}
    
    Recommended Products:
    """

    try:
        # Send preferences to Granite 3.2 for recommendations
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            headers=headers
        )

        result = response.json()
        # print the response for debugging
        print("Response from LM Studio API:", json.dumps(result, indent=2))

        # Extract the content from the response
        ai_response = result.get("choices", [{}])[0].get("text", "")
        print("recommendations:", ai_response)        
        return {"recommendations": ai_response}
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LM Studio API: {str(e)}")

    

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
