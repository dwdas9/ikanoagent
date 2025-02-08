from fastapi import FastAPI, Query
import requests
import openai
from typing import Dict, Any

app = FastAPI()

# Configure OpenAI API Key
OPENAI_API_KEY = "your-openai-api-key"
IKEA_API_KEY = "your-ikea-api-key"
IKEA_SEARCH_URL = "https://ikea-api.com/search"

@app.get("/search_product")
def search_product(query: str = Query(..., description="Search query for IKEA products")):
    """
    Calls IKEA's product search API and reformats response using OpenAI.
    """
    # Step 1: Fetch data from IKEA API
    headers = {"Authorization": f"Bearer {IKEA_API_KEY}"}
    response = requests.get(f"{IKEA_SEARCH_URL}?query={query}", headers=headers)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data from IKEA API"}
    
    ikea_data = response.json()
    
    # Step 2: Process response using OpenAI for better readability
    gpt_prompt = f"""
    You are an IKEA shopping assistant. Reformat the following product search results into a clear, user-friendly response:
    {ikea_data}
    """
    openai_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful IKEA product assistant."},
            {"role": "user", "content": gpt_prompt}
        ],
        api_key=OPENAI_API_KEY
    )
    
    # Step 3: Return final chatbot response
    return {
        "query": query,
        "response": openai_response["choices"][0]["message"]["content"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
