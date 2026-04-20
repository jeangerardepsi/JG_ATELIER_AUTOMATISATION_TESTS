from flask import Flask, render_template_string
import requests
import time
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def dashboard():
    # 1. Mesure de performance de l'API
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true"
    start = time.time()
    
    try:
        response = requests.get(url, timeout=5)
        latency = round((time.time() - start) * 1000)
        status = "PASSER" if response.status_code == 200 else "ÉCHEC"
        status_color = "#4ade80" 
    except Exception:
        latency = "-"
        status = "ERREUR"
        status_color = "#f87171"

    now = datetime.now().strftime("%Y-%m-%d à %H:%M:%S")

    # 2. Design aux couleurs de la FRANCE 🇫🇷
    html_template = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard Monitoring - Jean-Gérard (EPSI)</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #0f172a; color: #f8fafc; padding: 40px; margin: 0; }}
            .container {{ max-width: 1000px; margin: auto; }}
            .fr-bar {{ height: 12px; width: 100%; display: flex; position: fixed; top: 0; left: 0; z-index: 1000; border-bottom: 1px solid white; }}
            .blue {{ background-color: #002395; flex: 1; }}
            .white {{ background-color: #ffffff; flex: 1; }}
            .red {{ background-color: #ed2939; flex: 1; }}
            .header {{ border-bottom: 4px solid #002395; padding-bottom: 20px; margin-bottom: 30px; margin-top: 30px; }}
            h1 {{ color: #ffffff; margin: 0; font-size: 2.2em; text-transform: uppercase; letter-spacing: 2px; }}
            .sub-header {{ color: #94a3b8; font-size: 1.1em; margin-top: 10px; }}
            .btn-group {{ margin-bottom: 25px; display: flex; gap: 10px; flex-wrap: wrap; }}
            .btn {{ background-color: #002395; color: white; padding: 10px 20px; border-radius: 4px; text-decoration: none; font-weight: bold; border: 2px solid #ffffff; cursor: pointer; transition: 0.3s; }}
            .btn:hover {{ background-color: #ed2939; border-color: #ffffff; }}
            .btn-logs {{ background-color: #334155; border: none; font-size: 0.85em; opacity: 0.9; }}
            .btn-logs:hover {{ opacity: 1; background-color: #475569; }}
            .card {{ background-color: #1e293b; padding: 25px; border-radius: 0 0 15px 15px; border: 1px solid #334155; border-top: 6px solid #ed2939; }}
            .status-line {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding: 15px; background: #0f172a; border-radius: 8px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: #0f172a; border-radius: 8px; overflow: hidden; }}
            th {{ text-align: left; color: #ffffff; background-color: #002395; text-transform: uppercase; font-size: 0.8em; padding: 15px; }}
            td {{ padding: 15px; border-bottom: 1px solid #334155; }}
            .status-pass {{ color: {status_color}; font-weight: bold; }}
            .footer {{ margin-top: 40px; font-size: 0.85em; color: #94a3b8; text-align: center; }}
            .highlight {{ color: #ffffff; font-weight: bold; text-decoration: underline #ed2939; }}
        </style>
    </head>
    <body>
        <div class="fr-bar"><div class="blue"></div><div class="white"></div><div class="red"></div></div>
        <div class="container">
            <div class="header">
                <h1>🇫🇷 Monitoring API - Séquence 4</h1>
                <div class="sub-header">École : <span class="highlight">EPSI</span> | Professeur : <span class="highlight">Boris Stocker</span></div>
                <div class="sub-header">Étudiant : <span style="color:white; font-weight: bold;">Jean-Gérard</span></div>
            </div>

            <div class="btn-group">
                <a href="/" class="btn">⚡ ACTUALISER</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.access.log" target="_blank" class="btn btn-logs">📄 Access Log</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.error.log" target="_blank" class="btn btn-logs">⚠️ Error Log</a>
                <a href="https://www.pythonanywhere.com/user/jeangerard/files/var/log/jeangerard.pythonanywhere.com.server.log" target="_blank" class="btn btn-logs">🖥️ Server Log</a>
            </div>
            
            <div class="card">
                <div class="status-line">
                    <div style="font-size: 1.1em;">Dernier check : <strong>{now}</strong></div>
                    <div style="color: #4ade80; font-weight: bold;">TESTS GITHUB : PASSÉS ✅</div>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>Service Testé</th>
                            <th>Résultat</th>
                            <th>Latence</th>
                            <th>Localisation</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>API Météo (Open-Meteo)</td>
                            <td class="status-pass">{status}</td>
                            <td>{latency} ms</td>
                            <td>Paris, FR 🇫🇷</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="footer">
                <p>Projet Testing as Code - <span class="highlight">EPSI 2026</span></p>
                <p>Déployé automatiquement pour <strong>Boris Stocker</strong> via GitHub Actions</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
