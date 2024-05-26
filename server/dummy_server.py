import socket
import struct
from PyQt5.QtCore import *

class Server(QObject):
    newData = pyqtSignal(list)

    def __init__(self, server_ip, server_port):
        super().__init__()
        self.ip = server_ip
        self.port = server_port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)

        self.running = False

    def start_server(self):
        self.running = True
        print(f"Server started at {self.ip} on port {self.port}")

        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                # print(f"Connection from {client_address}")
                self.handle_client(client_socket)
            except socket.error as e:
                if self.running:
                    print(f"Error accepting connection: {e}")
                else:
                    print("Server is stopped")
                continue
   

    def handle_client(self, client_socket):
        try:
            while True:
                received_data = client_socket.recv(128)
                if not received_data:
                    break

                data = struct.unpack('<iffiiiiii', received_data[2:38])
                self.newData.emit(list(data))
        finally:
            client_socket.close()

    def stop_server(self):
        self.running = False
        self.server_socket.close()

 
