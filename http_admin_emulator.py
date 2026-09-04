import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from sensor.capture.brute_logger import BruteLogger

RESPONSE_HTML = """HTTP/1.1 200 OK
Content-Type: text/html
Connection: close

<html>
<head><title>Router Admin Panel</title></head>
<body>
<div style="width: 300px; margin: 100px auto; font-family: sans-serif;">
<h2>Router Administration</h2>
<form method="POST">
<label>Username</label><br>
<input name="user" style="width: 100%%"><br><br>
<label>Password</label><br>
<input type="password" name="password" style="width: 100%%"><br><br>
<input type="submit" value="Login">
</form>
</div>
</body>
</html>
"""

class HTTPAdminEmulator:
    def __init__(self, port=8080, bind_ip="0.0.0.0"):
        self.port = port
        self.bind_ip = bind_ip
        self.brute_logger = BruteLogger(log_dir="logs")

    def handle_client(self, conn, addr):
        try:
            data = conn.recv(4096).decode(errors='ignore')
            if "POST" in data:
                # Extract crude credentials from POST body
                # Very basic parsing for demo
                try:
                    lines = data.split("\r\n\r\n")
                    if len(lines) > 1:
                        body = lines[1]
                        self.brute_logger.log_attempt(addr[0], "http_post", body, service="http_admin")
                except:
                    pass
            
            conn.send(RESPONSE_HTML.encode())
        except Exception:
            pass
        finally:
            conn.close()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((self.bind_ip, self.port))
            s.listen(5)
            print(f"[*] HTTP Admin Emulator listening on {self.bind_ip}:{self.port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
        except Exception as e:
            print(f"[!] HTTP Bind failed (try running as admin/root if port < 1024): {e}")

if __name__ == "__main__":
    HTTPAdminEmulator().start()
