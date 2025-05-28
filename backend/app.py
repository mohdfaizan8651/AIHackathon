from fastapi import FastAPI
from pydantic import BaseModel
from prompts import   intent, database, structured_ans,hybred
import os
from dotenv import load_dotenv
from database import *
from fastapi.middleware.cors import CORSMiddleware
import jsonify
from  amazonembeddingv2 import search_query
import re
from fassi import cover
# Load API Key
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Or ["*"] to allow all (not safe for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question:str
    history: str

# GET endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

import re

def extract_sql_from_response(response_text):
    """
    Extracts SQL query from the '[SQL Query]' section of the model's response.

    Args:
        response_text (str): The full LLM response that includes [SQL Query] and other sections.

    Returns:
        str: The extracted SQL query or a message if not found.
    """
    pattern = r"\[SQL Query\]\s*```sql(.*?)```"  # handles ```sql blocks
    match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    # fallback if not inside a code block
    pattern_alt = r"\[SQL Query\]\s*(.*?)(?:\n\[|\Z)"  # up to next section or end
    match_alt = re.search(pattern_alt, response_text, re.DOTALL | re.IGNORECASE)

    if match_alt:
        return match_alt.group(1).strip()

    return "SQL query not found in response."



def extract_explanation(response_text):
    # Extract content under [Explanation] section
    match = re.search(r"\[Explanation\]\s*(.*?)\s*(?=\[|$)", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "Explanation not found."

# POST endpoint
@app.post("/ask")
def ask_question(query:Query):
 
    intent_q= intent(query.question)
    intent_=str(intent_q.split('\n')[0].split('Intent: [')[1][:-1])
    
    if intent_== "Structured Data":
        answer=intent_q.split('\n')[2].split(str(intent_.split()[0])+' Question: ')[1].strip()
        cursor.execute(database(answer))
        rows = cursor.fetchall()
        solve = ''
        for row in rows:
            print(row)
            solve+=str(row)
        return json.dumps({"answer":structured_ans(answer,solve)})

    elif intent_== "Document Data":
        answer=intent_q.split('\n')[2].split(str(intent_.split()[0])+' Question: ')[1].strip()
        return json.dumps({"answer":structured_ans(answer,search_query(answer))})
    elif intent_ == "Both":

        Document=intent_q.split('\n')[2].split('Document Question: ')[1].strip()
        
        text = search_query(Document)
        answer = hybred(query,text)
        # return extract_sql_from_response(answer)
        cursor.execute(extract_sql_from_response(answer))
        explain_=extract_explanation(answer)
        rows = cursor.fetchall()
        solve = ''
        for row in rows:
            solve+=str(row)
        return json.dumps({"answer":structured_ans(query,str(solve) + explain_)})

    else:
        return json.dumps({"answer": intent_q.split('\n')[2].split('Unrelated Question: ')[1].strip()})
      
# curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d "{\"question\": \"What is the capital of France?\"}"