import sqlite3

def conectar():
    conn = sqlite3.connect('pokemon_weather.db')
    conn.row_factory = sqlite3.Row
    return conn
