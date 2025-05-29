import requests
import json
import time
import numpy as np
import faiss
from dotenv import load_dotenv
import os
# Load API Key
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
API_URL = os.getenv("API_URL")

print(API_KEY,API_URL)
def get_amazon_embedding(text: str) -> list:
    global API_KEY
    global API_URL
    payload = {
        "api_key": API_KEY,
        "prompt": text,
        "model_id": "amazon-embedding-v2"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return []

    result = response.json()
    embedding_vector = result["response"]["embedding"]
    return embedding_vector

# Load embeddings
with open("document_embeddings.json", "r") as f:
    saved_embeddings = json.load(f)

texts = [item["text"] for item in saved_embeddings]
vectors = np.array([item["embedding"] for item in saved_embeddings]).astype("float32")

# Create FAISS index
dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vectors)

print(f"🔎 Loaded {len(vectors)} embeddings into FAISS index.")

# Define search function
def search_query(query: str, k=10):
    query_embedding = get_amazon_embedding(query)
    text=''
    if not query_embedding:
        print("❌ Failed to get query embedding.")
        return
    D, I = index.search(np.array([query_embedding]).astype("float32"), k=k)
    for idx in I[0]:
        # print(texts[idx])
        text+=str(texts[idx])
    return text