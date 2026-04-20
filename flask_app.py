from flask import Flask, render_template_string
import requests
import time
from datetime import datetime

app = Flask(__name__)

# Configuration des 5 villes de luxe
VILLES = [
    {"nom": "Courbevoie", "lat": "48.8973", "lon": "2.2522"},
    {"nom": "Cannes", "lat": "43.5513", "lon": "7.0128"},
    {"nom": "Saint-Tropez", "lat": "43.2680", "lon": "6.6440"},
    {"nom": "Monaco", "lat": "43.7383", "lon": "7.4245"},
    {"nom": "Biarritz", "lat": "43.4831", "lon": "-1.5586"}
]

@app.route('/')
def dashboard():
    resultats = []
    total_latency = 0
    now = datetime.now().strftime("%Y-%m-%d à %H:%M:%S")

    # Boucle pour tester chaque ville
    for ville in VILLES:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={ville['lat']}&longitude={ville['lon']}&current_weather=true"
        start = time.time()
        try:
            response = requests.get(url, timeout=5)
            latency = round((time.time() - start) * 1000)
            status = "PASSER" if response.status_code == 200 else "ÉCHEC"
            color = "#4ade80" if response.status_code == 200 else "#f87171"
            temp = f"{response.json()['current_weather']['temperature']}°C"
        except:
            latency, status, color, temp = "-", "ERREUR", "#f87171", "N/A"
        
        resultats.append({**ville, "status": status, "latency": latency, "color": color, "temp": temp})
        if isinstance(latency, int): total_latency += latency

    avg_latency = round(total_latency / len(VILLES))

    # Design aux couleurs de la France 🇫🇷
    html_template = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Lux Monitoring - EPSI</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #0f172a; color: #f8fafc; padding: 40px; margin: 0; }}
            .container {{ max-width: 1100px; margin: auto; }}
            .fr-bar {{ height: 12px; width: 100%; display: flex; position: fixed; top: 0; left: 0; z-index: 1000; border-bottom: 1px solid white; }}
            .blue {{ background-color: #002395; flex: 1; }} .white {{ background-color: #ffffff; flex: 1; }} .red {{ background-color: #ed2939; flex: 1; }}
            .header {{ border-bottom: 4px solid #002395; padding-bottom: 20px; margin-bottom: 30px; margin-top: 30px; }}
            h1 {{ color: #ffffff; margin: 0; font-size: 2.2em; text-transform: uppercase; letter-spacing: 2px; }}
            .btn-group {{ margin-bottom: 25px; display: flex; gap: 10px; flex-wrap: wrap; }}
            .btn {{ background-color: #002395; color: white; padding: 10px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; border: 2px solid #ffffff; cursor: pointer; }}
            .card {{ background-color: #1e293b; padding: 25px; border-radius: 0 0 15px 15px; border: 1px solid #334155; border-top: 6px solid #ed2939; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: #0f172a; }}
            th {{ text-align: left; color: #ffffff; background-color: #002395; text-transform: uppercase; font-size: 0.8em; padding: 15px; }}
            td {{ padding: 15px; border-bottom: 1px solid #334155; }}
            .footer {{ margin-top: 40px; font-size: 0.85em; color: #94a3b8; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="fr-bar"><div class="blue"></div><div class="white"></div><div class="red"></div></div>
        <div class="container">
            <div class="header">
                <h1>🇫🇷 Monitoring Luxe & Prestige</h1>
                <div style="margin-top:10px;">EPSI | Professeur : <strong>Boris Stocker</strong> | Étudiant : <strong>Jean-Gérard</strong></div>
            </div>

            <div class="btn-group">
                <a href="/" class="btn">⚡ RÉACTUALISER LES 5 VILLES</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.access.log" target="_blank" class="btn" style="background:#334155; border:none;">Logs</a>
            </div>
            
            <div class="card">
                <div style="display:flex; justify-content:space-between; margin-bottom:20px; background:#0f172a; padding:15px; border-radius:8px;">
                    <div>Check global : <strong>{now}</strong></div>
                    <div style="color:#4ade80;">LATENCE MOYENNE : {avg_latency} ms</div>
                </div>
                <table>
                    <thead>
                        <tr><th>Ville</th><th>Statut</th><th>Température</th><th>Latence</th><th>Coordonnées</th></tr>
                    </thead>
                    <tbody>
                        {" ".join([f'<tr><td>{r["nom"]}</td><td style="color:{r["color"]}; font-weight:bold;">{r["status"]}</td><td>{r["temp"]}</td><td>{r["latency"]} ms</td><td style="font-size:0.8em; color:#94a3b8;">{r["lat"]}, {r["lon"]}</td></tr>' for r in resultats])}
                    </tbody>
                </table>
            </div>
            <div class="footer"><p>Projet Automatisé EPSI - Séquence 4</p></div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
