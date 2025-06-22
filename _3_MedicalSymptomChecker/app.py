# This code is a FastAPI application that serves a medical symptom checker using medgemma-4b-it from Ollama.
# It includes an HTML interface for user interaction and handles requests to the Ollama API.
# This code and application is only for demonstration purposes and should not be used for actual medical advice.    

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
MODEL_NAME = "medgemma-4b-it"  # Using this model for customer support chatbot

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/analyze_symptoms")
def analyze_symptoms(symptoms: str = Form(...)):
    headers = {"Content-Type": "application/json"}

    prompt = f"""You are a medical AI assistant trained to analyze symptoms. 
    Based on the provided symptoms, give possible explanations and general advice. 
    Do not provide a diagnosis or replace a doctor's consultation.
    
    User Symptoms: {symptoms}
    
    Medical AI:"""

    try:
        # Send the symptoms to medgemma-4b-it
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
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)