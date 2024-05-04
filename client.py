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
from PIL import ImageTk, Image
import datetime
import classes
from tkinter import messagebox
#from tkinter import *


#class App(ctk.CTk):
#    def __init__(self):
#        super().__init__()
#        self.title("ThreadVortex")
#        self.geometry("800x600")
#        
#        self.iconpath = ImageTk.PhotoImage(file=os.path.join("assets","Thread Vortex no text logo.png"))
#        self.wm_iconbitmap()
#        self.iconphoto(False, self.iconpath)
#        
#        self.container = ctk.CTkFrame(self)
#        self.container.pack(side="top", fill="both", expand=True)
#        self.container.grid_rowconfigure(0, weight=1)
#        self.container.grid_columnconfigure(0, weight=1)
#
#        self.frames = {}
#        for F in (HomePage_Unconnected, HomePage_Connected, RegisterPage, LoginPage, EditProfilePage):
#            frame = F(self.container, self)
#            self.frames[F] = frame
#            frame.grid(row=0, column=0, sticky="nsew")
#
#        self.show_page(HomePage_Unconnected)
#
#    def show_page(self, cont):
#        frame = self.frames[cont]
#        frame.tkraise()

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

        #self.frames = {}
        #for F in (HomePage_Unconnected, HomePage_Connected, RegisterPage, LoginPage, EditProfilePage):
        #    frame = F(self.container, self)
        #    self.frames[F] = frame
        #    frame.grid(row=0, column=0, sticky="nsew")

        #self.show_page(HomePage_Unconnected)
        self.frame = HomePage_Unconnected(self.container, self)
        self.frame.grid(row=0, column=0, sticky="nsew")

    #def show_page(self, cont, profile_username=None, connected=None): # possible args are parameters from certain classes. ViewProfile for exa,ple can have an arg of "Username"
    #    #frame = self.frames[cont]
    #    #frame.tkraise()
    #    
    #    # i need to somehow use forget on the current used class frame and grid/pack the new class frame i want to use
    #    self.frame.forget()
    #    if profile_username is not None:
    #        if connected == "connected":
    #            self.frame = cont(self.container, self, profile_username, "connected")
    #        else:
    #            self.frame = cont(self.container, self, profile_username, "unconnected")
    #    else:
    #        self.frame = cont(self.container, self)
    #    self.frame.grid(row=0, column=0, sticky="nsew")
    def show_page(self, cont, **kwargs): # possible kwargs currently are: profile_username=user_profile.username, connected_status="connected"
        #frame = self.frames[cont]
        #frame.tkraise()
        
        # use forget on the current used class frame and grid the new class frame i want to use
        self.frame.forget()
        if "profile_username" in kwargs and "connected_status" in kwargs:
                self.frame = cont(self.container, self, kwargs.pop("profile_username"), kwargs.pop("connected_status"))
        else:
            self.frame = cont(self.container, self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        
        

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

        register_button = ctk.CTkButton(self, text="Register", command=lambda: self.user_register_h(controller, name_entry.get(), password_entry.get(), email_entry.get(), age_entry.get(), gender_entry.get(), country_entry.get(), occupation_entry.get(), datetime.datetime.now(), description_entry.get("1.0", "end-1c")))
        register_button.pack(pady=10)
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: controller.show_page(HomePage_Unconnected))
        go_back_button.pack(pady=10)
    
    def user_register_h(self, controller, username, password, mail, age, gender, country, occupation, date_creation, description):
        global user_profile
        
        user_profile = classes.User(username, password, mail, age, gender, country, occupation, date_creation, description)
        self.user_register(controller, user_profile)
    
    def user_register(self, controller, user_profile: classes.User):
        send_with_size(client_socket, f"REGUSR|{user_profile.username}|{user_profile.password}|{user_profile.mail}|{user_profile.age}|{user_profile.gender}|{user_profile.country}|{user_profile.occupation}|{user_profile.date_creation}|{user_profile.description}")
        data = recv_by_size(client_socket).decode().split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "REGUSR":
            if data[1] == "new_user":
                controller.show_page(HomePage_Connected)
                
        
        


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

        login_button = ctk.CTkButton(self, text="Login", command=lambda: self.user_login(controller, name_entry.get(), password_entry.get(), email_entry.get()))
        login_button.pack(pady=10)
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: controller.show_page(HomePage_Unconnected))
        go_back_button.pack(pady=10)
    
    def user_login(self, controller, name, password, email):
        global user_profile
        send_with_size(client_socket, f"LOGUSR|{name}|{password}|{email}")
        data = recv_by_size(client_socket).decode().split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "LOGUSR":
            if data[1] == "correct_identification":
                user_profile = classes.User(data[2], None, data[3], int(data[4]), data[5], data[6], data[7], data[8], data[9])
                controller.show_page(HomePage_Connected)
        
        




class HomePage_Unconnected(ctk.CTkFrame):
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

class HomePage_Connected(ctk.CTkFrame):
    def __init__(self, parent, controller):
        global user_profile
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
        self.disconnect_button = ctk.CTkButton(self.top_bar, text="Disconnect", fg_color="white", text_color="black", hover_color="cyan", command=lambda: self.disconnect(controller))
        self.disconnect_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)
        self.edit_profile_button = ctk.CTkButton(self.top_bar, text="Edit Profile", fg_color="white", text_color="black", hover_color="cyan", command=lambda: controller.show_page(EditProfilePage))
        self.edit_profile_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)
        
        #profile info
        view_profile_icon_image = Image.open(fp=os.path.join("assets","default user icon 2.png"))
        #profile_icon_image.resize((40, 40), Image.LANCZOS)
        #
        #self.profile_icon_tkimage = ImageTk.PhotoImage(image=profile_icon_image)
        
        #self.view_profile_icon_path = ImageTk.PhotoImage(file=os.path.join("assets","default user icon 2.png"))
        
        self.view_profile_icon = ctk.CTkImage(light_image=view_profile_icon_image, size=(40, 40))
        self.view_profile_button = ctk.CTkButton(self.top_bar, width=100, text="", image=self.view_profile_icon, command=lambda: controller.show_page(ViewProfile, profile_username=user_profile.username, connected_status="connected"))
        #self.view_profile_button.configure(width=40, height=40)
        self.view_profile_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)

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
    
    def disconnect(self, controller):
        if messagebox.askokcancel("Warning", "You are about to disconnect from the program."):
            controller.show_page(HomePage_Unconnected)

class EditProfilePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        global user_profile
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Edit Profile Page", font=("Helvetica", 16))
        label.pack(pady=10, padx=10)

        password_label = ctk.CTkLabel(self, text="Password:")
        password_label.pack()
        password_entry = ctk.CTkEntry(self, show="*")
        password_entry.pack()
        
        age_label = ctk.CTkLabel(self, text="Age:")
        age_label.pack()
        age_entry = ctk.CTkEntry(self)
        age_entry.insert(0, user_profile.age)
        age_entry.pack()

        gender_label = ctk.CTkLabel(self, text="Gender:")
        gender_label.pack()
        gender_entry = ctk.CTkEntry(self)
        gender_entry.insert(0, user_profile.gender)
        gender_entry.pack()

        country_label = ctk.CTkLabel(self, text="Country:")
        country_label.pack()
        country_entry = ctk.CTkEntry(self)
        country_entry.insert(0, user_profile.country)
        country_entry.pack()

        occupation_label = ctk.CTkLabel(self, text="Occupation:")
        occupation_label.pack()
        occupation_entry = ctk.CTkEntry(self)
        occupation_entry.insert(0, user_profile.occupation)
        occupation_entry.pack()

        description_label = ctk.CTkLabel(self, text="Description:")
        description_label.pack()
        description_entry = ctk.CTkTextbox(self)
        description_entry.insert('1.0', user_profile.description)
        description_entry.pack()

        register_button = ctk.CTkButton(self, text="Commit changes", command=lambda: self.user_edit_profile_h(controller, password_entry.get(), age_entry.get(), gender_entry.get(), country_entry.get(), occupation_entry.get(), description_entry.get("1.0", "end-1c")))
        register_button.pack(pady=10)
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: controller.show_page(HomePage_Connected))
        go_back_button.pack(pady=10)
    
    def user_edit_profile_h(self, controller, password, age, gender, country, occupation, description):
        global user_profile
        
        user_profile.edit_profile(int(age), gender, country, occupation, description)
        self.user_edit_profile(controller, user_profile, password)
    
    def user_edit_profile(self, controller, user_profile: classes.User, password):
        send_with_size(client_socket, f"EDTUSR|{user_profile.username}|{password}|{user_profile.mail}|{user_profile.age}|{user_profile.gender}|{user_profile.country}|{user_profile.occupation}|{user_profile.date_creation}|{user_profile.description}")
        data = recv_by_size(client_socket).decode().split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "EDTUSR":
            if data[1] == "edited_profile":
                messagebox.showinfo("Info", "User profile updated successfuly")
                controller.show_page(HomePage_Connected)
        

class ViewProfile(ctk.CTkFrame):
    def __init__(self, parent, controller, profile_username, connected_status):
        global user_profile
        super().__init__(parent)
        
        
        if profile_username == user_profile.username:
            user_data: classes.User = classes.User.clone(user_profile)
        else:
            # i will deal with this later. in this case a will ask the server for the data of the user who has this username, the sever will take it from the database - send to client and it will be displayed.
            pass
        
        name_label = ctk.CTkLabel(self, text=f"The info page of \"{user_data.username}\"")
        name_label.pack(pady=2)

        email_label = ctk.CTkLabel(self, text=f"Email: {user_data.mail}")
        email_label.pack()
        
        age_label = ctk.CTkLabel(self, text=f"Age: {user_data.age}")
        age_label.pack()

        gender_label = ctk.CTkLabel(self, text=f"Gender: {user_data.gender}")
        gender_label.pack()

        country_label = ctk.CTkLabel(self, text=f"Country: {user_data.country}")
        country_label.pack()

        occupation_label = ctk.CTkLabel(self, text=f"Occupation: {user_data.occupation}")
        occupation_label.pack()
        
        member_since_label = ctk.CTkLabel(self, text=f"Member Since: {user_data.date_creation}")
        member_since_label.pack()

        description_label = ctk.CTkLabel(self, text=f"Description: {user_data.description}")
        description_label.pack()
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: self.go_back_h(controller, connected_status))
        go_back_button.pack(pady=10)
    
    def go_back_h(self, controller, connected_status):
        if connected_status == "connected":
            controller.show_page(HomePage_Connected)
        else:
            controller.show_page(HomePage_Unconnected)
        
        
        
        
        
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
    user_profile = None
    app = App()
    app.mainloop()
