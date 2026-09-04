import os
import datetime

class PayloadSniffer:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, "payloads.log")

    def log_payload(self, ip, data, service="telnet"):
        timestamp = datetime.datetime.utcnow().isoformat()
        # Sanitize bytes for logging
        try:
            decoded = data.decode('utf-8', errors='ignore')
        except:
            decoded = str(data)
        
        entry = f"{timestamp} {service} {ip} CMD: {decoded.strip()}\n"
        with open(self.log_file, "a") as f:
            f.write(entry)
        print(f"[!] Payload: {entry.strip()}")
