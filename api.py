from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import sqlite3
from dotenv import load_dotenv

# Load env
load_dotenv()

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from backend.db import get_db_connection, init_db

app = FastAPI(title="SENTINEL-IoT Threat Intel API")

# Enable CORS for public access (or at least from Dashboard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on start
init_db()

@app.get("/")
def read_root():
    return {"status": "active", "system": "SENTINEL-IoT"}

@app.get("/feed/ips")
def get_bad_ips():
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT ip, count(*) as count FROM attacks GROUP BY ip ORDER BY count DESC LIMIT 100").fetchall()
        return [{"ip": r["ip"], "count": r["count"]} for r in rows]
    finally:
        conn.close()

@app.get("/dashboard/stats")
def get_dashboard_stats():
    conn = get_db_connection()
    try:
        # Total attacks
        total = conn.execute("SELECT count(*) as c FROM attacks").fetchone()["c"]
        
        # Attacks today
        import datetime
        today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        today_count = conn.execute("SELECT count(*) as c FROM attacks WHERE timestamp LIKE ?", (f"{today_str}%",)).fetchone()["c"]
        
        # Active campaigns (Unique attack types)
        campaigns = conn.execute("SELECT count(DISTINCT type) as c FROM attacks").fetchone()["c"]
        
        # Top Source (IP with most attacks)
        top_ip_row = conn.execute("SELECT ip, count(*) as c FROM attacks GROUP BY ip ORDER BY c DESC LIMIT 1").fetchone()
        top_source = f"{top_ip_row['ip']}" if top_ip_row else "None"
        
        # Recent logs
        recent_rows = conn.execute("SELECT ip, type, timestamp FROM attacks ORDER BY id DESC LIMIT 5").fetchall()
        recent_activity = [
            {"source": r["ip"], "port": "23/22", "signature": f"Auth.Brute.{r['type']}", "status": "Logged", "timestamp": r["timestamp"]}
            for r in recent_rows
        ]

        return {
            "attacks_today": today_count,
            "total_attacks": total,
            "active_campaigns": campaigns,
            "top_country": top_source, # Placeholder for Country
            "recent_activity": recent_activity
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST_IP", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host=host, port=port)
