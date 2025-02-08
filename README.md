### **🚀 Step-by-Step Guide to Create IKEA Chatbot API in Visual Studio (VS Code)**  
We'll **build a FastAPI backend** in **VS Code**, which fetches product data from **IKEA APIs**, processes it using **OpenAI GPT**, and allows filtering for large responses.

---

## **🔹 Step 1: Install Required Tools**
You need:
- **Python 3.9+** installed ([Download Here](https://www.python.org/downloads/))
- **VS Code** ([Download Here](https://code.visualstudio.com/))

### **🔹 Step 1.1: Install Required Python Libraries**
Open **VS Code Terminal** and run:
```sh
pip install fastapi uvicorn requests openai pydantic
```

---

## **🔹 Step 2: Create a FastAPI Project**
### **📁 Folder Structure**
Inside your project folder (`ikea-chatbot`), create:
```
ikea-chatbot/
│── main.py   # FastAPI server
│── requirements.txt
│── .env      # Store API keys securely
```

---

## **🔹 Step 3: Store API Keys Securely**
Inside `.env` file:
```
OPENAI_API_KEY=your-openai-api-key
IKEA_API_KEY=your-ikea-api-key
IKEA_SEARCH_URL=https://ikea-api.com/search
```

---

## **🔹 Step 4: Implement FastAPI in `main.py`**
Now, add this code in `main.py`:

```python
from fastapi import FastAPI, Query
import requests
import openai
import os
from dotenv import load_dotenv

# Load API Keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
IKEA_API_KEY = os.getenv("IKEA_API_KEY")
IKEA_SEARCH_URL = os.getenv("IKEA_SEARCH_URL")

app = FastAPI()

@app.get("/search_product")
def search_product(query: str = Query(..., description="Search query for IKEA products")):
    """
    Fetch product data from IKEA API, filter large results, and process with OpenAI.
    """
    headers = {"Authorization": f"Bearer {IKEA_API_KEY}"}
    response = requests.get(f"{IKEA_SEARCH_URL}?query={query}", headers=headers)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data from IKEA API"}
    
    ikea_data = response.json()
    
    # 🔹 Step 5: Filter Results (Reduce Large Responses)
    top_results = ikea_data.get("products", [])[:5]  # Limit to 5 products
    
    # 🔹 Step 6: Use OpenAI to Format the Response
    gpt_prompt = f"""
    You are an IKEA assistant. Format these search results into a user-friendly response:
    {top_results}
    """
    openai_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an IKEA product expert."},
            {"role": "user", "content": gpt_prompt}
        ],
        api_key=OPENAI_API_KEY
    )

    return {
        "query": query,
        "response": openai_response["choices"][0]["message"]["content"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## **🔹 Step 5: Run the API Server**
In **VS Code Terminal**, start the server:
```sh
uvicorn main:app --reload
```
**You should see output like:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## **🔹 Step 6: Test Your API**
Open your **browser** and visit:  
👉 `http://127.0.0.1:8000/docs`  
This will open **Swagger UI**, where you can test `search_product`.

Example test:  
`http://127.0.0.1:8000/search_product?query=sofa`

---

## **🔹 Step 7: Add Filtering Tools (If Response is Large)**
Since you **don’t use a vector database**, you can **add filtering** based on:
- **Price**: Only show products under a certain price.
- **Availability**: Show only “In Stock” items.
- **Color/Category**: Filter based on user preferences.

Modify `search_product()` like this:

```python
@app.get("/search_product")
def search_product(query: str, max_price: float = None, availability: str = None):
    """
    Fetch IKEA product data and allow filtering.
    """
    headers = {"Authorization": f"Bearer {IKEA_API_KEY}"}
    response = requests.get(f"{IKEA_SEARCH_URL}?query={query}", headers=headers)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data from IKEA API"}
    
    ikea_data = response.json().get("products", [])

    # 🔹 Apply Filtering
    if max_price:
        ikea_data = [p for p in ikea_data if float(p["price"].strip("$")) <= max_price]
    
    if availability:
        ikea_data = [p for p in ikea_data if p["availability"].lower() == availability.lower()]

    top_results = ikea_data[:5]  # Limit to 5 filtered products
    
    return {"filtered_results": top_results}
```
**Now you can search with filters:**  
👉 `http://127.0.0.1:8000/search_product?query=sofa&max_price=500&availability=in stock`

---

## **🔹 Step 8: Deploy the API**
- **To Cloud**: Use **AWS Lambda**, **Google Cloud Run**, or **Azure App Services**.
- **Dockerize** (Optional): Create a `Dockerfile` to package and deploy anywhere.
