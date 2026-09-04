import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

# Determine DB path:
# 1. Try env var 'DB_PATH'
# 2. If env var is relative, resolve it relative to PROJECT ROOT (which is one level up from backend/)
# 3. Fallback to local default

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "intel.db")

env_path = os.getenv("DB_PATH")
if env_path:
    if os.path.isabs(env_path):
        DB_PATH = env_path
    else:
        # Assuming run from project root or having CWD issues, let's anchor it to the file location to be safe
        # If DB_PATH is "backend/intel.db" and we are in "backend/db.py", we need to go up one level
        # Actually easier: If env var is provided, assume it's relative to CWD (Project Root).
        # But this file is imported by API and by Sensors.
        # Safest bet: Anchor relative to project root.
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DB_PATH = os.path.join(project_root, env_path)
else:
    DB_PATH = DEFAULT_DB_PATH

def get_db_connection():
    # Helper to ensure dir exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Create tables if not exist
    conn.execute('''CREATE TABLE IF NOT EXISTS attacks 
                    (id INTEGER PRIMARY KEY, ip TEXT, type TEXT, timestamp TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS malware 
                    (id INTEGER PRIMARY KEY, hash TEXT, family TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()
