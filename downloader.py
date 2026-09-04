import os
import hashlib
import json
import requests
import re

class Downloader:
    def __init__(self, sandbox_dir="sensor/sandbox/malware_samples"):
        self.sandbox_dir = sandbox_dir
        os.makedirs(self.sandbox_dir, exist_ok=True)
    
    def download_from_url(self, url):
        filename = url.split("/")[-1]
        if not filename:
            filename = "unknown_artifact"
        
        path = os.path.join(self.sandbox_dir, filename)
        try:
            # downloading with verification disabled for safety in lab, but strictly no execution
            r = requests.get(url, timeout=10, verify=False) 
            with open(path, "wb") as f:
                f.write(r.content)
            return path
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return None

    def fingerprint(self, path):
        if not path or not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            data = f.read()
            return hashlib.sha256(data).hexdigest()

    def analyze_sandbox(self):
        report = []
        for f in os.listdir(self.sandbox_dir):
            path = os.path.join(self.sandbox_dir, f)
            if os.path.isfile(path):
                h = self.fingerprint(path)
                report.append({"file": f, "sha256": h})
        
        with open("fingerprints.json", "w") as out:
            json.dump(report, out, indent=2)
        return report
