# This code is a FastAPI application that serves a customer support chatbot using the QWQ model from Ollama.
# It includes an HTML interface for user interaction and handles requests to the Ollama API.    

# Import necessary libraries
from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# API Configuration
OLLAMA_URL = "http://127.0.0.1:1234/v1/completions"  # Updated URL for Ollama API
MODEL_NAME = "qwq-32b"  # Using this model for customer support chatbot

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/chat")
def chat_with_ai(user_query: str = Form(...)):
    headers = {"Content-Type": "application/json"}

    # Create a structured prompt for a customer support chatbot
    prompt = f"""You are a customer support chatbot. Answer the user's question professionally and concisely.
    User: {user_query}
    Chatbot:"""

    try:
        # Send the query to QWQ
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
        print("reponse:", ai_response)        
        return {"response": ai_response}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LM Studio API: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)