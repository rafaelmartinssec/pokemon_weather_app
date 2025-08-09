# 🌤️🔥 Pokemon Weather App ❄️🌪️

Aplicação **full stack** em arquitetura MVC que recomenda um Pokémon com base na temperatura atual da cidade informada, utilizando a **OpenWeather API** (One Call 3.0) e a **PokeAPI**.

---

## 📦 Tecnologias Utilizadas

- 🐍 **Python** (Flask)
- 🗃️ **SQLite3**
- 🌐 **HTML + CSS + JavaScript**
- ☁️ **OpenWeather API** (One Call 3.0)
- 🎮 **PokeAPI**
- 📁 **Arquitetura MVC**

---

## 📂 Estrutura de Pastas

```bash
pokemon_weather_app/
├── app/
│   ├── app.py
│   ├── controller/
│   │   ├── weather_controller.py
│   │   └── pokemon_controller.py
│   ├── model/
│   │   ├── database.py
│   │   └── consulta.py
│   └── view/
│       ├── templates/
│       │   └── index.html
│       └── static/
│           ├── css/
│           │   └── style.css
│           └── js/
│               └── script.js
├── schema.sql
├── requirements.txt
├── .env
├── README.md
└── config.py
```

---

## ⚙️ Configuração do Ambiente

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/pokemon_weather_app.git
cd pokemon_weather_app
```

### 2️⃣ Crie e ative o ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure o arquivo `.env`

Crie o arquivo `.env` na raiz do projeto:

```env
OPENWEATHER_API_KEY=sua_chave_aqui
UNITS=metric
LANG=pt_br
```

> 🔑 Sua chave pode ser obtida em: [https://home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys)

---

## 🗃️ Criar o Banco de Dados

**Via terminal:**
```bash
sqlite3 pokemon_weather.db < schema.sql
```

**Ou via Python:**
```bash
python app/model/database.py
```

---

## 🚀 Executar o Projeto

```bash
python app/app.py
```

Acesse: [http://localhost:5000](http://localhost:5000)

---

## 🔄 Fluxo da Aplicação

1. Usuário informa uma cidade.
2. Coordenadas obtidas via Geocoding da OpenWeather.
3. Temperatura atual consultada via One Call API 3.0.
4. Definição do tipo de Pokémon:
   - 🔥 > 30°C → Fogo
   - ❄️ < 0°C → Gelo
   - 🌱 0–30°C → Grama
5. Sorteio do Pokémon via PokeAPI.
6. Exibição do resultado.

---

## 🧠 Melhorias Futuras

- 🔐 Autenticação de usuários
- 📈 Histórico de consultas com gráficos
- 🌍 Suporte multilíngue
- 🧪 Testes automatizados (Pytest)
- ☁️ Deploy com Docker + CI/CD (GitHub Actions)

---

## 👨‍💻 Autor

**Rafael O Martins**  
Desenvolvedor Full Stack | Engenheiro de Computação  
[LinkedIn](https://www.linkedin.com/in/rafaelomartins)

---

## 📝 Licença

MIT © 2025 - Pokémon e OpenWeather
