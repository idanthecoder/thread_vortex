import sqlite3
import hash_handler
import classes


__author__ = "Idan"


class UsernamePasswordORM(object):
    def __init__(self, db_name="UsernamePassword.db"):
        self.db_name = db_name
        self.conn = None  # will store the DB connection
        self.cursor = None  # will store the DB connection cursor

    def connect(self):
        """
        Process: Opens DB file and put value in self.conn (need DB file name) and self.cursor
        :parameter: nothing
        :return: nothing
        """

        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                salt TEXT,
                mail TEXT UNIQUE,
                age INTEGER,
                gender TEXT,
                country TEXT,
                occupation TEXT,
                date_creation TEXT,
                description TEXT
            )
        ''')

        self.commit()

    def insert_user(self, user: classes.User, salt):
        self.cursor.execute('''
            INSERT INTO Users (username, password, salt, mail, age, gender, country, occupation, date_creation, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user.username, user.password, salt, user.mail, user.age, user.gender, user.country, user.occupation, user.date_creation, user.description))
        self.commit()

    def print_table(self, table_name):
        table_list = [a for a in self.cursor.execute(f"SELECT * FROM {table_name}")]
        print(table_list)

    def get_table(self, table_name):
        table_list = [a for a in self.cursor.execute(f"SELECT * FROM {table_name}")]
        return table_list

    def update_user(self, user_id, subject, data):
        self.cursor.execute(f'''
                    UPDATE Users
                    SET {subject} = '{data}'
                    WHERE user_id = {user_id}
                ''')
        self.commit()

    def delete_user(self, user_id):
        self.cursor.execute(f'''
                    DELETE FROM Users
                    WHERE user_id = {user_id}
                ''')
        self.commit()

    def get_whole_col(self, subject):
        return self.cursor.execute(f'''SELECT {subject} FROM Users''').fetchall()

    def get_specific(self, user_id, subject):
        return self.cursor.execute(f'''SELECT {subject} FROM Users WHERE user_id = {user_id}''').fetchall()
    
    def delete_user_by_name(self, username):
        self.cursor.execute(f'''DELETE FROM Users WHERE username = '{username}' ''')
        self.commit()
    
    
    def update_password(self, username, password):
        """
        Process: update a user's password, and give it a new salt
        :parameter: username (string), password (string)
        :return: Nothing
        """
        
        # get the global pepper, generate new salt and hash them with the password
        salt = hash_handler.gen_salt()
        pepper = hash_handler.get_global_pepper()
        hashed_password = hash_handler.hash_password(pepper + salt + password)
        
        # change the password and the hash
        self.cursor.execute(f'''UPDATE Users
                            SET password = ?, salt = ?
                            WHERE username = ? ''', (hashed_password, salt, username))
        self.commit()
    
    def update_password_by_mail(self, mail, password):
        """
        Process: update a user's password, and give it a new salt
        :parameter: mail (string), password (string)
        :return: Nothing
        """
        
        # get the global pepper, generate new salt and hash them with the password
        salt = hash_handler.gen_salt()
        pepper = hash_handler.get_global_pepper()
        hashed_password = hash_handler.hash_password(pepper + salt + password)
        
        # change the password and the hash
        self.cursor.execute(f'''UPDATE Users
                            SET password = ?, salt = ?
                            WHERE mail = ? ''', (hashed_password, salt, mail))
        self.commit()

    
    def registeration_checks(self, username, mail):
        """
        Process: conduct all checks for registeration - mail and username must be unique
        :parameter: username (string), mail (string)
        :return: a list ([] means success, other results explain the issue)
        """
        
        # search for the existence of the name and mail
        name_in_data = (self.cursor.execute(f'''SELECT * FROM Users
                                   WHERE username = ? ''', (username,)).fetchall())
        mail_in_data = (self.cursor.execute(f'''SELECT * FROM Users
                                   WHERE mail = ? ''', (mail,)).fetchall())
        
        # return if both mail and name are unavailable or just one of them
        if name_in_data and mail_in_data:
            return ["name_mail_issue"]
        elif name_in_data:
            return ["name_issue"]
        elif mail_in_data:
            return ["mail_issue"]
        
        # a valid regiseration
        return []
    
    
    def enter_account(self, username, password, mail):
        """
        Process: enter the account if it can be found, and retrieve its data, otherwise return []
        :parameter: username (string), password (string), mail (string)
        :return: data (list of tuples or [])
        """
        
        salt = (self.cursor.execute(f'''SELECT salt FROM Users
                                   WHERE username = ? ''', (username,)).fetchall())
        
        # if no salt was found it means that there is no such user, as it has no data which is necessarily saved, return []
        if not salt:
            return []
        
        # get the global pepper, the salt from database and hash them together with the password
        pepper = hash_handler.get_global_pepper()
        hashed_password = hash_handler.hash_password(pepper + salt[0][0] + password)
        # get all of the user's data and return it
        data = self.cursor.execute(f'''SELECT * FROM Users 
                                   WHERE username = ? AND password = ? AND mail = ? ''', (username, hashed_password, mail)).fetchall()
        return data
    
    
    def edit_user_data(self, user: classes.User):
        if user.password != "":
            self.update_password(user.username, user.password)
        self.cursor.execute(f'''UPDATE Users
                            SET age = ?, gender = ?, country = ?, occupation = ?, date_creation = ?, description = ?
                            WHERE username = ? ''', (user.age, user.gender, user.country, user.occupation, user.date_creation, user.description, user.username))
        self.commit()
    
    def get_data_from_username(self, username):
        data = self.cursor.execute(f'''SELECT * FROM Users 
                                   WHERE username = ? ''', (username,)).fetchall()
        
        if len(data) == 0:
            return []
        return data

#---------------------------------

class MessagesORM(object):
    def __init__(self, db_name="Messages.db"):
        self.db_name = db_name
        self.conn = None  # will store the DB connection
        self.cursor = None  # will store the DB connection cursor

    def connect(self):
        """
        Process: Opens DB file and put value in self.conn (need DB file name) and self.cursor
        :parameter: nothing
        :return: nothing
        """

        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Messages (
                message_id INTEGER PRIMARY KEY,
                content TEXT,
                date_published TEXT,
                sender_username TEXT,
                conversation_title TEXT
            )
        ''')

        self.commit()

    def insert_message(self, message: classes.MessageStruct):
        self.cursor.execute('''
            INSERT INTO Messages (content, date_published, sender_username, conversation_title)
            VALUES (?, ?, ?, ?)
        ''', (message.content, message.date_published, message.sender_username, message.conversation_title))
        self.commit()

    def print_table(self, table_name):
        table_list = [a for a in self.cursor.execute(f"SELECT * FROM {table_name}")]
        print(table_list)

    def get_table(self, table_name):
        table_list = [a for a in self.cursor.execute(f"SELECT * FROM {table_name}")]
        return table_list

    def update_message(self, message_id, subject, data):
        self.cursor.execute(f'''
                    UPDATE Messages
                    SET {subject} = '{data}'
                    WHERE message_id = {message_id}
                ''')
        self.commit()

    def delete_message(self, message_id):
        self.cursor.execute(f'''
                    DELETE FROM Messages
                    WHERE message_id = {message_id}
                ''')
        self.commit()

    def get_whole_col(self, subject):
        return self.cursor.execute(f'''SELECT {subject} FROM Messages''').fetchall()

    def get_specific(self, message_id, subject):
        return self.cursor.execute(f'''SELECT {subject} FROM Messages WHERE message_id = {message_id}''').fetchall()
    
    def get_first_messages(self, conversation_title, amount=1):
        all_messages = self.cursor.execute(f'''SELECT * FROM Messages 
                                           WHERE conversation_title = ? ''', (conversation_title,)).fetchall()
        
        if len(all_messages) == 0:
            return []
        
        if len(all_messages) < amount:
            return all_messages[0:len(all_messages)]
        else:
            return all_messages[0:amount]
        
    def get_first_new_messages(self, conversation_title, last_recieved_msg_id, amount=1):
        # get all messages of the conversation
        all_messages = self.cursor.execute(f'''SELECT * FROM Messages 
                                           WHERE conversation_title = ? ''', (conversation_title,)).fetchall()
        
        new_messages = []
        for msgdata in all_messages:
            if int(msgdata[0]) > int(last_recieved_msg_id):
                new_messages.append(msgdata)
                if len(new_messages) == amount:
                    return new_messages
        
        # no new messages, or new messages but less then requested amount
        return new_messages
        
                
                
        
        ## check from last to first in case of 2 messages with the same content
        #all_messages_reversed = list(reversed(all_messages))
        #new_index = 0
        #for i, msgdata in enumerate(all_messages_reversed):
        #    if msgdata[1] == last_recieved_msg_content:
        #        # will give me the index of one after the one i'm looking at right now, but from the start not from the end
        #        new_index = len(all_messages) - i
        #        break
        #
        ## if there aren't any new messages
        #if new_index > len(all_messages):
        #    return [] 
        #
        ## if there are new messages, but not the requested amount
        #if len(all_messages) < new_index+amount:
        #    return all_messages[new_index: len(all_messages)]
        ## if there are new messages and can return the requested amount
        #else:
        #    return all_messages[new_index: new_index+amount]
    
    def search_for(self, search_for):
        search_in_data = (self.cursor.execute(f'''SELECT * FROM Messages
                                   WHERE content Like ?''', (f"%{search_for}%",)).fetchall())
        if len(search_in_data) == 0:
            return []
        return search_in_data

    #def change_vote(self, message_id, vote):
    #    # vote is either 1 or -1
    #    self.cursor.execute(f'''
    #                UPDATE Messages
    #                SET votes = votes + ?
    #                WHERE message_id = ?''', (vote, message_id))
    #    self.commit()
    
    #def alter_table(self):
    #    self.cursor.execute("ALTER TABLE Messages ADD COLUMN votes INTEGER DEFAULT 0")
    #    self.commit()

    #def dealter_table(self):
    #    self.cursor.execute("ALTER TABLE Messages DROP COLUMN votes")
    #    self.commit()
        
#---------------------------------

class ConversationsORM(object):
    def __init__(self, db_name="Conversations.db"):
        self.db_name = db_name
        self.conn = None  # will store the DB connection
        self.cursor = None  # will store the DB connection cursor

    def connect(self):
        """
        Process: Opens DB file and put value in self.conn (need DB file name) and self.cursor
        :parameter: nothing
        :return: nothing
        """

        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Conversations (
                conversation_id INTEGER PRIMARY KEY,
                title TEXT UNIQUE,
                creator_username TEXT,
                creation_date TEXT,
                restrictions TEXT
            )
        ''')

        self.commit()

    def insert_conversation(self, conversation: classes.ConversationStruct):
        self.cursor.execute('''
            INSERT INTO Conversations (title, creator_username, creation_date, restrictions)
            VALUES (?, ?, ?, ?)
        ''', (conversation.title, conversation.creator_username, conversation.creation_date, conversation.restrictions))
        self.commit()

    def print_table(self, table_name):
        table_list = [a for a in self.cursor.execute(f"SELECT * FROM {table_name}")]
        print(table_list)

    def get_table(self, table_name):
        table_list = [a for a in self.cursor.execute(f"SELECT * FROM {table_name}")]
        return table_list

    def update_conversation(self, conversation_id, subject, data):
        self.cursor.execute(f'''
                    UPDATE Conversations
                    SET {subject} = '{data}'
                    WHERE conversation_id = {conversation_id}
                ''')
        self.commit()

    def delete_conversation(self, conversation_id):
        self.cursor.execute(f'''
                    DELETE FROM Conversations
                    WHERE conversation_id = {conversation_id}
                ''')
        self.commit()

    def get_whole_col(self, subject):
        return self.cursor.execute(f'''SELECT {subject} FROM Conversations''').fetchall()

    def get_specific(self, conversation_id, subject):
        return self.cursor.execute(f'''SELECT {subject} FROM Conversations WHERE conversation_id = {conversation_id}''').fetchall()

    def get_last_conversations(self, amount=1):
        all_convs = self.get_table("Conversations")
        if len(all_convs) == 0:
            return []
        if len(all_convs) < amount:
            return all_convs[-len(all_convs):]
        else:
            return all_convs[-amount:] 
        
    def get_last_new_conversations(self, shown_titles, amount=1):
        all_convs = self.get_table("Conversations")
        if len(all_convs) == 0:
            return []
        
        return_lst = []
        all_convs_reverse = list(reversed(all_convs))
        
        for conv in all_convs_reverse:
            if not conv[1] in shown_titles:
                return_lst.append(conv)
                # if all found, break the loop and return the values
                if len(return_lst) == amount:
                    return return_lst
        
        # check
        if len(return_lst) == 0:
            # no new conversations
            return []
        # in this case there are new conversations, just not the requested amount
        return return_lst

    def conversation_checks(self, title):
        # search for the existence of the name and mail
        title_in_data = (self.cursor.execute(f'''SELECT * FROM Conversations
                                   WHERE title = ? ''', (title,)).fetchall())
        
        # return if both mail and name are unavailable or just one of them
        if title_in_data :
            return ["title_exists"]
        
        # a valid regiseration
        return []

    def search_for(self, search_for):
        search_in_data = (self.cursor.execute(f'''SELECT * FROM Conversations
                                   WHERE title Like ?''', (f"%{search_for}%",)).fetchall())
        if len(search_in_data) == 0:
            return []
        return search_in_data

    def get_data_from_title(self, title):
        data = self.cursor.execute(f'''SELECT * FROM Conversations 
                                   WHERE title = ? ''', (title,)).fetchall()
        
        if len(data) == 0:
            return []
        return data[0]


class UserMessageVotesORM(object):
    def __init__(self, db_name="UsersMessagesVotes.db"):
        self.db_name = db_name
        self.conn = None  # will store the DB connection
        self.cursor = None  # will store the DB connection cursor

    def connect(self):
        """
        Process: Opens DB file and put value in self.conn (need DB file name) and self.cursor
        :parameter: nothing
        :return: nothing
        """

        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UsersMessagesVotes (
                user_message_vote_id INTEGER PRIMARY KEY,
                username TEXT,
                message_id INTEGER,
                vote INTEGER
            )
        ''')

        self.commit()

    def insert_message_vote(self, votes: classes.UsersMessagesVotes):
        self.cursor.execute('''
            INSERT INTO UsersMessagesVotes (username, message_id, vote)
            VALUES (?, ?, ?)
        ''', (votes.username, votes.message_id, votes.vote))
        self.commit()

    def print_table(self, table_name):
        table_list = [a for a in self.cursor.execute(f"SELECT * FROM {table_name}")]
        print(table_list)

    def get_table(self, table_name):
        table_list = [a for a in self.cursor.execute(f"SELECT * FROM {table_name}")]
        return table_list
    
    def change_vote(self, username, message_id, vote):
        # vote is either 1 or -1 or 0
        
        self.cursor.execute(f'''
                    UPDATE UsersMessagesVotes
                    SET vote = ?
                    WHERE message_id = ? AND username = ?''', (vote, message_id, username))
        self.commit()
    
    def already_voted(self, username, message_id):
        # search for the existence of the name and mail
        vote_status = self.cursor.execute(f'''SELECT * FROM UsersMessagesVotes
                                   WHERE message_id = ? AND username = ? ''', (message_id, username)).fetchall()
        
        # return if both mail and name are unavailable or just one of them
        if vote_status :
            return vote_status[0]
        
        # a valid regiseration
        return "new vote"
    
    def get_votes(self, message_id):
        vote_amount = self.cursor.execute(f'''SELECT SUM(vote) FROM UsersMessagesVotes
                                   WHERE message_id = ? ''', (message_id,)).fetchall()
        
        if vote_amount[0][0] is None:
            return 0
        return vote_amount[0][0]


class UserConversationPinsORM(object):
    def __init__(self, db_name="UserConversationPins.db"):
        self.db_name = db_name
        self.conn = None  # will store the DB connection
        self.cursor = None  # will store the DB connection cursor

    def connect(self):
        """
        Process: Opens DB file and put value in self.conn (need DB file name) and self.cursor
        :parameter: nothing
        :return: nothing
        """

        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UsersConversationsPins (
                user_conversation_pin_id INTEGER PRIMARY KEY,
                username TEXT,
                conversation_title TEXT,
                pin INTEGER
            )
        ''')

        self.commit()

    def insert_conversation_pin(self, pins: classes.UsersConversationsPins):
        self.cursor.execute('''
            INSERT INTO UsersConversationsPins (username, conversation_title, pin)
            VALUES (?, ?, ?)
        ''', (pins.username, pins.conversation_title, pins.pin))
        self.commit()

    def print_table(self, table_name):
        table_list = [a for a in self.cursor.execute(f"SELECT * FROM {table_name}")]
        print(table_list)

    def get_table(self, table_name):
        table_list = [a for a in self.cursor.execute(f"SELECT * FROM {table_name}")]
        return table_list
    
    def change_pin(self, username, conversation_title, pin):
        # pin is either 1 or 0
        
        self.cursor.execute(f'''
                    UPDATE UsersConversationsPins
                    SET pin = ?
                    WHERE conversation_title = ? AND username = ?''', (pin, conversation_title, username))
        self.commit()
    
    def already_pinned(self, username, conversation_title):
        # search for the existence of the name and mail
        vote_status = self.cursor.execute(f'''SELECT * FROM UsersConversationsPins
                                   WHERE conversation_title = ? AND username = ? ''', (conversation_title, username)).fetchall()
        
        # return if both mail and name are unavailable or just one of them
        if vote_status :
            return vote_status[0]
        
        # a valid regiseration
        return "new pin"
    
    def get_pins(self, conversation_title):
        pin_amount = self.cursor.execute(f'''SELECT SUM(pin) FROM UsersConversationsPins
                                   WHERE conversation_title = ? ''', (conversation_title,)).fetchall()
        
        if pin_amount[0][0] is None:
            return 0
        return pin_amount[0][0]

    def get_specific_user_pins(self, username):
        user_pins = self.cursor.execute(f'''SELECT conversation_title FROM UsersConversationsPins
                                   WHERE username = ? AND pin != 0 ''', (username,)).fetchall()
        
        # list of tuples (each tuple has one value only in it)
        return user_pins


#if __name__ == "__main__":
#    ##orm = UserMessageVotesORM()
#    ##orm.connect()
#    ##gorm = orm.get_votes(73)
#    ##print(gorm[0][0])
#    ##print()
#    #msgorm = MessagesORM()
#    #msgorm.connect()
#    #msgorm.dealter_table()
#    
#    ormp = UserConversationPinsORM()
#    ormp.connect()
#    ge = ormp.get_specific_user_pins("Igor")
#    print(ge)
#    print()

