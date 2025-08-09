# app/model/consulta.py
from app.database import get_connection
from psycopg2 import sql

DDL = """
CREATE TABLE IF NOT EXISTS consulta (
  id          SERIAL PRIMARY KEY,
  cidade      TEXT NOT NULL,
  temperatura NUMERIC NOT NULL,
  tipo        TEXT NOT NULL,
  pokemon     TEXT NOT NULL,
  criado_em   TIMESTAMP NOT NULL DEFAULT NOW()
);
"""

def init_db():
    """Cria a tabela consulta se não existir."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(DDL)
        conn.commit()

def salvar_consulta(cidade: str, temperatura, tipo: str, pokemon: str):
    """Insere um registro na tabela consulta."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO consulta (cidade, temperatura, tipo, pokemon)
                VALUES (%s, %s, %s, %s)
                """,
                (cidade, float(temperatura), tipo, pokemon),
            )
        conn.commit()
