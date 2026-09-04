from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-dev-secret")

# Backend API URL from .env
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

@app.route("/")
def index():
    stats = {
        "attacks_today": 0,
        "active_campaigns": 0,
        "top_country": "System Init",
        "recent_activity": []
    }
    
    try:
        response = requests.get(f"{BACKEND_URL}/dashboard/stats", timeout=2)
        if response.status_code == 200:
            data = response.json()
            stats.update(data)
    except Exception as e:
        print(f"Backend Offline: {e}")

    return render_template("index.html", stats=stats)

if __name__ == "__main__":
    host = os.getenv("HOST_IP", "0.0.0.0")
    port = int(os.getenv("DASHBOARD_PORT", 5000))
    app.run(host=host, port=port, debug=True)
