__author__ = "Idan"

import socket
import SQL_ORM
import threading
from tcp_by_size import send_with_size, recv_by_size
import hash_handler
import classes


DEBUG = True
exit_all = False

# declare database and connect to it
users_db = SQL_ORM.UsernamePasswordORM()
users_db.connect()
users_db.create_table()


class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.exit_all = False

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Server started on {self.host}:{self.port}")
            while not self.exit_all:
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
            while not self.exit_all:
                data = recv_by_size(client_socket).decode()
                if not data:
                    break
                print(f"Received: {data}")
                
                to_send = "NO_VALUE"
                data_split = data.split('|')
                command = data_split[0]
                fields = data_split[1:]
                
                if command == "REGUSR":
                    register_status = users_db.registeration_checks(fields[0], fields[2])
                    
                    if not register_status:
                        salt = hash_handler.gen_salt()
                        pepper = hash_handler.get_global_pepper()
                        password = hash_handler.hash_password(pepper + salt + fields[1])
                        user = classes.User(fields[0], password, fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8]) # fields[7] should be datetime that I ran when the user sent the information (date_creation) and not an input of the user
                        users_db.insert_user(user, salt)
                        to_send = f"REGUSR|new_user|{user.username}|{user.password}|{user.mail}|{user.age}|{user.gender}|{user.country}|{user.occupation}|{user.date_creation}|{user.description}"
                    else:
                        if register_status[0] == "name_mail_issue":
                            to_send = f"REGUSR|name_mail_taken"
                        elif register_status[0] == "name_issue":
                            to_send = f"REGUSR|name_taken"
                        elif register_status[0] == "mail_issue":
                            to_send = f"REGUSR|mail_taken"
                elif command == "LOGUSR":
                    users_db.print_table("Users")
                    user_data = users_db.enter_account(fields[0], fields[1], fields[2])

                    if user_data:
                        to_send = f"LOGUSR|correct_identification|{user_data[0][1]}|{user_data[0][4]}|{user_data[0][5]}|{user_data[0][6]}|{user_data[0][7]}|{user_data[0][8]}|{user_data[0][9]}|{user_data[0][10]}"
                    else:
                        to_send = f"LOGUSR|failed_identification"
                elif command == "EDTUSR":
                    #salt = hash_handler.gen_salt()
                    #pepper = hash_handler.get_global_pepper()
                    #password = hash_handler.hash_password(pepper + salt + fields[1])
                    user = classes.User(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8])
                    users_db.edit_user_data(user)
                    to_send = "EDTUSR|edited_profile"
                    users_db.print_table("Users")
                elif command == "NEWCON":
                    # create a new conversation including the first message within it
                    pass
                    
                
                
                
                
                
                
                
                send_with_size(client_socket, to_send)
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
    server = TCPServer('localhost', 12345)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
