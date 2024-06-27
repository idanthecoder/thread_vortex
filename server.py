__author__ = "Idan"

import socket
import SQL_ORM
import threading
from tcp_by_size import send_with_size, recv_by_size
import hash_handler
import classes
from encryption_handler import EncryptionHandler


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

messages_votes_db = SQL_ORM.UserMessageVotesORM()
messages_votes_db.connect()
messages_votes_db.create_table()

conversations_pins_db = SQL_ORM.UserConversationPinsORM()
conversations_pins_db.connect()
conversations_pins_db.create_table()


class TCPServer:
    """
    A class that behaves as the server in my project.

    Attributes:
        host (str): The machine host.
        port (str): The port that is tuned to.
        server_socket (socket.socket): The socket instance of the server.
        clients (list): A list of all connected client sockets.
        clients_conversations (dict): A dictionary in which the key is a client socket and the value is a list of all the conversation that are already shown to that client.
        exit_all (bool): A boolean dictating when to close all connections.
    """
    
    def __init__(self, host, port):
        """
        The constructor for App class.

        Args:
            host (str): The machine host.
            port (str): The port that is tuned to.
        """
        
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.clients_conversations = {}
        self.exit_all = False

    def start(self):
        """
        This function makes the server start running and waiting for client connections.
        """
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
        """
        Handles all of the client's requests and sends a response.

        Args:
            client_socket (socket): The socket of a specific client in which data will be sent.
        """
        
        try:
            handle_encryption = EncryptionHandler(client_socket)
            while not self.exit_all:
                data = handle_encryption.decipher_data(recv_by_size(client_socket))
                if not data:
                    break
                print(f"Received: {data}")
                
                to_send = "NO_VALUE"
                data_split = data.split('|')
                command = data_split[0]
                fields = data_split[1:]
                
                if command == "REGUSR":
                    # register user
                    
                    salt = hash_handler.gen_salt()
                    pepper = hash_handler.get_global_pepper()
                    password = hash_handler.hash_password(pepper + salt + fields[1])
                    user = classes.User(fields[0], password, fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8]) # fields[7] should be datetime that I ran when the user sent the information (date_creation) and not an input of the user
                    register_status = users_db.insert_user(user, salt)
                    
                    if register_status == "no_issue":
                        to_send = f"REGUSR|new_user"
                    elif register_status == "mail_issue":
                        to_send = f"REGUSR|mail_taken"
                    elif register_status == "name_issue":
                        to_send = f"REGUSR|name_taken"
                elif command == "LOGUSR":
                    # log in / login user
                    
                    user_data = users_db.enter_account(fields[0], fields[1], fields[2])

                    if user_data:
                        to_send = f"LOGUSR|correct_identification|{user_data[0][1]}|{user_data[0][4]}|{user_data[0][5]}|{user_data[0][6]}|{user_data[0][7]}|{user_data[0][8]}|{user_data[0][9]}|{user_data[0][10]}"
                    else:
                        to_send = f"LOGUSR|failed_identification"
                elif command == "EDTUSR":
                    user = classes.User(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8])
                    users_db.edit_user_data(user)
                    to_send = "EDTUSR|edited_profile"
                
                elif command == "NEWCNV":
                    # create a new conversation including the first message within it
                    
                    # {conversation_title}|{message_content}|{restriction_status}|{creation_date}|{user_profile.username}
                    
                    conversation = classes.ConversationStruct(fields[0], fields[4], fields[3], fields[2])
                    conversation_status = conversations_db.insert_conversation(conversation)
                    # there can't be two titles with the same name!!
                    if conversation_status == "no_issue":
                        message = classes.MessageStruct(fields[1], fields[3], fields[4], fields[0])
                        messages_db.insert_message(message)
                        
                        to_send = "NEWCNV|new_conversation_added"
                    elif conversation_status == "title_issue":
                        to_send = "NEWCNV|title_issue"

                elif command == "MORCNV":
                    # get more conversations (new unseen conversations)
                    
                    # if current client already exists in the dictionary then he has already recieved messages
                    if client_socket in self.clients_conversations.keys():
                        # get the list of all titles the user has received so far
                        shown_titles = self.clients_conversations[client_socket]
                        # run command to get new conversations that aren't in the list
                        new_last_convs = conversations_db.get_last_new_conversations(shown_titles, int(fields[0]))
                        
                        
                        if len(new_last_convs) == 0:
                            to_send = "MORCNV|no_conversations"
                        # if there are new conversations then send them to the client
                        else:
                            to_send = "MORCNV|"
                        
                            for i, conv in enumerate(new_last_convs):
                                if i == len(new_last_convs)-1:
                                    to_send += f"{conv[1]}_{conv[2]}_{conv[3]}_{conv[4]}"
                                else:
                                    to_send += f"{conv[1]}_{conv[2]}_{conv[3]}_{conv[4]}|"
                            
                            shown_titles = shown_titles + self.apart_titles_from_lst(new_last_convs)
                            self.clients_conversations[client_socket] = shown_titles
                    else:
                        # in case client not in the dictionary. maybe make it so that this isn't possible? so when one loggs in he immediatly requests the first messages.
                        pass
                
                elif command == "FSTCNV":
                    # get the first conversations to show the user
                    last_conversations = conversations_db.get_last_conversations(int(fields[0]))
                    if last_conversations == []:
                        to_send = "FSTCNV|no_conversations"
                    else:
                        to_send = "FSTCNV|"
                        
                        for i, conv in enumerate(last_conversations):
                            if i == len(last_conversations)-1:
                                to_send += f"{conv[1]}_{conv[2]}_{conv[3]}_{conv[4]}"
                            else:
                                to_send += f"{conv[1]}_{conv[2]}_{conv[3]}_{conv[4]}|"
                        
                    self.clients_conversations[client_socket] = self.apart_titles_from_lst(last_conversations)
                
                elif command == "NEWMSG":
                    # send a new message inside a conversation
                    message = classes.MessageStruct(fields[0], fields[1], fields[2], fields[3])
                    messages_db.insert_message(message)
                
                    to_send = "NEWMSG|new_message_added"
                
                elif command == "FSTMSG":
                    # get the first messages inside a conversation to show the user
                    first_messages = messages_db.get_first_messages(fields[1], int(fields[0]))
                    if first_messages == []:
                        to_send = "FSTMSG|no_messages"
                    else:
                        to_send = "FSTMSG|"
                        
                        for i, msg in enumerate(first_messages):
                            if i == len(first_messages)-1:
                                to_send += f"{msg[0]}_{msg[1]}_{msg[2]}_{msg[3]}_{msg[4]}"
                            else:
                                to_send += f"{msg[0]}_{msg[1]}_{msg[2]}_{msg[3]}_{msg[4]}|"
                        
                    #self.clients_conversations[client_socket] = self.apart_titles_from_lst(first_messages)
                
                elif command == "MORMSG":
                    # get more messages inside a conversation to show the user
                    new_first_messages = messages_db.get_first_new_messages(fields[1], fields[2], int(fields[0]))
                    
                    print(f"message id is: {fields[2]}")

                    if new_first_messages == []:
                        to_send = "MORMSG|no_messages"
                    else:
                        to_send = "MORMSG|"
                        
                        for i, msg in enumerate(new_first_messages):
                            if i == len(new_first_messages)-1:
                                to_send += f"{msg[0]}_{msg[1]}_{msg[2]}_{msg[3]}_{msg[4]}"
                            else:
                                to_send += f"{msg[0]}_{msg[1]}_{msg[2]}_{msg[3]}_{msg[4]}|"
                
                elif command == "GETUSR":
                    # get a user's data
                    data_users = users_db.get_data_from_username(fields[0])
                    if len(data_users) == 0:
                        to_send = "GETUSR|no_user"
                    else:
                        user_data = data_users[0]
                        if user_data[1] != "[DELETED]":
                            to_send = f"GETUSR|{user_data[1]}|{user_data[4]}|{user_data[5]}|{user_data[6]}|{user_data[7]}|{user_data[8]}|{user_data[9]}|{user_data[10]}"
                        else:
                            to_send = "GETUSR|user_deleted"
                elif command == "SRCCNV":
                    # search for conversation and inside them for a text
                    search_in_convs = conversations_db.search_for(fields[0])
                    search_in_msgs = messages_db.search_for(fields[0])
                    
                    # get the conversation data in which this message is
                    convs_from_msgs = []
                    for msgdata in search_in_msgs:
                        convs_from_msgs.append(conversations_db.get_data_from_title(msgdata[4]))
                    
                    merged_lst = self.merge_lists(search_in_convs, convs_from_msgs)
                        
                    if merged_lst == []:
                        to_send = "SRCCNV|word_not_found"
                    else:
                        to_send = "SRCCNV|"
                        
                        for i, conv in enumerate(merged_lst):
                            if i == len(merged_lst)-1:
                                to_send += f"{conv[1]}_{conv[2]}_{conv[3]}_{conv[4]}"
                            else:
                                to_send += f"{conv[1]}_{conv[2]}_{conv[3]}_{conv[4]}|"
                
                elif command == "VOTMSG":
                    # user vote on a message
                    vote = fields[0]
                    username = fields[1]
                    message_id = fields[2]
                    
                    #messages_db.change_vote(int(message_id), int(vote))
                    
                    vote_status = messages_votes_db.already_voted(username, message_id)
                    
                    if vote_status == "new vote":
                        if vote == "upvote":
                            vt = 1
                        elif vote == "downvote":
                            vt = -1
                        message_vote = classes.UsersMessagesVotes(username, message_id, vt)
                        messages_votes_db.insert_message_vote(message_vote)
                        
                        vote_number = messages_votes_db.get_votes(message_id)
                        if vote == "upvote":
                            to_send = f"VOTMSG|upvote|{vote_number}" 
                        elif vote == "downvote":
                            to_send = f"VOTMSG|downvote|{vote_number}"                     
                    else:
                        if vote_status[3] == 1:
                            if vote == "upvote":
                                messages_votes_db.change_vote(username, message_id, 0)
                                vote_number = messages_votes_db.get_votes(message_id)
                                to_send = f"VOTMSG|no_vote|{vote_number}"
                            elif vote == "downvote":
                                messages_votes_db.change_vote(username, message_id, -1)
                                vote_number = messages_votes_db.get_votes(message_id)
                                to_send = f"VOTMSG|downvote|{vote_number}"
                        elif vote_status[3] == -1:
                            if vote == "upvote":
                                messages_votes_db.change_vote(username, message_id, 1)
                                vote_number = messages_votes_db.get_votes(message_id)
                                to_send = f"VOTMSG|upvote|{vote_number}"
                            elif vote == "downvote":
                                messages_votes_db.change_vote(username, message_id, 0)
                                vote_number = messages_votes_db.get_votes(message_id)
                                to_send = f"VOTMSG|no_vote|{vote_number}"
                        elif vote_status[3] == 0:
                            if vote == "upvote":
                                messages_votes_db.change_vote(username, message_id, 1)
                                vote_number = messages_votes_db.get_votes(message_id)
                                to_send = f"VOTMSG|upvote|{vote_number}"
                            elif vote == "downvote":
                                messages_votes_db.change_vote(username, message_id, -1)
                                vote_number = messages_votes_db.get_votes(message_id)
                                to_send = f"VOTMSG|downvote|{vote_number}"
                                
                elif command == "GEVMSG":
                    # get all users votes on a message
                    username = fields[0]
                    message_id = fields[1]
                    vote_status = messages_votes_db.already_voted(username, message_id)
                    vote_number = messages_votes_db.get_votes(message_id)
                    
                    if vote_status == "new vote":
                        to_send = f"GEVMSG|no_vote|{vote_number}"
                    else:
                        if vote_status[3] == 1:
                            to_send = f"GEVMSG|upvote|{vote_number}"
                        elif vote_status[3] == -1:
                            to_send = f"GEVMSG|downvote|{vote_number}"
                        else:
                            to_send = f"GEVMSG|no_vote|{vote_number}"
                    
                elif command == "PINCNV":
                    # user pin on a conversation
                    username = fields[0]
                    conversation_title = fields[1]
                    
                    pin_status = conversations_pins_db.already_pinned(username, conversation_title)
                    
                    if pin_status == "new pin":
                        conversation_pin = classes.UsersConversationsPins(username, conversation_title, 1)
                        conversations_pins_db.insert_conversation_pin(conversation_pin)
                        pin_number = conversations_pins_db.get_pins(conversation_title)
                        
                        to_send = f"PINCNV|pinned|{pin_number}"
                    else:
                        if pin_status[3] == 1:
                            conversations_pins_db.change_pin(username, conversation_title, 0)
                            pin_number = conversations_pins_db.get_pins(conversation_title)
                            to_send = f"PINCNV|no_pin|{pin_number}"
                        else:
                            conversations_pins_db.change_pin(username, conversation_title, 1)
                            pin_number = conversations_pins_db.get_pins(conversation_title)
                            to_send = f"PINCNV|pinned|{pin_number}"
                
                elif command == "GEPCNV":
                    # get all users pins on a conversation
                    username = fields[0]
                    conversation_title = fields[1]
                    pin_status = conversations_pins_db.already_pinned(username, conversation_title)
                    pin_number = conversations_pins_db.get_pins(conversation_title)
                    
                    if pin_status == "new pin":
                        to_send = f"GEPCNV|no_pin|{pin_number}"
                    else:
                        if pin_status[3] == 1:
                            to_send = f"GEPCNV|pinned|{pin_number}"
                        else:
                            to_send = f"GEPCNV|no_pin|{pin_number}"
                
                elif command == "GUPCNV":
                    # get all conversations that one specific user pinned
                    username = fields[0]
                    user_pinned_convs = conversations_pins_db.get_specific_user_pins(username)
                    
                    if user_pinned_convs == []:
                        to_send = "GUPCNV|no_pins"
                    else:
                        to_send = "GUPCNV|"
                        
                        for i, pinned_convs in enumerate(user_pinned_convs):
                            if i == len(user_pinned_convs)-1:
                                to_send += f"{pinned_convs[0]}"
                            else:
                                to_send += f"{pinned_convs[0]}|"
                
                elif command == "NPSUSR":
                    # user got a new password from forgot password
                    email = fields[0]
                    new_password = fields[1]
                    
                    users_db.update_password_by_mail(email, new_password)
                    to_send = "NPSUSR|password_updated"
                
                elif command == "DELMSG":
                    # delete a meesage
                    id = fields[0]
                    
                    messages_db.delete_message(id)
                    
                    to_send = "DELMSG|success"
                
                elif command == "EDTMSG":
                    # edit a message
                    id = fields[0]
                    content = fields[1]
                    messages_db.update_content(id, content)
                    
                    to_send = "EDTMSG|success"
                
                elif command == "DELUSR":
                    # delete a user and things related to him
                    username = fields[0]
                    users_db.delete_user(username)
                    messages_db.delete_user_messages(username)
                    conversations_db.change_to_deleted(username)
                    
                    to_send = "DELUSR|done"
                
                send_with_size(client_socket, handle_encryption.cipher_data(to_send))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Remove client from the list and from the dictionary saving the conversation he has received, then close the connection with him.
            self.clients.remove(client_socket)
            self.clients_conversations.pop(client_socket, "not_in_here")
            client_socket.close()

    def apart_titles_from_lst(self, conversation_lst):
        """
        Return a list of only titles without the other conversation data.

        Args:
            conversation_lst (list): A list of conversations data.

        Returns:
            list: A list of all the conversations titles.
        """
        titles_lst = []
        for conv in conversation_lst:
            titles_lst.append(conv[1])
        return titles_lst
    
    def merge_lists(self, list1, list2):
        """
        Merges 2 lists of tuples together without duplicates.

        Args:
            list1 (list): List of conversations data tuples
            list2 (list): List of conversations data tuples

        Returns:
            list: A merged list of list1 and list2 without duplicates.
        """
        
        unique_titles = set()
        merged_list = []

        list12 = list1 + list2
        for tup in list12:
            title = tup[1]  # Assuming title is at position [1]
            if title not in unique_titles:
                unique_titles.add(title)
                merged_list.append(tup)

        return merged_list

    def broadcast(self, message):
        """
        Sends data to all clients.

        Args:
            message (str): Message to send.
        """
        
        for client_socket in self.clients:
            try:
                send_with_size(client_socket, message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")

    def stop(self):
        """
        Stops the server process.
        """
        
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
