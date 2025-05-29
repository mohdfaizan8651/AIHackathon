from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from embedding_model import CustomHTTPEmbedding
# Setup your custom embedding

API_URL = "https://quchnti6xu7yzw7hfzt5yjqtvi0kafsq.lambda-url.eu-central-1.on.aws/"
API_KEY = "syn-7f22e2ef-6003-4f20-9fff-23aa8729c29c"


embedding = CustomHTTPEmbedding(api_url=API_URL, api_key=API_KEY)

# # Example chats
def cover(conversations,query="What you name"):
   

    docs = [Document(page_content=c) for c in conversations]
    # # Create and save FAISS
    faiss_store = FAISS.from_documents(docs, embedding)
    faiss_store.save_local("faiss_index")


    # Load FAISS later
    faiss_store = FAISS.load_local("faiss_index", embedding,allow_dangerous_deserialization=True)
    retriever = faiss_store.as_retriever(search_kwargs={"k": 2})

    results = retriever.get_relevant_documents(query)
    for doc in results:
        print(doc.page_content)
    return results
