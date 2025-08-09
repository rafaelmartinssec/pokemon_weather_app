# test_pokemon.py
from app.controller.pokemon_controller import (
    tipo_por_temperatura, get_pokemon_por_tipo
)

def testar(temp):
    tipo = tipo_por_temperatura(temp)
    nome, img = get_pokemon_por_tipo(tipo)
    print(f"Temp: {temp}°C  -> tipo: {tipo}")
    print(f"Pokémon sorteado: {nome}")
    print(f"Imagem: {img}\n")

if __name__ == "__main__":
    for t in (-2, 10, 25, 33):
        testar(t)
