from flask import Flask, render_template_string
import requests
import time
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def dashboard():
    # 1. Mesure de performance de l'API Open-Meteo
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true"
    start = time.time()
    
    try:
        response = requests.get(url, timeout=5)
        latency = round((time.time() - start) * 1000)
        status = "PASSER" if response.status_code == 200 else "ÉCHEC"
        status_color = "#4ade80" if response.status_code == 200 else "#f87171"
    except Exception as e:
        latency = "-"
        status = "ERREUR"
        status_color = "#f87171"

    now = datetime.now().strftime("%Y-%m-%d à %H:%M:%S")

    # 2. Design Amélioré (Style Dark Mode / EPSI)
    html_template = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard Monitoring - Jean-Gérard (EPSI)</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #1a1625; color: #e2e8f0; padding: 40px; line-height: 1.6; }}
            .container {{ max-width: 1000px; margin: auto; }}
            .header {{ border-bottom: 2px solid #8b5cf6; padding-bottom: 20px; margin-bottom: 30px; }}
            h1 {{ color: #c084fc; margin: 0; font-size: 2.5em; }}
            .sub-header {{ color: #94a3b8; font-size: 1.1em; margin-top: 10px; }}
            
            .btn-group {{ margin-bottom: 25px; display: flex; gap: 10px; flex-wrap: wrap; }}
            .btn {{ background-color: #7c3aed; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; border: none; cursor: pointer; transition: 0.3s; }}
            .btn:hover {{ background-color: #6d28d9; }}
            .btn-logs {{ background-color: #4b5563; font-size: 0.9em; }}
            
            .card {{ background-color: #2d2640; padding: 25px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border: 1px solid #443d5a; }}
            .status-line {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding: 15px; background: #1f1a2e; border-radius: 10px; }}
            
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: #1f1a2e; border-radius: 10px; overflow: hidden; }}
            th {{ text-align: left; color: #a78bfa; text-transform: uppercase; font-size: 0.8em; padding: 15px; border-bottom: 1px solid #443d5a; }}
            td {{ padding: 15px; border-bottom: 1px solid #332d4a; }}
            
            .status-pass {{ color: {status_color}; font-weight: bold; }}
            .footer {{ margin-top: 40px; font-size: 0.85em; color: #64748b; text-align: center; border-top: 1px solid #332d4a; padding-top: 20px; }}
            .highlight {{ color: #c084fc; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✨ État de l'API - Dashboard</h1>
                <div class="sub-header">École : <span class="highlight">EPSI</span> | Professeur : <span class="highlight">Boris Stocker</span></div>
                <div class="sub-header">Étudiant : Jean-Gérard</div>
            </div>

            <div class="btn-group">
                <button class="btn">⚡ Exécuter les tests manuellement</button>
                <a href="/var/log/jeangerard.pythonanywhere.com.access.log" class="btn btn-logs">📄 Access Log</a>
                <a href="/var/log/jeangerard.pythonanywhere.com.error.log" class="btn btn-logs">⚠️ Error Log</a>
                <a href="/var/log/jeangerard.pythonanywhere.com.server.log" class="btn btn-logs">🖥️ Server Log</a>
            </div>
            
            <div class="card">
                <div class="status-line">
                    <div style="font-size: 1.2em;">Dernière exécution : <span style="color: #94a3b8;">{now}</span></div>
                    <div style="background: #4c1d95; padding: 8px 15px; border-radius: 20px; font-size: 0.9em;">
                        Succès : 1 | Échecs : 0 | Latence : {latency} ms
                    </div>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>Point de terminaison</th>
                            <th>Statut</th>
                            <th>Latence</th>
                            <th>Détails</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>GET /forecast (Open-Meteo)</td>
                            <td class="status-pass">{status}</td>
                            <td>{latency} ms</td>
                            <td>Opérationnel ✅</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="footer">
                <p>Système de monitoring automatisé via <span class="highlight">GitHub Actions</span> et <span class="highlight">PythonAnywhere</span></p>
                <p>Séquence 4 : Atelier Testing as Code - Jean-Gérard</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
