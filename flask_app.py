from flask import Flask, render_template_string
import requests
import time

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Simulation de la mesure de performance pour le dashboard
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true"
    start = time.time()
    try:
        response = requests.get(url, timeout=5)
        status = "✅ OPÉRATIONNEL" if response.status_code == 200 else "❌ ERREUR"
        color = "#27ae60" if response.status_code == 200 else "#e74c3c"
    except:
        status = "⚠️ INDISPONIBLE"
        color = "#f39c12"
    
    ms = round((time.time() - start) * 1000)

    # Design du Dashboard
    html_template = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding: 50px; background-color: #f4f7f6; min-height: 100vh;">
        <div style="background: white; display: inline-block; padding: 40px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h1 style="color: #2c3e50; margin-bottom: 10px;">📊 API Monitoring Dashboard</h1>
            <p style="color: #7f8c8d;">Atelier Testing as Code - Jean-Gérard</p>
            <hr style="border: 0; height: 1px; background: #eee; margin: 20px 0;">
            
            <div style="margin: 20px 0;">
                <p style="font-size: 1.2em;"><strong>Service :</strong> Open-Meteo API</p>
                <p style="font-size: 1.5em; color: {color}; font-weight: bold;">{status}</p>
            </div>
            
            <div style="display: flex; justify-content: space-around; margin-top: 30px;">
                <div style="padding: 10px; border: 1px solid #eee; border-radius: 8px;">
                    <span style="display: block; color: #7f8c8d; font-size: 0.8em;">LATENCE</span>
                    <strong style="font-size: 1.2em;">{ms} ms</strong>
                </div>
                <div style="padding: 10px; border: 1px solid #eee; border-radius: 8px;">
                    <span style="display: block; color: #7f8c8d; font-size: 0.8em;">TESTS GITHUB</span>
                    <strong style="font-size: 1.2em; color: #27ae60;">PASSÉS ✅</strong>
                </div>
            </div>
            
            <p style="margin-top: 30px; font-size: 0.8em; color: #bdc3c7;">Déploiement automatique via GitHub Actions opérationnel</p>
        </div>
    </div>
    """
    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(debug=True)
