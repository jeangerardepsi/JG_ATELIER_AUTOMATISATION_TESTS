
import requests
import time

def test_api_status_code():
    """Vérifie que l'API répond avec un code 200 (Succès)"""
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true"
    response = requests.get(url)
    assert response.status_code == 200

def test_api_performance():
    """Vérifie que l'API répond en moins de 1 seconde (Indicateur de Qualité)"""
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true"
    start_time = time.time()
    requests.get(url)
    duration = time.time() - start_time
    assert duration < 1.0

def test_api_data_structure():
    """Vérifie que la réponse contient bien les données météo attendues"""
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true"
    data = requests.get(url).json()
    assert "current_weather" in data
    assert "temperature" in data["current_weather"]
