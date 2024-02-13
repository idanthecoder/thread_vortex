import sqlite3

import pickle
import hash_handler

import time

#  raise condition in SQLLite. if two people try to access at the same time it is a problem - solution may be to put sleep

# https://docs.python.org/2/library/sqlite3.html
# https://www.youtube.com/watch?v=U7nfe4adDw8


__author__ = "Idan"


class User:
    def __init__(self, name: str, password: str, mail: str, age: int, birthdate, gender: str,
                 description: str, country, workplace, date_creation):
        self.name = name
        self.password = password
        self.mail = mail
        self.age = age
        self.birthdate = birthdate
        self.gender = gender
        self.description = description
        self.country = country
        self.workplace = workplace
        self.date_creation = date_creation


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
                name TEXT UNIQUE,
                password TEXT,
                salt TEXT,
                mail TEXT UNIQUE,
                age INTEGER
                birthdate TEXT
                gender TEXT
                description TEXT
                country TEXT
                workplace TEXT
                date_creation TEXT
            )
        ''')

        self.commit()

    def insert_user(self, user: User, salt):
        self.cursor.execute('''
            INSERT INTO Users (name, password, salt, mail, age, birthdate, gender, description, country, workplace, date_creation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user.name, user.password, salt, user.mail, user.age, user.birthdate, user.gender, user.description,
              user.country, user.workplace, user.date_creation))
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
                            SET password = '{hashed_password}', salt = '{salt}'
                            WHERE username = '{username}' ''')

    # def deposit_withdraw_money(self, user_id, amount):
    #    current_money = self.get_specific(user_id, "money")
    #
    #    self.cursor.execute(f'''
    #                UPDATE Users
    #                SET money = '{current_money + amount}'
    #                WHERE user_id = {user_id}
    #            ''')
    #    self.commit()

    def registeration_checks(self, username, mail):
        """
        Process: conduct all checks for registeration - mail and username must be unique
        :parameter: username (string), mail (string)
        :return: a list ([] means success, other results explain the issue)
        """

        # search for the existence of the name and mail
        name_in_data = (self.cursor.execute(f'''SELECT * FROM Users
                                   WHERE username = '{username}' ''').fetchall())
        mail_in_data = (self.cursor.execute(f'''SELECT * FROM Users
                                   WHERE mail = '{mail}' ''').fetchall())

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
                                   WHERE username = '{username}' ''').fetchall())

        # if no salt was found it means that there is no such user, as it has no data which is necessarily saved, return []
        if not salt:
            return []

        # get the global pepper, the salt from database and hash them together with the password
        pepper = hash_handler.get_global_pepper()
        hashed_password = hash_handler.hash_password(pepper + salt[0][0] + password)
        # get all of the user's data and return it
        data = self.cursor.execute(f'''SELECT * FROM Users 
                                   WHERE username = '{username}' AND password = '{hashed_password}' AND mail = '{mail}' ''').fetchall()
        return data


class Message:
    def __init__(self, content: str, sender: User, date_send: str, conversation_id):
        self.content = content
        self.seder = sender
        self.date_send = date_send
        self.conversation_id = conversation_id


class Conversation:
    def __init__(self, initialize_date, title, restrictions, message_lst=None):
        if message_lst is None:
            message_lst = []
        else:
            self.message_lst = message_lst
        self.initialize_date = initialize_date
        self.title = title
        self.restrictions = restrictions
