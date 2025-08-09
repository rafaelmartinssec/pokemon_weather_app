import requests
from config import OPENWEATHER_API_KEY

def get_temperature(cidade):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={OPENWEATHER_API_KEY}&units=metric"
    resp = requests.get(url).json()
    return resp['main']['temp']
