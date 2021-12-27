import socket
import time
import threading

# Acquire a port for sending/receiving (to determine mechanism)
LOCAL_IP = "192.168.195.1"
LOCAL_PORT = 20001
BUFFER_SIZE = 1024

# The server IP and port (known, either static or DDNS).
DEST_IP = "192.168.195.10"
DEST_PORT = 20002

INTERVAL = 700

# Client sends and listens on the same port (required for UDP hole punching)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LOCAL_IP, LOCAL_PORT))

def listen():
    global sock

    while True:
        data = sock.recv(1024)
        print(f"Received from server: {data.decode()}")

# Start listener as a thread (so doesn't block)
listener = threading.Thread(target=listen, daemon=True)
listener.start()

# Send update packet (for revealing IP, and for UDP pinhole) every 30 s.
while True:
    sock.sendto(b'device-id;device-ip;', (DEST_IP, DEST_PORT))
    time.sleep(INTERVAL);

