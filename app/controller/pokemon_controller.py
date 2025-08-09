# app/controller/pokemon_controller.py
import os
import random
import requests
import requests_cache
from dotenv import load_dotenv

# ---------- Config ----------
load_dotenv()
POKEAPI_BASE_URL = os.getenv("POKEAPI_BASE_URL", "https://pokeapi.co/api/v2").rstrip("/")
TIMEOUT = 15  # segundos
LANG_CODE = "pt-BR"  # tenta exibir nome em PT-BR (fallback para EN/slug)
MAX_TRIES = 12       # tentativas para achar um Pokémon com sprite

# Cache de 10 minutos (reduz latência e carga na API)
requests_cache.install_cache("pokeapi_cache", expire_after=600)

# Sessão com cabeçalho amigável
_session = requests.Session()
_session.headers.update({"User-Agent": "pokemon-weather-app/1.0 (+https://example.local)"})

# ---------- Util ----------
class PokeAPIError(Exception):
    pass

def _get(url, params=None):
    try:
        resp = _session.get(url, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise PokeAPIError(f"Falha ao acessar {url}: {e}")

def _best_sprite(sprites: dict) -> str | None:
    if not sprites:
        return None
    other = sprites.get("other") or {}
    # official artwork
    official = (other.get("official-artwork") or {}).get("front_default")
    if official:
        return official
    # dream world (svg)
    dream = (other.get("dream_world") or {}).get("front_default")
    if dream:
        return dream
    # front_default
    return sprites.get("front_default")

def _display_name_ptbr(species_data: dict, fallback: str) -> str:
    """Tenta pegar o nome em PT-BR; se não achar, usa fallback."""
    try:
        for n in species_data.get("names", []):
            if n.get("language", {}).get("name") == "pt-BR":
                return n.get("name") or fallback
    except Exception:
        pass
    return fallback

# ---------- Regras de negócio ----------
def tipo_por_temperatura(temp: float) -> str:
    """Mapeia temperatura (°C) -> tipo do Pokémon na PokeAPI."""
    if temp <= 0:
        return "ice"
    elif temp <= 15:
        return "water"
    elif temp <= 30:
        return "grass"
    else:
        return "fire"

def get_pokemon_por_tipo(tipo: str) -> tuple[str, str]:
    """
    Retorna (nome_exibicao, img_url) de um Pokémon aleatório do tipo informado.
    Pula entradas sem sprite válido.
    """
    tipo = (tipo or "").strip().lower()
    if not tipo:
        raise PokeAPIError("Tipo inválido.")

    url = f"{POKEAPI_BASE_URL}/type/{tipo}"
    data = _get(url)

    entries = data.get("pokemon") or []
    if not entries:
        raise PokeAPIError(f"Nenhum Pokémon encontrado para o tipo '{tipo}'.")

    # Aleatoriza a ordem e tenta achar um com sprite
    random.shuffle(entries)

    tries = 0
    for entry in entries:
        if tries >= MAX_TRIES:
            break
        tries += 1

        name_slug = entry.get("pokemon", {}).get("name")
        if not name_slug:
            continue

        # Detalhes do Pokémon (sprites)
        poke_url = f"{POKEAPI_BASE_URL}/pokemon/{name_slug}"
        poke_data = _get(poke_url)
        img_url = _best_sprite(poke_data.get("sprites"))
        if not img_url:
            continue  # sem sprite, tenta outro

        # Nome legível (tenta species em PT-BR)
        species_url = poke_data.get("species", {}).get("url")
        display_name = name_slug
        if species_url:
            species_data = _get(species_url)
            display_name = _display_name_ptbr(species_data, fallback=name_slug.capitalize())
        else:
            display_name = name_slug.capitalize()

        return display_name, img_url

    # Se chegou aqui, não achou sprite válido
    raise PokeAPIError(f"Não foi possível encontrar sprite válido para o tipo '{tipo}' após {MAX_TRIES} tentativas.")

def get_pokemon_imagem(nome: str) -> str:
    """
    Retorna a melhor URL de imagem disponível para o Pokémon:
    - official-artwork (preferido)
    - dream_world
    - front_default (fallback)
    """
    if not nome:
        raise PokeAPIError("Nome de Pokémon inválido.")

    url = f"{POKEAPI_BASE_URL}/pokemon/{nome}"
    data = _get(url)
    img = _best_sprite(data.get("sprites"))
    if not img:
        raise PokeAPIError(f"Sem sprite disponível para '{nome}'.")
    return img
