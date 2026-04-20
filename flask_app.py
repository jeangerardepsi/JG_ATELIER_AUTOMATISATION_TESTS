from flask import Flask, render_template_string
import requests
import time
from datetime import datetime

app = Flask(__name__)

# Configuration des destinations de luxe
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
        url = f"https://api.open-meteo.com/v1/forecast?latitude={ville['lat']}&longitude={ville['lon']}&current_weather=true&hourly=apparent_temperature"
        try:
            response = requests.get(url, timeout=5).json()
            temp = response['current_weather']['temperature']
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
        <title>Lux Monitoring 🇫🇷 - Jean-Gérard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            /* NOUVELLE COULEUR DE FOND : BLEU NUIT PROFOND */
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #020617; color: #f8fafc; padding: 20px; margin: 0; }}
            
            .container {{ max-width: 1000px; margin: auto; }}
            .fr-bar {{ height: 12px; width: 100%; display: flex; position: fixed; top: 0; left: 0; z-index: 1000; border-bottom: 1px solid rgba(255,255,255,0.1); }}
            .blue {{ background-color: #002395; flex: 1; }} .white {{ background-color: #ffffff; flex: 1; }} .red {{ background-color: #ed2939; flex: 1; }}
            
            h1 {{ margin-top: 50px; text-transform: uppercase; letter-spacing: 3px; border-left: 5px solid #ed2939; padding-left: 15px; }}
            .info-bar {{ margin-bottom: 20px; color: #94a3b8; font-size: 0.9em; }}
            
            .btn-group {{ margin: 25px 0; display: flex; gap: 12px; flex-wrap: wrap; }}
            .btn {{ background-color: #002395; color: white; padding: 12px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; border: 1px solid white; transition: 0.3s; }}
            .btn:hover {{ background-color: #ed2939; transform: translateY(-2px); }}
            .btn-logs {{ background-color: #1e293b; border: 1px solid #334155; font-size: 0.85em; }}
            
            .card {{ background-color: #0f172a; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4); margin-bottom: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
            th {{ text-align: left; color: #64748b; font-size: 0.8em; text-transform: uppercase; padding: 12px; border-bottom: 2px solid #1e293b; }}
            td {{ padding: 15px; border-bottom: 1px solid #1e293b; }}
            
            .chart-container {{ background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; }}
            .footer {{ margin-top: 50px; text-align: center; color: #475569; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <div class="fr-bar"><div class="blue"></div><div class="white"></div><div class="red"></div></div>
        
        <div class="container">
            <h1>🇫🇷 LUXE & PRESTIGE MONITORING</h1>
            <div class="info-bar">EPSI | Professeur : <b>Boris Stocker</b> | Étudiant : <b>Jean-Gérard</b></div>
            
            <div class="btn-group">
                <a href="/" class="btn">⚡ ACTUALISER</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.access.log" target="_blank" class="btn btn-logs">📄 Access Log</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.error.log" target="_blank" class="btn btn-logs">⚠️ Error Log</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.server.log" target="_blank" class="btn btn-logs">🖥️ Server Log</a>
            </div>

            <div class="card">
                <table>
                    <thead><tr><th>Destination</th><th>Statut API</th><th>Temp. Réelle</th><th>Ressenti</th></tr></thead>
                    <tbody>
                        {" ".join([f'<tr><td style="font-weight:bold;">{r["nom"]}</td><td style="color:{r["color"]}">{r["status"]}</td><td style="font-size:1.1em;">{r["temp"]}°C</td><td style="color:#cbd5e1;">{r["ressenti"]}°C</td></tr>' for r in resultats])}
                    </tbody>
                </table>
            </div>

            <div class="chart-container">
                <canvas id="luxChart" height="120"></canvas>
            </div>
            
            <div class="footer">Dernière mise à jour : {datetime.now().strftime("%H:%M:%S")} | Projet Séquence 4 - EPSI 2026</div>
        </div>

        <script>
            const ctx = document.getElementById('luxChart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: {labels_graphe},
                    datasets: [
                        {{ label: 'Température Réelle', data: {temps_graphe}, backgroundColor: '#002395', borderRadius: 5 }},
                        {{ label: 'Ressenti Thermique', data: {ressenti_graphe}, backgroundColor: '#ed2939', borderRadius: 5 }}
                    ]
                }},
                options: {{ 
                    plugins: {{ legend: {{ labels: {{ color: '#94a3b8' }} }} }},
                    scales: {{ 
                        y: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
                        x: {{ ticks: {{ color: '#94a3b8' }} }}
                    }} 
                }}
            }});
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)
