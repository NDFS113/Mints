import requests
import json
import time

class TelemetryClient:
    def __init__(self, backend_url="http://localhost:8000"):
        self.backend_url = backend_url

    def send_metrics(self, data):
        try:
            # res = requests.post(f"{self.backend_url}/telemetry", json=data)
            print(f"[*] Telemetry sent: {len(data)} items")
        except Exception as e:
            print(f"[!] Telemetry failed: {e}")

if __name__ == "__main__":
    client = TelemetryClient()
    while True:
        # scan logs and send
        time.sleep(60)
