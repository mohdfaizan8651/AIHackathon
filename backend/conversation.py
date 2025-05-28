from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from cloudemodel import llm
from langchain.memory import VectorStoreRetrieverMemory


# memory = ConversationBufferWindowMemory(k=3)


# faiss_store = FAISS.from_texts(
#     texts=["Faizan lives in Bangalore.", "Faizan is working on an AI agent."],
#     embedding=embedding
# )

# retriever = faiss_store.as_retriever(search_kwargs={"k": 3})
# results = retriever.get_relevant_documents("Where does Faizan live?")

memory = VectorStoreRetrieverMemory(
    retriever=faiss_store.as_retriever(search_kwargs={"k": 3}),
    memory_key="history"  # used internally by LangChain
)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Example loop
while True:
    user_input = input("You: ")
    response = conversation.run(user_input)
    print("Claude:", response)