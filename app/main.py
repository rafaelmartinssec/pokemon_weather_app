from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from app.controller.weather_controller import get_temperature
from app.controller.pokemon_controller import tipo_por_temperatura, get_pokemon_por_tipo
from app.model.consulta import salvar_consulta, init_db


import logging

# Carrega variáveis do .env
load_dotenv()

# Informa ao Flask onde estão templates/estáticos
app = Flask(
    __name__,
    template_folder="view/templates",
    static_folder="view/static",
    static_url_path="/static",
)

# ---- Logging básico ----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- Helpers de erro ----
def error_response(message, status=400, extra=None):
    payload = {"error": message}
    if extra:
        payload.update(extra)
    return jsonify(payload), status

@app.errorhandler(404)
def not_found(_e):
    return error_response("Rota não encontrada.", 404)

@app.errorhandler(500)
def server_error(e):
    logger.exception("Erro interno não tratado: %s", e)
    return error_response("Erro interno do servidor.", 500)

# ---- Rotas ----
@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/consulta")
def consulta():
    data = request.get_json(silent=True) or {}
    cidade = (data.get("cidade") or "").strip()
    lat = data.get("lat")
    lon = data.get("lon")

    if not cidade and (lat is None or lon is None):
        return error_response("Informe 'cidade' OU 'lat' e 'lon'.", 422)

    # 1) Clima (com suporte a coordenadas)
    try:
        if lat is not None and lon is not None:
            temp = get_temperature(None, lat=lat, lon=lon)
            cidade_label = cidade or f"{lat},{lon}"
        else:
            temp = get_temperature(cidade)
            cidade_label = cidade
    except Exception as e:
        logger.exception("Falha ao obter temperatura para %r: %s", cidade or (lat, lon), e)
        return error_response(
            "Não achei esse local. Tente digitar de outro jeito ou escolha na busca de cidades.",
            502,
            {"dica": "Use o endpoint /api/cidades?q=<termo> (se disponível) para selecionar um resultado válido."}
        )

    # 2) Pokémon pelo tipo climático
    try:
        tipo = tipo_por_temperatura(float(temp))
        nome, imagem = get_pokemon_por_tipo(tipo)
    except Exception as e:
        logger.exception("Falha ao obter Pokémon por tipo %r: %s", tipo, e)
        return error_response("Não foi possível selecionar um Pokémon para o clima.", 502, {"detalhe": str(e)})

    # 3) Persistência (não quebra a resposta se falhar)
    try:
        salvar_consulta(cidade_label, temp, tipo, nome)
    except Exception as e:
        logger.warning("Falha ao salvar consulta: %s", e)

    return jsonify({
        "cidade": cidade_label,
        "temperatura": temp,
        "tipo": tipo,
        "pokemon": nome,
        "imagem": imagem
    }), 200

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # Cria a tabela se não existir
    try:
        init_db()
        logger.info("Banco inicializado/verificado com sucesso.")
    except Exception as e:
        logger.exception("Falha ao inicializar o banco: %s", e)

    app.run(debug=True)
