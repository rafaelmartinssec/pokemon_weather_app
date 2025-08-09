import sqlite3

with open("schema.sql", "r") as f:
    schema = f.read()

conn = sqlite3.connect("pokemon_weather.db")
conn.executescript(schema)
conn.close()
