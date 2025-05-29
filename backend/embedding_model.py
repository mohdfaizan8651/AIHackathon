from langchain.embeddings.base import Embeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
import requests, json, os

# Custom embedding wrapper
class CustomHTTPEmbedding(Embeddings):
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            payload = {
                "api_key": self.api_key,
                "prompt": text,
                "model_id": "amazon-embedding-v2"
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                result = response.json()

                embeddings.append(result['response']['embedding'])  # Adjust if your key is different
            else:
                print(f"Error {response.status_code}: {response.text}")
                embeddings.append([0.0] * 768)
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

# Setup

