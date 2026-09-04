# weather_service.py
import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def obter_dados_climaticos(cidade):
    """Consulta a API do OpenWeather e identifica as condições atuais."""
    if not API_KEY:
        raise ValueError("Chave da API do OpenWeather não encontrada no .env")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    
    try:
        resposta = requests.get(url)
        resposta.raise_for_status() # Lança erro se o status não for 200
        dados = resposta.json()
        
        temp = dados["main"]["temp"]
        vento = dados["wind"]["speed"] * 3.6 # m/s para km/h
        condicao = dados["weather"][0]["main"].lower()
        descricao = dados["weather"][0]["description"]
        
        # Identificando eventos críticos
        evento = None
        if condicao in ["rain", "thunderstorm"]:
            evento = "Chuva Forte"
        elif vento > 40.0:
            evento = "Ventos Fortes"
        elif temp > 35.0:
            evento = "Calor Extremo"
        elif temp < 10.0:
            evento = "Frio Intenso"
            
        return {
            "temperatura": temp,
            "vento": vento,
            "descricao": descricao,
            "evento_relevante": evento
        }
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar clima para {cidade}: {e}")
        return None