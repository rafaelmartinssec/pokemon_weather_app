import requests
import random
from config import POKEAPI_BASE_URL

def tipo_por_temperatura(temp):
    if temp <= 0:
        return "ice"
    elif temp <= 15:
        return "water"
    elif temp <= 30:
        return "grass"
    else:
        return "fire"

def get_pokemon_por_tipo(tipo):
    url = f"{POKEAPI_BASE_URL}/type/{tipo}"
    resp = requests.get(url).json()
    pokemons = resp['pokemon']
    escolhido = random.choice(pokemons)
    nome = escolhido['pokemon']['name']
    img_url = get_pokemon_imagem(nome)
    return nome, img_url

def get_pokemon_imagem(nome):
    data = requests.get(f"{POKEAPI_BASE_URL}/pokemon/{nome}").json()
    return data['sprites']['front_default']
