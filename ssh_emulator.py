import socket
import threading
import paramiko
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from sensor.capture.brute_logger import BruteLogger

# Silence paramiko logging
paramiko.util.log_to_file("logs/paramiko.log")

HOST_KEY_PATH = "host.key"

class HoneypotServer(paramiko.ServerInterface):
    def __init__(self, client_ip, brute_logger):
        self.event = threading.Event()
        self.client_ip = client_ip
        self.brute_logger = brute_logger

    def check_auth_password(self, username, password):
        # Log the attempt
        self.brute_logger.log_attempt(self.client_ip, username, password, service="ssh")
        # Always fail authentication to keep them out
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

class SSHEmulator:
    def __init__(self, port=2222, bind_ip="0.0.0.0"):
        self.port = port
        self.bind_ip = bind_ip
        self.brute_logger = BruteLogger(log_dir="logs")

        # Generate host key if missing
        if not os.path.exists(HOST_KEY_PATH):
            print("[*] Generating SSH Host Key...")
            key = paramiko.RSAKey.generate(2048)
            key.write_private_key_file(HOST_KEY_PATH)
        self.host_key = paramiko.RSAKey(filename=HOST_KEY_PATH)

    def handle_connection(self, client, addr):
        transport = paramiko.Transport(client)
        transport.add_server_key(self.host_key)
        server = HoneypotServer(addr[0], self.brute_logger)
        try:
            transport.start_server(server=server)
            # Accept logic to trigger auth
            channel = transport.accept(20) 
            if channel is None:
                return
            channel.close()
        except Exception:
            pass
        finally:
            transport.close()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((self.bind_ip, self.port))
            s.listen(100)
            print(f"[*] SSH Emulator listening on {self.bind_ip}:{self.port}")
            while True:
                client, addr = s.accept()
                threading.Thread(target=self.handle_connection, args=(client, addr)).start()
        except Exception as e:
            print(f"[!] SSH Bind failed: {e}")

if __name__ == "__main__":
    SSHEmulator().start()
