import os
import datetime
import sqlite3
from dotenv import load_dotenv

load_dotenv()

class BruteLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, "credentials.log")
        
        # Resolve DB Path same way as backend/db.py
        env_path = os.getenv("DB_PATH")
        if env_path:
             if os.path.isabs(env_path):
                self.db_path = env_path
             else:
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                self.db_path = os.path.join(project_root, env_path)
        else:
             # Fallback
             base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
             self.db_path = os.path.join(base_dir, "backend", "intel.db")

    def log_attempt(self, ip, username, password, service="telnet"):
        timestamp = datetime.datetime.utcnow().isoformat()
        
        # 1. Log to File
        entry = f"{timestamp} {service} {ip} {username} {password}\n"
        try:
            with open(self.log_file, "a") as f:
                f.write(entry)
        except Exception as e:
            print(f"[!] File Log Error: {e}")

        # 2. Log to Database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS attacks 
                            (id INTEGER PRIMARY KEY, ip TEXT, type TEXT, timestamp TEXT)''')
                            
            cursor.execute("INSERT INTO attacks (ip, type, timestamp) VALUES (?, ?, ?)", 
                           (ip, service, timestamp))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[!] DB Log Error: {e}")

        print(f"[*] Captive: {entry.strip()}")
