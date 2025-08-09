# -*- coding: utf-8 -*-
import os, unicodedata, time, requests, requests_cache
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org"
UNITS = "metric"
LANG = "pt_br"
TIMEOUT = 15

requests_cache.install_cache("ow_cache", expire_after=600)
_session = requests.Session()
_session.headers.update({"User-Agent": "pokemon-weather-app/1.0"})

class WeatherError(Exception): pass

# apelidos úteis p/ locais “não-cidade”
SPECIAL_PLACES = {
    "polo sul":   {"lat": -90.0, "lon": 0.0, "label": "South Pole"},
    "south pole": {"lat": -90.0, "lon": 0.0, "label": "South Pole"},
    "polo norte": {"lat":  90.0, "lon": 0.0, "label": "North Pole"},
    "north pole": {"lat":  90.0, "lon": 0.0, "label": "North Pole"},
    "groenlandia": {"lat": 72.0, "lon": -40.0, "label": "Greenland"},
    "greenland":   {"lat": 72.0, "lon": -40.0, "label": "Greenland"},
    "antartida":   {"lat": -82.0, "lon": 0.0, "label": "Antarctica"},
    "antarctica":  {"lat": -82.0, "lon": 0.0, "label": "Antarctica"},
}

def _strip_accents(s:str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def _get(url, params):
    if not OPENWEATHER_API_KEY:
        raise WeatherError("OPENWEATHER_API_KEY não definida.")
    params = dict(params or {})
    params["appid"] = OPENWEATHER_API_KEY
    r = _session.get(url, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def _try_geo(q: str, limit=1):
    url = f"{BASE_URL}/geo/1.0/direct"
    return _get(url, {"q": q, "limit": limit})

def _geocode(city: str, country: str | None = None, state: str | None = None):
    q = city.strip()
    key = _strip_accents(q.lower())

    # 1) apelidos especiais
    if key in SPECIAL_PLACES:
        d = SPECIAL_PLACES[key]
        return d["lat"], d["lon"]

    # 2) busca normal (pt-br pode estar no corpus, mas o geocoding não usa lang)
    parts = [q]
    if state:   parts.append(state)
    if country: parts.append(country)
    query = ",".join(parts)
    data = _try_geo(query)
    if data:
        return data[0]["lat"], data[0]["lon"]

    # 3) fallback: sem acento / inglês
    alt = _strip_accents(query)
    if alt != query:
        data = _try_geo(alt)
        if data:
            return data[0]["lat"], data[0]["lon"]

    # 4) último recurso: tentar só a primeira palavra sem acento (ex: “Rio”)
    first = _strip_accents(q.split()[0])
    data = _try_geo(first)
    if data:
        return data[0]["lat"], data[0]["lon"]

    raise WeatherError(f"Cidade não encontrada: {city}")

def get_temperature(cidade: str | None, lat: float | None = None, lon: float | None = None,
                    country: str | None = None, state: str | None = None) -> float:
    """Retorna temperatura em °C para cidade OU coordenadas."""
    if lat is None or lon is None:
        if not cidade:
            raise WeatherError("Informe cidade ou lat/lon.")
        lat, lon = _geocode(cidade, country, state)

    url = f"{BASE_URL}/data/2.5/weather"
    data = _get(url, {"lat": lat, "lon": lon, "units": UNITS, "lang": LANG})
    return float(data["main"]["temp"])
