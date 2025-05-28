import psycopg2
import requests
import json

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="DataCoSupplyChainDataset",
    user="postgres",
    password="umra",
    host="localhost",
    port="5432"  # default PostgreSQL port
)
cursor = conn.cursor()
#