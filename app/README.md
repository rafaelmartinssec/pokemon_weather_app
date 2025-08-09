---

## 📄 README.md

````markdown
# Pokémon Weather App

Aplicação em Python que integra dados meteorológicos e informações da PokéAPI, exibindo temperatura e condições climáticas com interface web (Flask).

## 🚀 Funcionalidades
- Consulta da temperatura atual de uma cidade.
- Integração com APIs de clima e PokéAPI.
- Armazenamento das consultas no PostgreSQL.
- Cache local para otimizar consultas repetidas.

---

## 🛠️ Tecnologias
- **Python 3.10+**
- **Flask**
- **PostgreSQL**
- **Requests + Requests Cache**
- **psycopg2**

---

## 📦 Instalação

1. **Clonar o repositório**
   ```bash
   git clone https://github.com/SEU_USUARIO/pokemon_weather_app.git
   cd pokemon_weather_app
````

2. **Criar e ativar ambiente virtual**

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Instalar dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar banco de dados PostgreSQL**

   * Criar banco:

     ```sql
     CREATE DATABASE pokemon_weather;
     ```
   * Criar usuário (se necessário):

     ```sql
     CREATE USER postgres WITH PASSWORD 'SUA_SENHA';
     GRANT ALL PRIVILEGES ON DATABASE pokemon_weather TO postgres;
     ```

5. **Configurar variáveis de ambiente (.env)**
   Na raiz do projeto, crie o arquivo `.env`:

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=pokemon_weather
   DB_USER=postgres
   DB_PASSWORD=SUA_SENHA
   ```

6. **Iniciar aplicação**

   ```bash
   python -m app.main
   ```

   A aplicação estará disponível em:
   `http://127.0.0.1:5000`

---

## 📊 Consultas no banco

Para visualizar os dados salvos:

```sql
SELECT * FROM consulta ORDER BY data_consulta DESC;
```

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais informações.

````

---

## 📌 Commit e Push no GitHub

No PowerShell ou terminal:
```bash
# Adicionar todos os arquivos
git add .

# Criar commit
git commit -m "feat: primeira versão do Pokemon Weather App"

# Enviar para o GitHub
git push origin main
````

Se for o **primeiro push**:

```bash
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/pokemon_weather_app.git
git push -u origin main
```

---
