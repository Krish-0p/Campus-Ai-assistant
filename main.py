from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json

app = FastAPI()

# Allow React frontend to access backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load context from data.json
def load_context(path="data.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return "\n".join([f"Q: {item['question']} A: {item['answer']}" for item in data])

context = load_context()

class Query(BaseModel):
    text: str

@app.post("/ask")
def ask_llama(query: Query):
    user_question = query.text

    prompt = f"""You are a helpful assistant for a college website. Use ONLY the information in the context below to answer. Do not say anything like "Based on the context provided" or try to explain why.

Context:
{context}

Question: {user_question}

Answer:"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )
        return {"answer": response.json()["response"]}
    except Exception as e:
        return {"error": str(e)}
