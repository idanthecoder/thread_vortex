__author__ = "Idan"

import socket
import SQL_ORM
import threading
from tcp_by_size import send_with_size, recv_by_size
import hash_handler


DEBUG = True
exit_all = False

# declare database and connect to it
db = SQL_ORM.UsernamePasswordORM()
db.connect()
db.create_table()


class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Server started on {self.host}:{self.port}")
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
                self.clients.append(client_socket)
        except Exception as e:
            print(f"Error: {e}")
            self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            while True:
                data = recv_by_size(client_socket).decode()
                if not data:
                    break
                print(f"Received: {data.decode()}")
                send_with_size(client_socket, data)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    def broadcast(self, message):
        for client_socket in self.clients:
            try:
                send_with_size(client_socket, message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")

    def stop(self):
        for client_socket in self.clients:
            client_socket.close()
        self.server_socket.close()
        print("Server stopped")


if __name__ == "__main__":
    server = TCPServer('localhost', 9999)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
