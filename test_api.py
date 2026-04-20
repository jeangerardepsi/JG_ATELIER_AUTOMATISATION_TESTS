import requests
import time

def test_api_status_code():
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true"
    response = requests.get(url)
    assert response.status_code == 200

def test_api_performance():
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true"
    start = time.time()
    requests.get(url)
    duration = time.time() - start
    # On teste si l'API répond en moins d'une seconde
    assert duration < 1.0
