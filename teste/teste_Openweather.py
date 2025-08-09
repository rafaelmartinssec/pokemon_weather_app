#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import requests
import requests_cache
from datetime import datetime
from dotenv import load_dotenv

# ---- Configuração ----
load_dotenv()  # lê OPENWEATHER_API_KEY do .env, se existir
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # defina no ambiente/.env
BASE_URL = "https://api.openweathermap.org"
UNITS = "metric"      # metric = °C
LANG = "pt_br"        # português do Brasil

# Cache de 10 minutos (evita bater limite à toa)
requests_cache.install_cache("ow_cache", expire_after=600)

# ---- Utilidades ----
class OpenWeatherError(Exception):
    pass

def _check_key():
    if not API_KEY:
        raise OpenWeatherError(
            "Defina a variável de ambiente OPENWEATHER_API_KEY (ou .env)."
        )

def _get(url, params=None, retry=2, backoff=1.5):
    """GET com retries simples e mensagens amigáveis."""
    if params is None:
        params = {}
    params["appid"] = API_KEY
    try:
        for attempt in range(retry + 1):
            resp = requests.get(url, params=params, timeout=15)
            # Se do cache, OK; se erro 429/5xx, tentar novamente
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < retry:
                time.sleep(backoff ** attempt)
                continue
            # Outros códigos: mostra mensagem da API se houver
            try:
                msg = resp.json().get("message", "")
            except Exception:
                msg = resp.text
            raise OpenWeatherError(
                f"Erro {resp.status_code} em {url}: {msg}".strip()
            )
    except requests.exceptions.RequestException as e:
        raise OpenWeatherError(f"Falha de rede ao acessar {url}: {e}") from e

# ---- Geocoding (cidade -> lat/lon) ----
def geocode_city(city, country=None, state=None, limit=1):
    """
    Converte nome da cidade em coordenadas usando o endpoint de geocoding.
    Exemplos:
      geocode_city('São Paulo', 'BR')
      geocode_city('Porto Alegre', 'BR', 'RS')
    """
    _check_key()
    q = city
    if state:
        q += f",{state}"
    if country:
        q += f",{country}"

    url = f"{BASE_URL}/geo/1.0/direct"
    data = _get(url, params={"q": q, "limit": limit})
    if not data:
        raise OpenWeatherError(f"Cidade não encontrada: {q}")
    return data[0]  # retorna o primeiro match

# ---- Clima atual ----
def get_current_weather_by_city(city, country=None, state=None):
    """
    Clima atual por cidade (usa geocoding por baixo dos panos).
    Retorna dicionário com campos relevantes.
    """
    loc = geocode_city(city, country, state)
    return get_current_weather_by_coord(lat=loc["lat"], lon=loc["lon"])

def get_current_weather_by_coord(lat, lon):
    """Clima atual por coordenadas."""
    _check_key()
    url = f"{BASE_URL}/data/2.5/weather"
    data = _get(url, params={"lat": lat, "lon": lon, "units": UNITS, "lang": LANG})
    return {
        "local": f'{data.get("name","")} / {data["sys"].get("country","")}'.strip(),
        "coord": data.get("coord", {}),
        "descricao": data["weather"][0]["description"].capitalize(),
        "temp": data["main"]["temp"],
        "sensacao": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],
        "umidade_%": data["main"]["humidity"],
        "vento_ms": data.get("wind", {}).get("speed"),
        "nuvens_%": data.get("clouds", {}).get("all"),
        "pressao_hpa": data["main"]["pressure"],
        "nascer_sol": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M"),
        "por_sol": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M"),
        "atualizado": datetime.fromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M"),
        "raw": data,  # opcional: payload completo
    }

# ---- Previsão 5 dias (3 h) ----
def get_forecast_by_city(city, country=None, state=None):
    loc = geocode_city(city, country, state)
    return get_forecast_by_coord(lat=loc["lat"], lon=loc["lon"])

def get_forecast_by_coord(lat, lon):
    """
    Previsão em blocos de 3 horas para ~5 dias (endpoint /forecast).
    Retorna lista resumida de registros úteis.
    """
    _check_key()
    url = f"{BASE_URL}/data/2.5/forecast"
    data = _get(url, params={"lat": lat, "lon": lon, "units": UNITS, "lang": LANG})
    items = []
    for f in data.get("list", []):
        items.append({
            "quando": datetime.fromtimestamp(f["dt"]).strftime("%Y-%m-%d %H:%M"),
            "descricao": f["weather"][0]["description"].capitalize(),
            "temp": f["main"]["temp"],
            "sensacao": f["main"]["feels_like"],
            "umidade_%": f["main"]["humidity"],
            "vento_ms": f.get("wind", {}).get("speed"),
            "nuvens_%": f.get("clouds", {}).get("all"),
            "pressao_hpa": f["main"]["pressure"],
            "chuva_mm": (f.get("rain", {}) or {}).get("3h", 0),
        })
    return {
        "local": f'{data.get("city", {}).get("name","")} / {data.get("city", {}).get("country","")}',
        "coord": data.get("city", {}).get("coord", {}),
        "itens": items,
        "raw": data,  # opcional
    }

# ---- CLI simples ----
def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python openweather_client.py 'Cidade' [Pais] [Estado]")
        print("Exemplos:")
        print("  python openweather_client.py 'São Paulo' BR")
        print("  python openweather_client.py 'Rio de Janeiro' BR RJ")
        sys.exit(1)

    city = sys.argv[1]
    country = sys.argv[2] if len(sys.argv) >= 3 else None
    state = sys.argv[3] if len(sys.argv) >= 4 else None

    try:
        atual = get_current_weather_by_city(city, country, state)
        print("=== Clima Atual ===")
        print(f"Local:        {atual['local']}")
        print(f"Tempo:        {atual['descricao']}")
        print(f"Temp:         {atual['temp']} °C (sensação {atual['sensacao']} °C)")
        print(f"Umidade:      {atual['umidade_%']}%")
        print(f"Vento:        {atual['vento_ms']} m/s")
        print(f"Nuvens:       {atual['nuvens_%']}%")
        print(f"Pressão:      {atual['pressao_hpa']} hPa")
        print(f"Sol:          nascer {atual['nascer_sol']} | pôr {atual['por_sol']}")
        print(f"Atualizado:   {atual['atualizado']}\n")

        prev = get_forecast_by_city(city, country, state)
        print("=== Previsão 5 dias (3h) ===")
        for item in prev["itens"][:12]:  # mostra próximos 12 blocos (~36h)
            print(
                f"{item['quando']} | {item['descricao']:<25} "
                f"{item['temp']:>5.1f}°C  "
                f"Umid {item['umidade_%']:>2}%  "
                f"Vento {item['vento_ms']} m/s  "
                f"Chuva {item['chuva_mm']} mm"
            )

    except OpenWeatherError as e:
        print(f"[ERRO] {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
