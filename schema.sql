CREATE TABLE IF NOT EXISTS consulta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cidade TEXT,
    temperatura REAL,
    tipo_pokemon TEXT,
    nome_pokemon TEXT,
    data_hora TIMESTAMP
);
