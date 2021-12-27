import socket
import threading

# The server's IP and port (known, either static or DDNS).
LOCAL_IP = "192.168.195.10"
LOCAL_PORT = 20002
BUFFER_SIZE = 1024

# The client's IP and port (unknown)
client_ip = None
client_port = None

# Server listens and sends on same port (required for UDP hole punching)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LOCAL_IP, LOCAL_PORT))

def listen():
    global sock, client_ip, client_port

    while True:
        data, (ip, port) = sock.recvfrom(1024)
        print(f"Received from client: {data.decode()}")

        # Client may roam, client IP is not static. Update IP, port on change.
        if ip != client_ip and port != client_port:
            client_ip = ip
            client_port = port
            print(f"New client IP, port established: {client_ip},"
                  f" {client_port}.")

# Start listener as a thread (so doesn't block)
listener = threading.Thread(target=listen, daemon=True)
listener.start()

while True:
    # Need to first determine client IP and wait for client to make UDP pinhole
    # before sending a message through (eg: initiate reverse-ssh or tcp conn.)
    if client_ip:
        msg = input("Send message to client: ")
        sock.sendto(msg.encode(), (client_ip, client_port))
