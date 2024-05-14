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

messages_db = SQL_ORM.MessagesORM()
messages_db.connect()
messages_db.create_table()

conversations_db = SQL_ORM.ConversationsORM()
conversations_db.connect()
conversations_db.create_table()



class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.clients_conversations = {}
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
                elif command == "NEWCNV":
                    # create a new conversation including the first message within it
                    
                    # {conversation_title}|{message_content}|{restriction_status}|{creation_date}|{user_profile.username}
                    
                    #posted_user_data = users_db.get_data_from_username(fields[4])
                    #posted_user_data[3] is salt
                    #posted_user = classes.User(posted_user_data[1], posted_user_data[2], posted_user_data[4], posted_user_data[5], posted_user_data[6], posted_user_data[7], posted_user_data[8], posted_user_data[9], posted_user_data[10])
                    conversation_status = conversations_db.conversation_checks(fields[0])
                    if not conversation_status:
                        conversation = classes.ConversationVServer(fields[0], fields[4], fields[3], fields[2])
                        conversations_db.insert_conversation(conversation)
                        # there can't be two titles with the same name!!
                        #conversation_id = conversations_db.get_id_from_title(fields[0])
                        
                        message = classes.MessageVServer(fields[1], fields[3], fields[4], fields[0])
                        messages_db.insert_message(message)
                        
                        to_send = "NEWCNV|new_conversation_added"
                    else:
                        if conversation_status[0] == "title_exists":
                            to_send = "NEWCNV|title_issue"
                    # not done yet. need to add a check for if a conversation with the same title already exists. and maybe let the user enter the conversation he has created?

                elif command == "MORCNV":
                    if client_socket in self.clients_conversations.keys():
                        shown_titles = self.clients_conversations[client_socket]
                        new_last_convs = conversations_db.get_last_new_conversations(shown_titles, int(fields[0]))
                        if len(new_last_convs) == 0:
                            to_send = "MORCNV|no_conversations"
                        else:
                            to_send = "MORCNV|"
                        
                            for i, conv in enumerate(new_last_convs):
                                if i == len(new_last_convs)-1:
                                    to_send += f"{conv[1]},{conv[2]},{conv[3]},{conv[4]}"
                                else:
                                    to_send += f"{conv[1]},{conv[2]},{conv[3]},{conv[4]}|"
                            
                            shown_titles = shown_titles + self.apart_titles_from_lst(new_last_convs)
                            self.clients_conversations[client_socket] = shown_titles
                    else:
                        # in case client not in the dictionary. maybe make it so that this isn't possible? so when one loggs in he immediatly requests the first messages.
                        pass
                
                elif command == "FSTCNV":
                    last_conversations = conversations_db.get_last_conversations(int(fields[0]))
                    if last_conversations == []:
                        to_send = "FSTCNV|no_conversations"
                    else:
                        to_send = "FSTCNV|"
                        
                        for i, conv in enumerate(last_conversations):
                            if i == len(last_conversations)-1:
                                to_send += f"{conv[1]},{conv[2]},{conv[3]},{conv[4]}"
                            else:
                                to_send += f"{conv[1]},{conv[2]},{conv[3]},{conv[4]}|"
                        
                    self.clients_conversations[client_socket] = self.apart_titles_from_lst(last_conversations)
                
                elif command == "NEWMSG":
                    message = classes.MessageVServer(fields[0], fields[1], fields[2], fields[3])
                    messages_db.insert_message(message)
                
                    to_send = "NEWMSG|new_message_added"
                
                elif command == "FSTMSG":
                    first_messages = messages_db.get_first_messages(fields[1], int(fields[0]))
                    if first_messages == []:
                        to_send = "FSTMSG|no_messages"
                    else:
                        to_send = "FSTMSG|"
                        
                        for i, msg in enumerate(first_messages):
                            if i == len(first_messages)-1:
                                to_send += f"{msg[1]},{msg[2]},{msg[3]},{msg[4]}"
                            else:
                                to_send += f"{msg[1]},{msg[2]},{msg[3]},{msg[4]}|"
                        
                    #self.clients_conversations[client_socket] = self.apart_titles_from_lst(first_messages)
                
                elif command == "MORMSG":
                    new_first_messages = messages_db.get_first_new_messages(fields[1], fields[2], int(fields[0]))

                    if new_first_messages == []:
                        to_send = "MORMSG|no_messages"
                    else:
                        to_send = "MORMSG|"
                        
                        for i, msg in enumerate(new_first_messages):
                            if i == len(new_first_messages)-1:
                                to_send += f"{msg[1]},{msg[2]},{msg[3]},{msg[4]}"
                            else:
                                to_send += f"{msg[1]},{msg[2]},{msg[3]},{msg[4]}|"
                
                elif command == "GETUSR":
                    data_users = users_db.get_data_from_username(fields[0])
                    if len(data_users) == []:
                        to_send = "GETUSR|no_user"
                    else:
                        user_data = data_users[0]
                        to_send = f"GETUSR|{user_data[1]}|{user_data[4]}|{user_data[5]}|{user_data[6]}|{user_data[7]}|{user_data[8]}|{user_data[9]}|{user_data[10]}"
                    
                        

                    
                    
                

                
                
                send_with_size(client_socket, to_send)
        #except Exception as e:
        #    print(f"Error: {e}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()

    def apart_titles_from_lst(self, conversation_lst):
        titles_lst = []
        for conv in conversation_lst:
            titles_lst.append(conv[1])
        return titles_lst

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
