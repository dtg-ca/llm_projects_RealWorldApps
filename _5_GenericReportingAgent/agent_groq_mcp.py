#This code attempts to put together a generic workflow using LLM working with 3 agents:
# Uses context server to capture context updates from each agent
# Uses Groq LLMs to collect, transform and generate output at the backend
# Three specific agents : 
# Data collector Agent - collects data based on user input 
# Data Transformer Agent - processes and anlyzes the collected data
# Output generator agent -  creates final output using combined inputs from the other agents
# Before running this code, ensure you have the Groq LLMs installed and running, and the MCP server (context_server.py) is running.

# MCP Client wrapper
import requests
import json
import os

class MCPClient:
    def __init__(self, base_url= "http://127.0.0.1:8000"):
        self.base_url = base_url

    def update_context(self, key, value):
        return requests.post(f"{self.base_url}/update_context/", json = { "key": key, "value": value }).json()
    def get_context(self, key):
        res = requests.get(f"{self.base_url}/get_context/{key}")
        return res.json().get(key) if res.status_code == 200 else None


from langchain_groq import ChatGroq

# Define Data collector Agent
class DataCollectorAgent:
    def __init__(self, mcp_client):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
        self.mcp = mcp_client

    def collect_data(self, user_input):
        prompt = f"Collect all the necessary information as required by the following: {user_input}"
        result = self.llm.invoke(prompt)
        #print(f"Result from LLM: {result}")
        result_text = result.content if hasattr(result, "content") else str(result)
        self.mcp.update_context("collected_data", result_text)
        return result_text    

# Define Data transformer Agent
class DataTransformerAgent:
    def __init__(self, mcp_client):
        self.llm = ChatGroq(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            temperature=0.2,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
        self.mcp = mcp_client

    def transform_data(self):
        collected_data = self.mcp.get_context("collected_data")
        prompt = f"Transform this data given into actionable insights: {collected_data}"
        result = self.llm.invoke(prompt)
        result_text = result.content if hasattr(result, "content") else str(result)
        self.mcp.update_context("transformed_data", result_text)
        return result_text 

# Define Output Generator Agent
class OutputGeneratorAgent:
    def __init__(self, mcp_client):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
        self.mcp = mcp_client

    def generated_output(self):
        transformed_data = self.mcp.get_context("transformed_data")
        prompt = f"Generate detailed output based on the following insights : {transformed_data}"
        result = self.llm.invoke(prompt)
        result_text = result.content if hasattr(result, "content") else str(result)
        self.mcp.update_context("final_output", result_text)
        return result_text

# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set Anthropic API key from environment variable
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


user_input = input("Enter what information you want me to collect, analyze and report on? (eg: GDP growth in India over last 10 years):")

# Main function to run the workflow
def main(user_input):       
    # Initialize MCP client
    mcp_client = MCPClient()

    # Initialize agents with MCP client
    data_collector = DataCollectorAgent(mcp_client)
    data_transformer = DataTransformerAgent(mcp_client)
    output_generator = OutputGeneratorAgent(mcp_client)

    # Step 1 - collect data
    collected_data = data_collector.collect_data(user_input)
    print(f"Collected data: {collected_data}")

    # Step 2 - transform data
    transformed_data = data_transformer.transform_data()
    print(f"Transformed data: {transformed_data}")

    # Step 3 - generate output
    final_output = output_generator.generated_output()
    #print(f"Final Output: {final_output}")

    return final_output

if __name__ == "__main__":
    final_output = main(user_input)
    print(f"Final Output: {final_output}")
