import socket
import threading
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from sensor.capture.brute_logger import BruteLogger
from sensor.capture.payload_sniffer import PayloadSniffer

class TelnetEmulator:
    def __init__(self, port=2323, bind_ip="0.0.0.0"):
        self.port = port
        self.bind_ip = bind_ip
        self.brute_logger = BruteLogger(log_dir="logs")
        self.payload_sniffer = PayloadSniffer(log_dir="logs")

    def handle_client(self, conn, addr):
        try:
            conn.send(b"login: ")
            user = conn.recv(1024).strip().decode(errors='ignore')
            conn.send(b"password: ")
            pwd = conn.recv(1024).strip().decode(errors='ignore')

            self.brute_logger.log_attempt(addr[0], user, pwd, service="telnet")

            conn.send(b"Welcome to IoT Device\n# ")
            
            while True:
                data = conn.recv(2048)
                if not data:
                    break
                
                # Check for exit
                if b"exit" in data:
                    break

                # Log generic payload if relevant
                if b"http" in data or b"wget" in data or b"curl" in data:
                     self.payload_sniffer.log_payload(addr[0], data, service="telnet")
                
                conn.send(b"# ")
        except Exception as e:
            pass # Connection dropped
        finally:
            conn.close()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((self.bind_ip, self.port))
            s.listen(5)
            print(f"[*] Telnet Emulator listening on {self.bind_ip}:{self.port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
        except OSError as e:
            print(f"[!] Error binding to port {self.port}: {e}")

if __name__ == "__main__":
    emu = TelnetEmulator()
    emu.start()
