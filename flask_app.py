from flask import Flask, render_template_string
import requests
import time
from datetime import datetime

app = Flask(__name__)

# Configuration des destinations
VILLES = [
    {"nom": "Courbevoie 🏢", "lat": "48.8973", "lon": "2.2522"},
    {"nom": "Cannes 🎬", "lat": "43.5513", "lon": "7.0128"},
    {"nom": "Monaco 🏎️", "lat": "43.7383", "lon": "7.4245"},
    {"nom": "Saint-Tropez 🛥️", "lat": "43.2680", "lon": "6.6440"},
    {"nom": "Biarritz 🏄", "lat": "43.4831", "lon": "-1.5586"}
]

@app.route('/')
def dashboard():
    resultats = []
    labels_graphe = []
    temps_graphe = []
    ressenti_graphe = []
    
    for ville in VILLES:
        # Ajout du paramètre apparent_temperature
        url = f"https://api.open-meteo.com/v1/forecast?latitude={ville['lat']}&longitude={ville['lon']}&current_weather=true&hourly=apparent_temperature"
        try:
            response = requests.get(url, timeout=5).json()
            temp = response['current_weather']['temperature']
            # On récupère le ressenti actuel
            ressenti = response['hourly']['apparent_temperature'][0]
            status, color = "OPÉRATIONNEL", "#4ade80"
        except:
            temp, ressenti, status, color = 0, 0, "ERREUR", "#f87171"
        
        resultats.append({**ville, "status": status, "temp": temp, "ressenti": ressenti, "color": color})
        labels_graphe.append(ville['nom'])
        temps_graphe.append(temp)
        ressenti_graphe.append(ressenti)

    html_template = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Lux Monitoring 🇫🇷</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #0f172a; color: #f8fafc; padding: 20px; margin: 0; }}
            .container {{ max-width: 1000px; margin: auto; }}
            .fr-bar {{ height: 12px; width: 100%; display: flex; position: fixed; top: 0; left: 0; z-index: 1000; border-bottom: 1px solid white; }}
            .blue {{ background-color: #002395; flex: 1; }} .white {{ background-color: #ffffff; flex: 1; }} .red {{ background-color: #ed2939; flex: 1; }}
            .btn-group {{ margin: 30px 0; display: flex; gap: 10px; }}
            .btn {{ background-color: #002395; color: white; padding: 10px 15px; border-radius: 4px; text-decoration: none; font-weight: bold; border: 2px solid white; }}
            .card {{ background-color: #1e293b; padding: 20px; border-radius: 12px; border-top: 8px solid #ed2939; margin-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; background: #0f172a; margin-bottom: 20px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #334155; }}
            canvas {{ background: #1e293b; padding: 20px; border-radius: 12px; }}
        </style>
    </head>
    <body>
        <div class="fr-bar"><div class="blue"></div><div class="white"></div><div class="red"></div></div>
        <div class="container">
            <h1 style="margin-top:40px;">🇫🇷 Monitoring Luxe & Prestige</h1>
            
            <div class="btn-group">
                <a href="/" class="btn">⚡ ACTUALISER</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.access.log" target="_blank" class="btn" style="background:#334155;">Access Log</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.error.log" target="_blank" class="btn" style="background:#334155;">Error Log</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.server.log" target="_blank" class="btn" style="background:#334155;">Server Log</a>
            </div>

            <div class="card">
                <table>
                    <thead><tr><th>Ville</th><th>Statut</th><th>Réel</th><th>Ressenti</th></tr></thead>
                    <tbody>
                        {" ".join([f'<tr><td>{r["nom"]}</td><td style="color:{r["color"]}">{r["status"]}</td><td>{r["temp"]}°C</td><td>{r["ressenti"]}°C</td></tr>' for r in resultats])}
                    </tbody>
                </table>
            </div>

            <canvas id="luxChart" width="400" height="150"></canvas>
        </div>

        <script>
            const ctx = document.getElementById('luxChart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: {labels_graphe},
                    datasets: [
                        {{ label: 'Température Réelle (°C)', data: {temps_graphe}, backgroundColor: '#002395' }},
                        {{ label: 'Ressenti (°C)', data: {ressenti_graphe}, backgroundColor: '#ed2939' }}
                    ]
                }},
                options: {{ scales: {{ y: {{ beginAtZero: false, grid: {{ color: '#334155' }} }} }} }}
            }});
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)
