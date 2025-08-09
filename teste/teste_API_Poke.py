import requests
import requests_cache

# Ativa cache (expira em 1 dia)
requests_cache.install_cache('pokeapi_cache', expire_after=86400)

BASE_URL = "https://pokeapi.co/api/v2/"

def buscar_dado(endpoint, identificador=None):
    """Busca dados na PokeAPI para um endpoint específico."""
    url = f"{BASE_URL}{endpoint}/"
    if identificador:
        url += f"{identificador}/"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro {response.status_code} ao acessar {url}")
        return None

def listar_todos(endpoint, limite=100):
    """Lista todos os registros de um endpoint, lidando com paginação."""
    url = f"{BASE_URL}{endpoint}/?limit={limite}&offset=0"
    resultados = []
    
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Erro {response.status_code} ao acessar {url}")
            break
        
        data = response.json()
        resultados.extend(data["results"])
        url = data["next"]  # Pega o próximo link da paginação
    
    return resultados

# Exemplo de uso: buscar informações do Pikachu
pikachu = buscar_dado("pokemon", "pikachu")
if pikachu:
    print("Nome:", pikachu["name"])
    print("Altura:", pikachu["height"])
    print("Peso:", pikachu["weight"])
    print("Habilidades:", [h["ability"]["name"] for h in pikachu["abilities"]])

# Exemplo: listar todas as berries
berries = listar_todos("berry", limite=50)
print(f"Total de berries encontradas: {len(berries)}")
