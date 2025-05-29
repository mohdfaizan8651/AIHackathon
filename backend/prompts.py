import requests
import json
import time
import numpy as np
import faiss
from cloudemodel import llm
from dotenv import load_dotenv
import os
# Load API Key
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")


url = "https://quchnti6xu7yzw7hfzt5yjqtvi0kafsq.lambda-url.eu-central-1.on.aws/"

def intent(user_question):
    global url,api_key
    prompt = f'''
        You are an expert intent recognizer for a supply chain assistant system. You are working with two types of data:

        1. **Unstructured Document Topics** (e.g., policy documents, guidelines):
        - Inventory Management
        - Obsolete Inventory Handling
        - Health, Safety, and Environment (HSE)
        - Supplier Selection and Qualification
        - Supplier Code of Conduct (Ethical Sourcing)
        - Supplier Relationship Management
        - Sourcing and Procurement Practices
        - Capacity Planning
        - Demand Forecasting and Planning
        - Order Management
        - Transportation and Logistics Management
        - Warehouse and Storage Policy
        - Returns and Reverse Logistics
        - Risk Management and Mitigation
        - Business Continuity and Disaster Recovery
        - Trade Compliance and Regulations
        - Anti-Counterfeit and Product Authenticity
        - Data Security and Cybersecurity
        - Environmental Sustainability (Green Supply Chain)
        - Circular Economy and Waste Reduction
        - Performance Measurement (KPIs)
        - Technology Adoption (IoT, Blockchain)
        - Change Management in Supply Chains
        - Cost Reduction and Efficiency
        - Contract Management and Negotiation
        - Communication and Crisis Management
        - Labor Standards and Fair Labor Practices
        - Diversity in Supplier Base
        - Continuous Improvement and Innovation
        - Product Quality Assurance and Control

        2. **Structured Database Schema** (PostgreSQL):
        - **customers** (customer_id, fname, lname, email, password, segment, city, state, country, street, zipcode)
        - **departments** (department_id, department_name)
        - **categories** (category_id, category_name)
        - **products** (product_card_id, category_id, product_name, product_price, etc.)
        - **orders** (order_id, customer_id, order_date, shipping_date, shipping_mode, region, market, etc.)
        - **order_items** (order_item_id, order_id, product_id, quantity, discount, total, profit, etc.)
        - **shipping** (order_id, shipping durations, delivery status, risk)

        ---

        Your task is:

        - First, **identify the intent** of the question: Does it relate to:
        - `[Document Data]` (e.g., policy, safety, supplier guidelines)?
        - `[Structured Data]` (e.g., customer orders, delivery performance, product profit)?
        - `[Both]` if the question involves both.
        - `[unrelated]` if the question not first answer the question and related to datasets then force to asking question in a polite way?

        - Then, if applicable, **split the user question into two simplified sub-questions**: one for document data and one for structured data — in clear and simple language that a language model like LLaMA can understand and process.

        ---

        **Natural Language User Question**:
        \"\"\"{user_question}\"\"\"

        Return the result in this format:

        Intent: [Document Data] or [Structured Data] or [Both] or [Unrelated]

        If [Both], then:

        Document Question: ...

        Structured Question: ...

        Unrelated Question: ...

        '''

    response = llm._call(prompt)
    return response["response"]["content"][0]["text"]

def database(user_question):
    global api_key, url

    prompt =f"""
    You are an expert query writter working with a PostgreSQL supply chain database. The database contains the following tables and schemas:

    ---

    TABLE: customers
    - customer_id (TEXT, PK)
    - fname, lname, email, password, segment, city, state, country, street, zipcode

    TABLE: departments
    - department_id (INTEGER, PK)
    - department_name

    TABLE: categories
    - category_id (INTEGER, PK)
    - category_name

    TABLE: products
    - product_card_id (TEXT, PK)
    - product_category_id, category_id (FK to categories), description, image, product_name, product_price, product_status

    TABLE: orders
    - order_id (TEXT, PK)
    - customer_id (FK to customers), order_date, shipping_date, shipping_mode, status, city, state, country, zipcode, region, market, latitude, longitude, Type

    TABLE: order_items
    - order_item_id (TEXT, PK)
    - order_id (FK), product_id (FK), cardprod_id, quantity, discount, discount_rate, product_price, total, profit_ratio, profit_per_order, benefit_per_order, sales_per_customer

    TABLE: shipping
    - order_id (PK, FK to orders)
    - days_for_shipping_real, days_for_shipment_scheduled, delivery_status, late_delivery_risk

    ---

    Your task is to write accurate and optimized PostgreSQL SQL queries based on the following natural language question.

    ---

    Natural Language Question:
    \"\"\"{user_question}\"\"\"

    Write only the SQL query without any explanation and first understand the above tables giving then generate or write query. Use table joins appropriately and ensure syntax is correct.
    """
    response = llm._call(prompt)
    return response["response"]["content"][0]["text"]

def structured_ans(user_question, answer):
    global api_key, url

    prompt = f"""
    You are a helpful assistant.

    Given:
    - A user query: \"\"\"{user_question}\"\"\"
    - An initial answer: \"\"\"{answer}\"\"\"

    Your task:
    1. Understand the intent behind the user's question.
    2. Rephrase and improve the answer to be clear, concise, and informative.
    3. Present the final response in a professional and structured format and add some style .

    Output:
    Final Answer:
    """    
   
    response = llm._call(prompt)
    return response["response"]["content"][0]["text"]


def hybred(user_question, document_text):
    global api_key, url
    prompt = f"""
    You are an intelligent assistant helping with hybrid data queries involving both documents (policies, guidelines) and databases (structured data).

    structure data information use this for write postgres sql
    
    TABLE: customers
    - customer_id (TEXT, PK)
    - fname, lname, email, password, segment, city, state, country, street, zipcode

    TABLE: departments
    - department_id (INTEGER, PK)
    - department_name

    TABLE: categories
    - category_id (INTEGER, PK)
    - category_name

    TABLE: products
    - product_card_id (TEXT, PK)
    - product_category_id, category_id (FK to categories), description, image, product_name, product_price, product_status

    TABLE: orders
    - order_id (TEXT, PK)
    - customer_id (FK to customers), order_date, shipping_date, shipping_mode, status, city, state, country, zipcode, region, market, latitude, longitude, Type

    TABLE: order_items
    - order_item_id (TEXT, PK)
    - order_id (FK), product_id (FK), cardprod_id, quantity, discount, discount_rate, product_price, total, profit_ratio, profit_per_order, benefit_per_order, sales_per_customer

    TABLE: shipping
    - order_id (PK, FK to orders)
    - days_for_shipping_real, days_for_shipment_scheduled, delivery_status, late_delivery_risk in 0 or 1


    Task:
    1. Understand the user’s query.
    2. Analyze the given document or policy text to extract the required rule or condition.
    3. Use the extracted rule to construct a correct and optimized SQL query that answers the user's question.
    4. Explain both the rule and the SQL query clearly.

    ---

    User Query:
    \"\"\"{user_question}\"\"\"

    Document/Policy Text:
    \"\"\"{document_text}\"\"\"

    Respond in the following format:

    [Understanding]
    Summarize what the user wants.

    [Extracted Rule]
    State the rule, definition, or logic derived from the policy text that’s relevant to the query.

    [SQL Query]
    Write a precise SQL query based on the extracted rule.if  have a query write sql query  in this *** *** else write oonnoonn

    [Explanation]
    Briefly explain how the query answers the user’s question.
    """


    response = llm._call(prompt)
    return response["response"]["content"][0]["text"]

def user_role():
    global url, api_key

    prompt='''You are an intelligent assistant embedded in an enterprise system. Respond to user queries based strictly on their role and departmental affiliation. Follow these access rules:

Users in the Planning department can access information related to inventory, logistics, and forecasting.

Users in the Finance department can access margin reports, cost breakdowns, and profit & loss (P&L) data.

If a user requests data outside their role, respond with:
“Access to this information requires explicit cross-role authorization. Please contact your system administrator.”

Additional Instructions:

Never infer cross-department access unless it's explicitly authorized.

Respect fine-grained permissions based on user attributes such as department, role level, and access tags.

Log every query with the user’s role, requested data, timestamp, and access outcome (granted/denied).

Provide helpful guidance only within the user’s allowed scope. For example, suggest related Planning data if the user is in Planning and requests restricted Finance data.

Ensure the interaction remains smooth and context-aware while upholding strict access boundaries.'''

    payload = {
    "api_key": api_key,
    "prompt":  prompt,
    "model_id": "claude-3.5-sonnet",
    "model_params": {
    "max_tokens": 1024,
    "temperature": 0.7
    }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()

    return result["response"]["content"][0]["text"] 
#