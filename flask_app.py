from flask import Flask, render_template_string
import requests
import time
from datetime import datetime

app = Flask(__name__)

# Configuration des 5 villes de luxe
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
    total_latency = 0
    now = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")

    # Boucle de test dynamique pour chaque ville
    for ville in VILLES:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={ville['lat']}&longitude={ville['lon']}&current_weather=true"
        start = time.time()
        try:
            response = requests.get(url, timeout=5)
            latency = round((time.time() - start) * 1000)
            data = response.json()
            temp = f"{data['current_weather']['temperature']}°C"
            status = "OPÉRATIONNEL"
            color = "#4ade80" # Vert
        except Exception:
            latency = "-"
            temp = "N/A"
            status = "HORS-LIGNE"
            color = "#f87171" # Rouge
        
        resultats.append({**ville, "status": status, "latency": latency, "color": color, "temp": temp})
        if isinstance(latency, int):
            total_latency += latency

    avg_latency = round(total_latency / len(VILLES))

    # Design aux couleurs de la France 🇫🇷 avec liens de logs intégrés
    html_template = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Lux Monitoring 🇫🇷 - Jean-Gérard</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #0f172a; color: #f8fafc; padding: 40px; margin: 0; }}
            .container {{ max-width: 1100px; margin: auto; }}
            
            /* Drapeau Français en haut */
            .fr-bar {{ height: 12px; width: 100%; display: flex; position: fixed; top: 0; left: 0; z-index: 1000; border-bottom: 1px solid white; }}
            .blue {{ background-color: #002395; flex: 1; }}
            .white {{ background-color: #ffffff; flex: 1; }}
            .red {{ background-color: #ed2939; flex: 1; }}
            
            .header {{ border-bottom: 4px solid #002395; padding-bottom: 20px; margin-bottom: 30px; margin-top: 30px; }}
            h1 {{ color: #ffffff; margin: 0; font-size: 2.2em; text-transform: uppercase; letter-spacing: 2px; }}
            .highlight {{ color: #ffffff; font-weight: bold; text-decoration: underline #ed2939; }}
            
            .btn-group {{ margin-bottom: 25px; display: flex; gap: 10px; flex-wrap: wrap; }}
            .btn {{ background-color: #002395; color: white; padding: 10px 18px; border-radius: 4px; text-decoration: none; font-weight: bold; border: 2px solid white; transition: 0.3s; }}
            .btn:hover {{ background-color: #ed2939; }}
            .btn-logs {{ background-color: #334155; border: none; font-size: 0.85em; }}
            
            .card {{ background-color: #1e293b; padding: 25px; border-radius: 12px; border: 1px solid #334155; border-top: 8px solid #ed2939; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
            .status-summary {{ display: flex; justify-content: space-between; margin-bottom: 20px; background: #0f172a; padding: 15px; border-radius: 8px; border-left: 5px solid #002395; }}
            
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; background: #0f172a; border-radius: 8px; overflow: hidden; }}
            th {{ text-align: left; color: white; background-color: #002395; text-transform: uppercase; font-size: 0.8em; padding: 15px; }}
            td {{ padding: 15px; border-bottom: 1px solid #334155; }}
            
            .footer {{ margin-top: 40px; font-size: 0.85em; color: #94a3b8; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="fr-bar"><div class="blue"></div><div class="white"></div><div class="red"></div></div>
        
        <div class="container">
            <div class="header">
                <h1>🇫🇷 Monitoring Luxe & Prestige</h1>
                <div style="margin-top:10px; color: #94a3b8;">
                    École : <span class="highlight">EPSI</span> | Professeur : <span class="highlight">Boris Stocker</span> | Étudiant : <strong>Jean-Gérard</strong>
                </div>
            </div>

            <div class="btn-group">
                <a href="/" class="btn">⚡ ACTUALISER</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.access.log" target="_blank" class="btn btn-logs">📄 Access Log</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.error.log" target="_blank" class="btn btn-logs">⚠️ Error Log</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.server.log" target="_blank" class="btn btn-logs">🖥️ Server Log</a>
            </div>
            
            <div class="card">
                <div class="status-summary">
                    <div>Dernière analyse : <strong>{now}</strong></div>
                    <div style="color: #4ade80;">LATENCE MOYENNE : <strong>{avg_latency} ms</strong></div>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>Ville Destination</th>
                            <th>Statut API</th>
                            <th>Météo Actuelle</th>
                            <th>Temps de réponse</th>
                            <th>Coordonnées</th>
                        </tr>
                    </thead>
                    <tbody>
                        {" ".join([f'''
                        <tr>
                            <td style="font-weight:bold;">{r["nom"]}</td>
                            <td style="color:{r["color"]}; font-weight:bold;">{r["status"]}</td>
                            <td style="font-size: 1.1em;">{r["temp"]}</td>
                            <td>{r["latency"]} ms</td>
                            <td style="font-size:0.8em; color:#64748b;">{r["lat"]}, {r["lon"]}</td>
                        </tr>
                        ''' for r in resultats])}
                    </tbody>
                </table>
            </div>

            <div class="footer">
                <p>Projet Testing as Code - <span class="highlight">Séquence 4</span></p>
                <p>Déployé automatiquement via GitHub Actions pour l'EPSI</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
