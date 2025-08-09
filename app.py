from flask import Flask, request, jsonify, render_template
from controller.weather_controller import get_temperature
from controller.pokemon_controller import tipo_por_temperatura, get_pokemon_por_tipo
from model.consulta import salvar_consulta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/consulta', methods=['POST'])
def consulta():
    data = request.get_json()
    cidade = data.get('cidade')

    temp = get_temperature(cidade)
    tipo = tipo_por_temperatura(temp)
    nome, imagem = get_pokemon_por_tipo(tipo)
    
    salvar_consulta(cidade, temp, tipo, nome)
    
    return jsonify({
        "temperatura": temp,
        "tipo": tipo,
        "pokemon": nome,
        "imagem": imagem
    })

if __name__ == '__main__':
    app.run(debug=True)
