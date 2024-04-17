__author__ = "Idan"

import socket

import threading
from tcp_by_size import send_with_size, recv_by_size
#from tkinter import messagebox, Listbox, END, SINGLE, simpledialog
#from tkinter import *
import email_handler
import time


#import tkinter as tk
#from tkinter import ttk
import customtkinter as ctk
#from classes import Message


#class CustomApp(ctk.CTk):
#    def __init__(self):
#        super().__init__()
#
#        self.title("Custom Tkinter Application")
#        self.geometry("400x300")
#
#        self.container = ctk.CTkFrame(self)
#        self.container.pack(side="top", fill="both", expand=True)
#        self.container.grid_rowconfigure(0, weight=1)
#        self.container.grid_columnconfigure(0, weight=1)
#
#        self.frames = {}
#        for F in (HomePage, SettingsPage, RegisterPage, LoginPage):
#            frame = F(self.container, self)
#            self.frames[F] = frame
#            frame.grid(row=0, column=0, sticky="nsew")
#
#        self.show_page(HomePage)
#
#    def show_page(self, cont):
#        frame = self.frames[cont]
#        frame.tkraise()
#
#
#class ConversationPreviewGUI:
#    pass
#
#
#class MessageGUI(ctk.CTkFrame):
#    def __init__(parent):
#        super().__init__(parent)
#        self.
#        
#        
#
#
#class HomePage(ctk.CTkFrame):
#    def __init__(self, parent, controller):
#        super().__init__(parent)
#
#        label = ctk.CTkLabel(self, text="Home Page", font=("Helvetica", 16))
#        label.pack(pady=10, padx=10)
#
#        button = ctk.CTkButton(self, text="Go to Settings", command=lambda: controller.show_page(SettingsPage))
#        button.pack(pady=10)
#
#        register_button = ctk.CTkButton(self,  text="Register", command=lambda: controller.show_page(RegisterPage))
#        register_button.pack(pady=10)
#
#        login_button = ctk.CTkButton(self, text="Login", command=lambda: controller.show_page(LoginPage))
#        login_button.pack(pady=10)
#
#
#class SettingsPage(ctk.CTkFrame):
#    def __init__(self, parent, controller):
#        super().__init__(parent)
#
#        label = ctk.CTkLabel(self, text="Settings Page", font=("Helvetica", 16))
#        label.pack(pady=10, padx=10)
#
#
#class RegisterPage(ctk.CTkFrame):
#    def __init__(self, parent, controller):
#        super().__init__(parent)
#
#        label = ctk.CTkLabel(self, text="Register Page", font=("Helvetica", 16))
#        label.pack(pady=10, padx=10)
#
#        name_label = ctk.CTkLabel(self, text="Name:")
#        name_label.pack()
#        name_entry = ctk.CTkEntry(self)
#        name_entry.pack()
#
#        password_label = ctk.CTkLabel(self, text="Password:")
#        password_label.pack()
#        password_entry = ctk.CTkEntry(self, show="*")
#        password_entry.pack()
#
#        email_label = ctk.CTkLabel(self, text="Email:")
#        email_label.pack()
#        email_entry = ctk.CTkEntry(self)
#        email_entry.pack()
#
#        register_button = ctk.CTkButton(self, text="Register", command=lambda: print("Registered!"))
#        register_button.pack(pady=10)
#
#
#class LoginPage(ctk.CTkFrame):
#    def __init__(self, parent, controller):
#        super().__init__(parent)
#
#        label = ctk.CTkLabel(self, text="Login Page", font=("Helvetica", 16))
#        label.pack(pady=10, padx=10)
#
#        name_label = ctk.CTkLabel(self, text="Name:")
#        name_label.pack()
#        name_entry = ctk.CTkEntry(self)
#        name_entry.pack()
#
#        password_label = ctk.CTkLabel(self, text="Password:")
#        password_label.pack()
#        password_entry = ctk.CTkEntry(self, show="*")
#        password_entry.pack()
#
#        login_button = ctk.CTkButton(self, text="Login", command=lambda: print("Logged in!"))
#        login_button.pack(pady=10)
#
#
#if __name__ == "__main__":
#    app = CustomApp()
#    app.mainloop()
#

###################

#import customtkinter as ctk

#normal version

#from tkinter import *
#
#class App(Tk):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.title("ThreadVortex")
#        self.geometry("800x600")
#
#        # Top bar with logo, search bar, and login/register buttons
#        self.top_bar = Frame(self, bg="purple")
#        self.top_bar.pack(fill=X)
#        self.logo = Label(self.top_bar, text="ThreadVortex", bg="purple", fg="white")
#        self.logo.pack(side=LEFT)
#        self.search_bar = Entry(self.top_bar)
#        self.search_bar.pack(side=LEFT)
#        self.login_button = Button(self.top_bar, text="Login")
#        self.login_button.pack(side=RIGHT)
#        self.register_button = Button(self.top_bar, text="Register")
#        self.register_button.pack(side=RIGHT)
#
#        # Sidebar with topics
#        self.sidebar = Frame(self, bg="purple")
#        self.sidebar.pack(side=LEFT, fill=Y)
#        self.topics = ["Gaming", "Cyber", "Tech", "Fashion", "Sports", "History", "Politics", "Physics"]
#        for topic in self.topics:
#            Button(self.sidebar, text=topic).pack()
#
#        # Add messages here
#        # Main content area with messages
#        self.content_area = Frame(self)
#        self.content_area.pack(fill=BOTH, expand=True)
#        self.messages = [
#            {"user": "User1", "date": "22.2.24", "content": "What does the 'yield' keyword do in Python?"},
#            {"user": "User2", "date": "20.2.24", "content": "🤔 IF YOU MAKE THE UNIVERSE A BETTER PLACE..."},
#            # Add more messages here...
#        ]
#        for message in self.messages:
#            Message(self.content_area, message["user"], message["date"], message["content"])
#
#class Message(Frame):
#    def __init__(self, parent, user, date, content):
#        super().__init__(parent, bg="white", highlightbackground="black", highlightthickness=2)
#        self.pack(fill=X, padx=5, pady=2)
#        self.user_label = Label(self, text=user, bg="white")
#        self.user_label.pack(side=LEFT)
#        self.date_label = Label(self, text=date, bg="white")
#        self.date_label.pack(side=RIGHT)
#        self.content_label = Label(self, text=content, bg="white")
#        self.content_label.pack()

#####

## sorta working scroll
#from tkinter import *
#
#class App(Tk):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.title("ThreadVortex")
#        self.geometry("800x600")
#
#        # Top bar with logo, search bar, and login/register buttons
#        self.top_bar = Frame(self, bg="purple")
#        self.top_bar.pack(fill=X)
#        self.logo = Label(self.top_bar, text="ThreadVortex", bg="purple", fg="white")
#        self.logo.pack(side=LEFT)
#        self.search_bar = Entry(self.top_bar)
#        self.search_bar.pack(side=LEFT)
#        self.login_button = Button(self.top_bar, text="Login")
#        self.login_button.pack(side=RIGHT)
#        self.register_button = Button(self.top_bar, text="Register")
#        self.register_button.pack(side=RIGHT)
#
#        # Sidebar with topics
#        self.sidebar = Frame(self, bg="purple")
#        self.sidebar.pack(side=LEFT, fill=Y)
#        self.topics = ["Gaming", "Cyber", "Tech", "Fashion", "Sports", "History", "Politics", "Physics"]
#        for topic in self.topics:
#            Button(self.sidebar, text=topic).pack()
#
#        # Main content area with messages
#        self.content_area = Canvas(self)
#        self.content_area.pack(fill=BOTH, expand=True)
#
#        # Create a frame inside the canvas to hold the messages
#        self.messages_frame = Frame(self.content_area)
#        self.content_area.create_window((0, 0), window=self.messages_frame, anchor='nw')
#
#        # set up vertical and horizontal scroll bars
#        scroll_bar_ver = Scrollbar(self, command=self.content_area.yview)
#        scroll_bar_ver.pack(side=RIGHT, fill=Y)
#        self.content_area.configure(yscrollcommand=scroll_bar_ver.set)
#
#        scroll_bar_hor = Scrollbar(self, command=self.content_area.xview, orient='horizontal')
#        scroll_bar_hor.pack(side=BOTTOM, fill=X)
#        self.content_area.configure(xscrollcommand=scroll_bar_hor.set)
#
#        # Function to update the scrollable region of the canvas
#        def on_configure(event):
#            self.content_area.configure(scrollregion=self.content_area.bbox("all"))
#
#        # Bind the function to the content frame's <Configure> event
#        self.messages_frame.bind("<Configure>", on_configure)
#
#        self.messages = [
#            {"user": "User1", "date": "22.2.24", "content": "What does the 'yield' keyword do in Python?"},
#            {"user": "User2", "date": "20.2.24", "content": "🤔 IF YOU MAKE THE UNIVERSE A BETTER PLACE..."},
#            # Add more messages here...
#        ]
#        for message in self.messages:
#            Message(self.messages_frame, message["user"], message["date"], message["content"])
#
#class Message(Frame):
#    def __init__(self, parent, user, date, content):
#        super().__init__(parent, bg="white", highlightbackground="black", highlightthickness=2)
#        self.pack(fill=X, padx=5, pady=2)
#        self.user_label = Label(self, text=user, bg="white")
#        self.user_label.pack(side=LEFT)
#        self.date_label = Label(self, text=date, bg="white")
#        self.date_label.pack(side=RIGHT)
#        self.content_label = Label(self, text=content, bg="white")
#        self.content_label.pack()




######

#from tkinter import *
#from tkinter import ttk
#
#class App(Tk):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.title("ThreadVortex")
#        self.geometry("800x600")
#
#        # Top bar with logo, search bar, and login/register buttons
#        self.top_bar = Frame(self, bg="purple")
#        self.top_bar.pack(fill=X)
#        self.logo = Label(self.top_bar, text="ThreadVortex", bg="purple", fg="white")
#        self.logo.pack(side=LEFT)
#        self.search_bar = Entry(self.top_bar)
#        self.search_bar.pack(side=LEFT)
#        self.login_button = Button(self.top_bar, text="Login")
#        self.login_button.pack(side=RIGHT)
#        self.register_button = Button(self.top_bar, text="Register")
#        self.register_button.pack(side=RIGHT)
#
#        # Sidebar with topics
#        self.sidebar = Frame(self, bg="purple")
#        self.sidebar.pack(side=LEFT, fill=Y)
#        self.topics = ["Gaming", "Cyber", "Tech", "Fashion", "Sports", "History", "Politics", "Physics"]
#        for topic in self.topics:
#            Button(self.sidebar, text=topic).pack()
#
#        # Add messages here
#        # Main content area with messages
#        self.content_area = Frame(self)
#        self.content_area.pack(fill=BOTH, expand=True)
#
#        # Create a canvas inside the content_area frame
#        self.canvas = Canvas(self.content_area)
#        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
#
#        # Add a scrollbar to the canvas
#        self.scrollbar = ttk.Scrollbar(self.content_area, orient=VERTICAL, command=self.canvas.yview)
#        self.scrollbar.pack(side=RIGHT, fill=Y)
#        self.canvas.configure(yscrollcommand=self.scrollbar.set)
#
#        # Add a frame inside the canvas
#        self.inner_frame = Frame(self.canvas)
#        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
#
#        self.messages = [
#            {"user": "User1", "date": "22.2.24", "content": "What does the 'yield' keyword do in Python?"},
#            {"user": "User2", "date": "20.2.24", "content": "🤔 IF YOU MAKE THE UNIVERSE A BETTER PLACE..."},
#            # Add more messages here...
#        ]
#        for message in self.messages:
#            Message(self.inner_frame, message["user"], message["date"], message["content"])
#
#        # Update inner_frame's scrollregion after configuring the canvas
#        self.inner_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
#
#class Message(Frame):
#    def __init__(self, parent, user, date, content):
#        super().__init__(parent, bg="white", highlightbackground="black", highlightthickness=2)
#        self.pack(fill=X, padx=5, pady=2)
#        self.user_label = Label(self, text=user, bg="white")
#        self.user_label.pack(side=LEFT)
#        self.date_label = Label(self, text=date, bg="white")
#        self.date_label.pack(side=RIGHT)
#        self.content_label = Label(self, text=content, bg="white")
#        self.content_label.pack()


        
#############
import customtkinter as ctk
import os
from PIL import ImageTk
import datetime
#from tkinter import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ThreadVortex")
        self.geometry("800x600")
        
        self.iconpath = ImageTk.PhotoImage(file=os.path.join("assets","Thread Vortex no text logo.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, RegisterPage, LoginPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page(HomePage)

    def show_page(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#class HomePage(ctk.CTkFrame):
#    def __init__(self, parent, controller):
#        super().__init__(parent)
#
#        label = ctk.CTkLabel(self, text="Home Page", font=("Helvetica", 16))
#        label.pack(pady=10, padx=10)
#
#        button = ctk.CTkButton(self, text="Go to Settings", command=lambda: controller.show_page(SettingsPage))
#        button.pack(pady=10)
#
#        register_button = ctk.CTkButton(self,  text="Register", command=lambda: controller.show_page(RegisterPage))
#        register_button.pack(pady=10)
#
#        login_button = ctk.CTkButton(self, text="Login", command=lambda: controller.show_page(LoginPage))
#        login_button.pack(pady=10)


#class SettingsPage(ctk.CTkFrame):
#    def __init__(self, parent, controller):
#        super().__init__(parent)
#
#        label = ctk.CTkLabel(self, text="Settings Page", font=("Helvetica", 16))
#        label.pack(pady=10, padx=10)


class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Register Page", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        name_label = ctk.CTkLabel(self, text="Name:")
        name_label.pack()
        name_entry = ctk.CTkEntry(self)
        name_entry.pack()

        password_label = ctk.CTkLabel(self, text="Password:")
        password_label.pack()
        password_entry = ctk.CTkEntry(self, show="*")
        password_entry.pack()

        email_label = ctk.CTkLabel(self, text="Email:")
        email_label.pack()
        email_entry = ctk.CTkEntry(self)
        email_entry.pack()
        
        
        age_label = ctk.CTkLabel(self, text="Age:")
        age_label.pack()
        age_entry = ctk.CTkEntry(self)
        age_entry.pack()

        gender_label = ctk.CTkLabel(self, text="Gender:")
        gender_label.pack()
        gender_entry = ctk.CTkEntry(self)
        gender_entry.pack()

        country_label = ctk.CTkLabel(self, text="Country:")
        country_label.pack()
        country_entry = ctk.CTkEntry(self)
        country_entry.pack()

        occupation_label = ctk.CTkLabel(self, text="Occupation:")
        occupation_label.pack()
        occupation_entry = ctk.CTkEntry(self)
        occupation_entry.pack()

        description_label = ctk.CTkLabel(self, text="Description:")
        description_label.pack()
        description_entry = ctk.CTkTextbox(self)
        description_entry.pack()

        register_button = ctk.CTkButton(self, text="Register", command=lambda: self.user_register(name_entry.get(), password_entry.get(), email_entry.get(), age_entry.get(), gender_entry.get(), country_entry.get(), occupation_entry.get(), datetime.datetime.now(), description_entry.get("1.0", "end-1c")))
        register_button.pack(pady=10)
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: controller.show_page(HomePage))
        go_back_button.pack(pady=10)
    
    def user_register(self, name, password, email, age, gender, country, occupation, date_creation, description):
        send_with_size(client_socket, f"REGUSR|{name}|{password}|{email}|{age}|{gender}|{country}|{occupation}|{date_creation}|{description}")
        data = recv_by_size(client_socket).decode().split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "REGUSR":
            pass
        
        


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Login Page", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        name_label = ctk.CTkLabel(self, text="Name:")
        name_label.pack()
        name_entry = ctk.CTkEntry(self)
        name_entry.pack()

        password_label = ctk.CTkLabel(self, text="Password:")
        password_label.pack()
        password_entry = ctk.CTkEntry(self, show="*")
        password_entry.pack()
        
        email_label = ctk.CTkLabel(self, text="Email:")
        email_label.pack()
        email_entry = ctk.CTkEntry(self)
        email_entry.pack()

        login_button = ctk.CTkButton(self, text="Login", command=lambda: self.user_login(name_entry.get(), password_entry.get(), email_entry.get()))
        login_button.pack(pady=10)
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: controller.show_page(HomePage))
        go_back_button.pack(pady=10)
    
    def user_login(self, name, password, email):
        send_with_size(client_socket, f"LOGUSR|{name}|{password}|{email}")


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Top bar with logo, search bar, and login/register buttons
        self.top_bar = ctk.CTkFrame(self, fg_color="purple", bg_color="purple")
        self.top_bar.pack(fill=ctk.X)
        self.logo = ctk.CTkLabel(self.top_bar, text="ThreadVortex", fg_color="purple", bg_color="purple", text_color="white")
        self.logo.pack(side=ctk.LEFT, padx=12, pady=1.25)
        self.search_bar = ctk.CTkEntry(self.top_bar)
        self.search_bar.pack(side=ctk.LEFT, padx=1)
        self.search_button = ctk.CTkButton(self.top_bar, text="Search🔎", fg_color="white", text_color="black", hover_color="cyan", width=100)
        self.search_button.pack(side=ctk.LEFT)
        self.login_button = ctk.CTkButton(self.top_bar, text="Login", fg_color="white", text_color="black", hover_color="cyan", command=lambda: controller.show_page(LoginPage))
        self.login_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)
        self.register_button = ctk.CTkButton(self.top_bar, text="Register", fg_color="white", text_color="black", hover_color="cyan", command=lambda: controller.show_page(RegisterPage))
        self.register_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)

        # Sidebar with topics
        self.sidebar = ctk.CTkFrame(self, bg_color="purple", fg_color="purple")
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
        self.topics = ["Gaming", "Cyber", "Tech", "Fashion", "Sports", "History", "Politics", "Physics"]
        for topic in self.topics:
            ctk.CTkButton(self.sidebar, text=topic, fg_color="white", text_color="black", hover_color="cyan", width=100).pack(pady=2)

        # Add messages here
        # Main content area with messages
        self.content_area = ctk.CTkScrollableFrame(self)
        self.content_area.pack(fill=ctk.BOTH, expand=True)
        self.messages = [
            {"user": "User1", "date": "22.2.24", "content": "What does the 'yield' keyword do in Python?"},
            {"user": "User2", "date": "20.2.24", "content": "🤔 IF YOU MAKE THE UNIVERSE A BETTER PLACE..."},
            # Add more messages here...
        ]
        for message in self.messages:
            Message(self.content_area, message["user"], message["date"], message["content"])

#class App(ctk.CTk):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.title("ThreadVortex")
#        self.geometry("800x600")
#        self.iconpath = ImageTk.PhotoImage(file=os.path.join("assets","Thread Vortex no text logo.png"))
#        self.wm_iconbitmap()
#        self.iconphoto(False, self.iconpath)
#        # Top bar with logo, search bar, and login/register buttons
#        self.top_bar = ctk.CTkFrame(self, fg_color="purple", bg_color="purple")
#        self.top_bar.pack(fill=ctk.X)
#        self.logo = ctk.CTkLabel(self.top_bar, text="ThreadVortex", fg_color="purple", bg_color="purple", text_color="white")
#        self.logo.pack(side=ctk.LEFT, padx=12, pady=1.25)
#        self.search_bar = ctk.CTkEntry(self.top_bar)
#        self.search_bar.pack(side=ctk.LEFT, padx=1)
#        self.search_button = ctk.CTkButton(self.top_bar, text="Search🔎", fg_color="white", text_color="black", hover_color="cyan", width=100)
#        self.search_button.pack(side=ctk.LEFT)
#        self.login_button = ctk.CTkButton(self.top_bar, text="Login", fg_color="white", text_color="black", hover_color="cyan")
#        self.login_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)
#        self.register_button = ctk.CTkButton(self.top_bar, text="Register", fg_color="white", text_color="black", hover_color="cyan")
#        self.register_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)
#
#        # Sidebar with topics
#        self.sidebar = ctk.CTkFrame(self, bg_color="purple", fg_color="purple")
#        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
#        self.topics = ["Gaming", "Cyber", "Tech", "Fashion", "Sports", "History", "Politics", "Physics"]
#        for topic in self.topics:
#            ctk.CTkButton(self.sidebar, text=topic, fg_color="white", text_color="black", hover_color="cyan", width=100).pack(pady=2)
#
#        # Add messages here
#        # Main content area with messages
#        self.content_area = ctk.CTkScrollableFrame(self)
#        self.content_area.pack(fill=ctk.BOTH, expand=True)
#        self.messages = [
#            {"user": "User1", "date": "22.2.24", "content": "What does the 'yield' keyword do in Python?"},
#            {"user": "User2", "date": "20.2.24", "content": "🤔 IF YOU MAKE THE UNIVERSE A BETTER PLACE..."},
#            # Add more messages here...
#        ]
#        for message in self.messages:
#            Message(self.content_area, message["user"], message["date"], message["content"])

class Message(ctk.CTkFrame):
    def __init__(self, parent, user, date, content):
        super().__init__(parent, height=100, fg_color="white", corner_radius=50, border_color="black", border_width=2)  # Increase border_width
        self.pack_propagate(False)
        self.pack(fill=ctk.X, padx=4, pady=2)
        self.user_label = ctk.CTkLabel(self, text=user)
        self.user_label.pack(side=ctk.LEFT, padx=10)
        self.date_label = ctk.CTkLabel(self, text=date)
        self.date_label.pack(side=ctk.RIGHT, padx=10)
        self.content_label = ctk.CTkLabel(self, text=content)
        self.content_label.pack(side=ctk.TOP, pady=35)


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    app = App()
    app.mainloop()
