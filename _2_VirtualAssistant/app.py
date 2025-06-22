# This code is a FastAPI application that serves a virtual assistant.
# It includes an HTML interface for user interaction and handles requests to the Ollama API. 
# This can be further enhanced with AI agents to actually work with calendar APIs or other task management systems.   

# Import necessary libraries
from fastapi import FastAPI, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os
import json
import datetime

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# API Configuration
OLLAMA_URL = "http://127.0.0.1:1234/v1/completions"  # Updated URL for Ollama API
MODEL_NAME = "meta-llama-3.1-8b-instruct"  # Using this model for virtual assistant chatbot

# Store scheduled tasks in memory (for demonstration purposes)
scheduled_tasks = []

@app.get("/")
def serve_homepage():
    """ Serve the index.html file when accessing the root URL """
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/chat")
def chat_with_ai(user_query: str = Form(...)):
    headers = {"Content-Type": "application/json"}

    # Create a structured prompt for a customer support chatbot
    prompt = f"""You are a AI powered Virtual assistant that is capable of scheduling tasks and answering queries.
    You will respond to user queries in a helpful and concise manner. Only answer what the user asks. Do not generate follow-up questions or extra content.
    Only If the user specifically asks to schedule a specific task, you will extract the task details and save it.
    User: {user_query}
    Assistant:"""

    try:
        # Send the query to the Ollama API
        print("Sending request to LM Studio API with prompt:", prompt)
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False, "max_tokens": 150, "temperature": 0.02},
            headers=headers
        )

        result = response.json()
        # print the response for debugging
        print("Response from LM Studio API:", json.dumps(result, indent=2))
        
        # Extract the content from the response
        ai_response = result.get("choices", [{}])[0].get("text", "").strip('\n')
        print("ai_reponse:", ai_response)

        #check if the response contains a task to schedule  
        if "schedule" in user_query.lower() or "task" in user_query.lower():
            # Extract task details from the response
            task_details = user_query
            task_id = len(scheduled_tasks) + 1
            scheduled_task = {
                "id": task_id,
                "task": task_details,
                "scheduled_at": datetime.datetime.now().isoformat()
            }
            scheduled_tasks.append(scheduled_task)
            print(f"Scheduled Task: {scheduled_tasks}")

        return {"ai_response": ai_response, "tasks": scheduled_tasks} 
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LM Studio API: {str(e)}")

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)