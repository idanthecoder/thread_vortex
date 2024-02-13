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


def handle_client(sock, tid, db):
    """
    Process: Receives information from the client, calls the function to handle it, and then send the result
    :parameter: sock (socket), tid (tread number - int), db (UsernamePasswordORM class type)
    :return: nothing
    """

    global exit_all

    print("New Client num " + str(tid))

    while not exit_all:
        try:
            data = recv_by_size(sock).decode()
            if data == "":
                print("Error: Seens Client DC")
                break

            # figure out what to send
            to_send = do_action(data, db)

            send_with_size(sock, to_send)

        except socket.error as err:
            # deak with the possible exceptions
            if err.errno == 10054:
                # 'Connection reset by peer'
                print("Error %d Client is Gone. %s reset by peer." % (err.errno, str(sock)))
                break
            else:
                print("%d General Sock Error Client %s disconnected" % (err.errno, str(sock)))
                break
    sock.close()


def do_action(data, db):
    """
    Process: Examine the client's request, access / change the database, and return the result of the
    process to the client
    :parameter: data (list), db (UsernamePasswordORM class type)
    :return: to_send (string - in the format of the protocol, send this to the client)
    """

    # get the action and the fields (until index 6 it's the action and after that it's the field
    to_send = "Not Set Yet"
    action = data[:6]
    data = data[7:]
    fields = data.split('|')

    if DEBUG:
        print("Got client request " + action + " -- " + str(fields))

    # identify user
    if action == "LOGUSR":
        # get user's data if password and username are correct, otherwise inform of the identification error
        # access the account by passing the username and password, it will add the salt of the user and the password and check the hash to login
        user_data = db.enter_account(fields[0], fields[1], fields[2])

        if user_data:
            to_send = f"LOGUSR|correct_identification|{user_data[0][1]}|{user_data[0][2]}|{user_data[0][3]}|{user_data[0][4]}"
        else:
            to_send = f"LOGUSR|failed_identification"

    elif action == "REGUSR":
        # get user's data if password and username are correct, otherwise inform of the name error
        # access the account by passing the username password, it already has its assigned salt / already exists
        register_status = db.registeration_checks(fields[0], fields[2])

        #usernames = db.get_whole_col("username")

        # check if username is unique
        if not register_status:
            # generate a new salt and get the gloval pepper, to season the password
            salt = hash_handler.gen_salt()
            pepper = hash_handler.get_global_pepper()
            password = pepper + salt + fields[1]
            # use SHA256 on the salted and peppered password
            user = SQL_ORM.User(fields[0], hash_handler.hash_password(password), fields[2], 0)
            db.insert_user(user, salt)
            to_send = f"REGUSR|new_user|{user.username}|{user.password}|{user.mail}|{user.money}"
        else:
            # if name and/or email is already in use then tell this to the client
            if register_status[0] == "name_mail_issue":
                to_send = f"REGUSR|name_mail_taken"
            elif register_status[0] == "name_issue":
                to_send = f"REGUSR|name_taken"
            elif register_status[0] == "mail_issue":
                to_send = f"REGUSR|mail_taken"
                
    elif action == "DELUSR":
        # delete specified user if asked to
        db.delete_user_by_name(fields[0])
        to_send = f"DELUSR|success"
        
    elif action == "UPPUSR":
        # update password and salt if asked to
        db.update_password(fields[0], fields[1])
        to_send = f"UPPUSR|success"
        
    else:
        print("Got unknown action from client " + action)
        to_send = "ERR___R|001|" + "unknown action"

    return to_send


def main():
    """
    Process: Open the server and start accepting client connection in threads
    :parameter: nothing
    :return: nothing
    """

    global exit_all

    exit_all = False

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 12345))

    s.listen(4)
    print("after listen")
    threads = []
    i = 1
    while True:
        cli_s, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(cli_s, i, db))
        t.start()
        i += 1
        threads.append(t)


    exit_all = True
    for t in threads:
        t.join()
    manager.join()

    s.close()


if __name__ == "__main__":
    main()
