from .database import conectar
from datetime import datetime

def salvar_consulta(cidade, temperatura, tipo, nome):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO consulta (cidade, temperatura, tipo_pokemon, nome_pokemon, data_hora)
        VALUES (?, ?, ?, ?, ?)
    """, (cidade, temperatura, tipo, nome, datetime.now()))
    conn.commit()
    conn.close()
