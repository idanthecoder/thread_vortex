__author__ = "Idan"

import socket

import threading
from tcp_by_size import send_with_size, recv_by_size
from tkinter import messagebox, Listbox, END, SINGLE, simpledialog
from tkinter import *
import email_handler
import time


WAIT_TIME_MINS = 5


def close_sub_win(win, do_deiconify=False):
    """
    Process: Close a window
    :parameter: win (tkinter root)
    :return: Nothing
    """

    win.quit()
    win.destroy()
    if do_deiconify:
        root.deiconify()
        

def on_closing():
    """
    Process: Terminate every ongoing activity
    :parameter: Nothing
    :return: Nothing
    """
    # close the window
    root.destroy()

    # close the socket
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()
    exit(0)


def user_area(username, password, mail, money):
    """
    Process: Allows the user is able to interact with the system
    :parameter: username (string), password (string), password_check (string), mode (string), win (tkinter root)
    :return: Nothing
    """
    
    root.withdraw()
    area_root = Toplevel()
    area_root.title("Your Account")
    area_root.protocol("WM_DELETE_WINDOW", lambda: close_sub_win(area_root, True))

    area_root.geometry(f"{width}x{height}")

    Label(area_root, text="Success!", bd=9, relief=GROOVE, font=("times new roman", 40, "bold"),
          bg="white", fg="green").pack()

    go_back_button = Button(area_root, text="return to main lobby", command=lambda: return_to_lobby(area_root))
    go_back_button.pack()

    print(f"name:{username}, password:{password}, mail:{mail}, money:{money}")
    
    area_root.mainloop()


def enter_user_area(username, password, mail, mode, win, forgot_root=None):
    """
    Process: Send the client's details to the server, to determine if the details are correct and the client can enter
    the system, or if there is an error with his input
    :parameter: username (string), password (string), password_check (string), mode (string), win (tkinter root)
    :return: Nothing
    """    
    
    send_with_size(client_socket, f"{mode}|{username}|{password}|{mail}")
    data = recv_by_size(client_socket).decode().split('|')
    if len(data) <= 1:
        return

    if data[0] == "LOGUSR":
        # check if the client can login
        if data[1] == "failed_identification":
            messagebox.showinfo("Identification Error", "failed to Identify")
            if forgot_root is not None:
                close_sub_win(forgot_root)
                win.deiconify()
        elif data[1] == "correct_identification":
            win.quit()
            win.destroy()
            user_area(data[2], data[3], data[4], data[5])
    elif data[0] == "REGUSR":
        # check if the name and mail inputted are free to take
        if data[1] == "name_mail_taken":
            messagebox.showinfo("Name And Mail Error", "chosen name and mail are unavailable")
        elif data[1] == "name_taken":
            messagebox.showinfo("Name Error", "chosen name is unavailable")
        elif data[1] == "mail_taken":
            messagebox.showinfo("Mail Error", "mail is unavailable")
        elif data[1] == "new_user":
            win.withdraw()
            # if the mail gets verified enter user area, otherwise go back to the register screen
            mail_verified = mail_conformation(mail)
            if mail_verified:
                win.quit()
                win.destroy()
                user_area(data[2], data[3], data[4], data[5])
            else:
                send_with_size(client_socket, f"DELUSR|{username}")
                data = recv_by_size(client_socket).decode().split('|')
                print(data[1])
                messagebox.showinfo("Mail Error", "closed conversation window")
                win.deiconify()


def return_to_lobby(win):
    """
    Process: Close any windows it gets, and deiconify the main root
    :parameter: win (tkinter root)
    :return: Nothing
    """

    win.quit()
    win.destroy()
    root.deiconify()


def get_user_conf(user_conf_entry, conf_code, conf_root, mail):
    """
    Process: If the timer is not expired and the entry code is correct then move on
    :parameter: user_conf_entry (tkinter Entry), conf_code (string: the real code), conf_root (the tkinter conformation root), mail (string)
    :return: Nothing
    """

    global conf_done, end_time
    
    if is_timer_expired(end_time):
        messagebox.showinfo("Timeout Error", "Delay of more than 5 minutes\nResending a code to the mail")
        resend_mail(mail)
        return
    
    if conf_code == user_conf_entry.get():
        conf_done = True
        close_sub_win(conf_root)
    else:
        messagebox.showinfo("Code Error", "wrong verification code")


def set_timer(minutes):
    """
    Process: calculates the total time (the current system time + the minutes of the countdown)
    :parameter: minutes (int)
    :return: The total countdown time
    """

    seconds = minutes * 60
    return time.time() + seconds


def is_timer_expired(end_time):
    """
    Process: checks if the timer has expired
    :parameter: end_time (int)
    :return: True / False depends on the result
    """
    
    return time.time() >= end_time


def resend_mail(mail):
    """
    Process: resend the conformation mail and reset the timer
    :parameter: mail (string)
    :return: Nothing
    """
    
    global conformation_code, end_time
    conformation_code = email_handler.send_conformation_mail(mail)
    end_time = set_timer(WAIT_TIME_MINS)
    

def mail_conformation(mail):
    """
    Process: send conformation code to the client's mail and wait until they submit the right code. They can ask for new code and there is a 5 min timer for each one
    :parameter: mail (string)
    :return: True if the conformation window is closed properly (not interrupted mid conversation)
    """
    
    global conf_done, conformation_code, end_time
    
    # open a window to let the user enter the conformation code, let the user ask for a new one and timeout this for 5 minutes for each code
    conf_done = False
    resend_mail(mail)
    conf_root = Toplevel()
    conf_root.title("Mail conformation")
    conf_root.protocol("WM_DELETE_WINDOW", lambda: close_sub_win(conf_root))
    
    Label(conf_root, text="Enter Conformation Code", font=('Helvetica', 20)).pack(pady=20)
    Label(conf_root, text=f"You have {WAIT_TIME_MINS} minutes to enter the code", font=('Helvetica', 15)).pack(pady=20)
    
    user_conf_code = Entry(conf_root, width=20)
    user_conf_code.pack()
    
    
    conf_button = Button(conf_root, text="confirm", command=lambda: get_user_conf(user_conf_code, conformation_code, conf_root, mail))
    conf_button.pack()
    
    send_again_button = Button(conf_root, text="send different code", command=lambda: resend_mail(mail))
    send_again_button.pack()
    
    conf_root.mainloop()
    # if this collapses then it means email is correct
    if conf_done:
        return True
    return False
    


def register_password_check(username, password, password_check, mail, mode, win):
    """
    Process: Checks if the password check is correct, and if so call enter_user_area
    :parameter: username (string), password (string), password_check (string), mode (string), win (tkinter root)
    :return: Nothing
    """

    if password != password_check:
        messagebox.showinfo("Password check fail", "second password given is incorrect")
        return
    
    enter_user_area(username, password, mail, mode, win)


def check_injection(username, password, mail, mode, win, forgot_root=None):
    """
    Process: Checks if the username contains string which resembles SQL code, if not then call enter_user_area
    :parameter: username (string), password (string), password_check (string), mode (string), win (tkinter root)
    :return: nothing
    """

    if username.__contains__("'") or username.__contains__("--"):
        messagebox.showinfo("Injection blocked", "SQL injection attempt blocked")
        if forgot_root is not None:
            forgot_root.deiconify()
        return
    
    if forgot_root is not None:
        close_sub_win(forgot_root)
    enter_user_area(username, password, mail, mode, win, forgot_root)


def register_func():
    """
    Process: Handles the registration GUI and allows the client to enter information
    :parameter: Nothing
    :return: Nothing
    """

    # withdraw the main root and set up a toplevel root for the login window
    root.withdraw()

    register_root = Toplevel()
    register_root.title("Register Page")
    register_root.protocol("WM_DELETE_WINDOW", lambda: close_sub_win(register_root, True))

    register_root.geometry(f"{width}x{height}")

    # use entry widget to get input from the user (username, password and the password check)
    Label(register_root, text="Register", bd=9, relief=GROOVE, font=("times new roman", 40, "bold"),
          bg="white", fg="green").pack()

    Label(register_root, text="Enter Username", font=('Helvetica', 20)).pack(pady=20)

    username = Entry(register_root, width=20)
    username.pack()

    Label(register_root, text="Enter Password", font=('Helvetica', 20)).pack(pady=20)

    password = Entry(register_root, show="*", width=20)
    password.pack()

    Label(register_root, text="Password check", font=('Helvetica', 20)).pack(pady=20)

    password_check = Entry(register_root, show="*", width=20)
    password_check.pack()

    Label(register_root, text="Enter Mail", font=('Helvetica', 20)).pack(pady=20)

    mail = Entry(register_root, width=20)
    mail.pack()
    

    # clicking this button will call the function that will check if the second password isn't equal to the first,
    # thus the client's interaction with this page isn't over
    submission_button = Button(register_root, text="submit", command=lambda: register_password_check(
        username.get(), password.get(), password_check.get(), mail.get(), "REGUSR", register_root))
    submission_button.pack()

    # clicking this button will terminate the registration window and let the user return to the main root
    go_back_button = Button(register_root, text="return to main lobby", command=lambda: return_to_lobby(register_root))
    go_back_button.pack()

    register_root.mainloop()


def set_new_password(new_password, username, mail, forgot_root, win):
    """
    Process: set the new password by sending a request to the server
    :parameter: new_password (string), username (string), mail (string), forgot_root (tkinter root), win (tkinter root)
    :return: Nothing
    """
    
    forgot_root.withdraw()
    
    # ask the server to update the user
    send_with_size(client_socket, f"UPPUSR|{username}|{new_password}")
    data = recv_by_size(client_socket).decode().split('|')
    print(data[1])
    
    check_injection(username, new_password, mail, "LOGUSR", win, forgot_root)

def close_forgot_win(forgot_root, login_win):
    """
    Process: close the forgot window and deiconify login window specificly
    :parameter: forgot_root (tkinter root), login_win (tkinter root)
    :return: Nothing
    """
    
    close_sub_win(forgot_root)
    login_win.deiconify()

def forgot_password(username, mail, win):
    """
    Process: open a forgot password diaglog and set up a new one if all is correct
    :parameter: username (string), mail (string), win (tkinter root)
    :return: Nothing
    """
    
    # withdraw the login win, and get a mail verification
    win.withdraw()
    mail_verified = mail_conformation(mail)
    
    if mail_verified:
        # if verified let the user enter a new password for the account
        forgot_root = Toplevel()
        forgot_root.title("New password")
        forgot_root.protocol("WM_DELETE_WINDOW", lambda: close_forgot_win(forgot_root, win))
        
        Label(forgot_root, text="Enter new password", font=('Helvetica', 20)).pack(pady=20)

        new_password = Entry(forgot_root, width=20)
        new_password.pack()
        
        
        new_pass_button = Button(forgot_root, text="confirm", command=lambda: set_new_password(new_password.get(), username, mail, forgot_root, win))
        new_pass_button.pack()
        
        forgot_root.mainloop()
    else:
        messagebox.showinfo("Mail Error", "closed conversation window")
        win.deiconify()


def login_func():
    """
    Process: Handles the login GUI and allows the client to enter information
    :parameter: Nothing
    :return: Nothing
    """

    # withdraw the main root and set up a toplevel root for the login window
    root.withdraw()

    login_root = Toplevel()
    login_root.title("Login Page")
    login_root.protocol("WM_DELETE_WINDOW", lambda: close_sub_win(login_root, True))

    login_root.geometry(f"{width}x{height}")

    Label(login_root, text="Login", bd=9, relief=GROOVE, font=("times new roman", 40, "bold"),
          bg="white", fg="green").pack()

    # use entry widget to get input from the user (username and password)
    Label(login_root, text="Enter Username", font=('Helvetica', 20)).pack(pady=20)

    username = Entry(login_root, width=20)
    username.pack()

    Label(login_root, text="Enter Password", font=('Helvetica', 20)).pack(pady=20)

    password = Entry(login_root, show="*", width=20)
    password.pack()
    
    Label(login_root, text="Enter Mail", font=('Helvetica', 20)).pack(pady=20)

    mail = Entry(login_root, width=20)
    mail.pack()

    # clicking this button will call the function that will check if a SQL injection attempt was made,
    # thus the client's interaction with this page isn't over
    submission_button = Button(login_root, text="submit", command=lambda: check_injection(
        username.get(), password.get(), mail.get(), "LOGUSR", login_root))
    submission_button.pack()
    
    # sorry I forgor the password
    forgot_button = Button(login_root, text="forgot password", command=lambda: forgot_password(username.get(), mail.get(), login_root))
    forgot_button.pack()

    # clicking this button will terminate the login window and let the user return to the main root
    go_back_button = Button(login_root, text="return to main lobby", command=lambda: return_to_lobby(login_root))
    go_back_button.pack()

    login_root.mainloop()


if __name__ == "__main__":
    # set up the tkinter root

    root = Tk()
    width = 800
    height = 600
    root.geometry(f"{width}x{height}")
    root.title("Multiplayer Lobby")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    title = Label(root, text="WELCOME TO THE LOBBY!\nEnter Username and Password", bd=9, relief=GROOVE,
                  font=("times new roman", 40, "bold"), bg="white", fg="green")
    title.pack(side=TOP, fill=X)

    credit = Label(root, text="Made by Idan Barkin", bd=9, relief=GROOVE, font=("times new roman", 30, "bold"),
                   bg="white", fg="green")
    credit.pack()

    # connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    register_button = Button(root, text="register", command=register_func)
    register_button.pack()

    login_button = Button(root, text="log in", command=login_func)
    login_button.pack()

    root.mainloop()
