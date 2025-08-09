import sqlite3

conn = sqlite3.connect('pokemon_weather.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("Tabelas existentes:", tabelas)

cursor.execute("PRAGMA table_info(consulta);")
colunas = cursor.fetchall()

print("Estrutura da tabela 'consulta':")
for coluna in colunas:
    print(coluna)

conn.close()
