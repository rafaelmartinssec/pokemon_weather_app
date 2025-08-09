# app/database.py
import os, psycopg2
from dotenv import load_dotenv
load_dotenv()  # lê .env na raiz

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST","localhost"),
        port=os.getenv("POSTGRES_PORT","5432"),
        dbname=os.getenv("POSTGRES_DB","pokemon_weather"),
        user=os.getenv("POSTGRES_USER","postgres"),
        password=os.getenv("POSTGRES_PASSWORD"),   # <-- ESSENCIAL
        connect_timeout=5,
    )
