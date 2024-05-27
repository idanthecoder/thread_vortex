__author__ = "Idan"

import socket
import threading
from tcp_by_size import send_with_size, recv_by_size
import email_handler
import time
import customtkinter as ctk
import os
from PIL import ImageTk, Image
import datetime
import classes
from tkinter import messagebox
from modified_gui import ModifiedCTkScrollableFrame
from encryption_handler import EncryptionHandler
from text_to_speech_handler import speak_text, stop_speech

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

        self.saved_frames = {}
        self.frame = OpeningScreen(self.container, self)
        self.saved_frames[OpeningScreen] = self.frame
        self.frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, class_to_show, **kwargs):
        """
        Process: 
        Parameters: class_to_show - the class to switch to,
        **kwargs - possible kwargs currently are for example: profile_username="username", title="title", class_return_to=class, edited_profile=True/False
        Returns: Nothing.
        """
        
        # if the requested class is already saved in the dictinary I want to use it in the state it was last left in
        if class_to_show in self.saved_frames.keys():
            # if those parameters are in kwargs then this relates to the ViewProfile class
            if "profile_username" in kwargs and "class_return_to" in kwargs and "edited_profile" in kwargs:
                profile_username = kwargs.pop("profile_username")
                class_return_to = kwargs.pop("class_return_to")
                edited_profile = kwargs.pop("edited_profile")
                
                # if at least one of the values is new then reset the value for this class and grid it
                if profile_username != self.saved_frames[class_to_show].profile_username or class_return_to != self.saved_frames[class_to_show].class_return_to or edited_profile != self.saved_frames[class_to_show].edited_profile:
                    self.frame = class_to_show(self.container, self, profile_username, class_return_to, edited_profile)
                    self.saved_frames[class_to_show] = self.frame
                    self.frame.grid(row=0, column=0, sticky="nsew")
                    return
            
            # if this parameter is in kwargs then this relates to the InsideConversationGUI class
            elif "title" in kwargs:
                title = kwargs.pop("title")
                # if the value is new then it is a different conversation. Rreset the value for this class and grid it
                if title != self.saved_frames[class_to_show].title:
                    self.frame = class_to_show(self.container, self, title)
                    self.saved_frames[class_to_show] = self.frame
                    self.frame.grid(row=0, column=0, sticky="nsew")
                    return
            
            elif "str_to_search" in kwargs:
                str_to_search = kwargs.pop("str_to_search")
                if str_to_search != self.saved_frames[class_to_show].str_to_search:
                    self.frame = class_to_show(self.container, self, str_to_search)
                    self.saved_frames[class_to_show] = self.frame
                    self.frame.grid(row=0, column=0, sticky="nsew")
                    return
            
            # if no kwargs are given or if their values are the same then user tkraise to switch frames
            self.frame = self.saved_frames[class_to_show]
            self.frame.tkraise()
        else:
            # if it is a totally new class then create an instance of it and grid it
            if "profile_username" in kwargs and "class_return_to" in kwargs and "edited_profile" in kwargs:
                self.frame = class_to_show(self.container, self, kwargs.pop("profile_username"), kwargs.pop("class_return_to"), kwargs.pop("edited_profile"))
            elif "title" in kwargs:
                self.frame = class_to_show(self.container, self, kwargs.pop("title"))
            elif "str_to_search" in kwargs:
                self.frame = class_to_show(self.container, self, kwargs.pop("str_to_search"))
            else:
                self.frame = class_to_show(self.container, self)
            
            self.saved_frames[class_to_show] = self.frame
            self.frame.grid(row=0, column=0, sticky="nsew")
        

class OpeningScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Top bar with logo, search bar, and login/register buttons
        self.top_bar = ctk.CTkFrame(self, fg_color="purple", bg_color="purple")
        self.top_bar.pack(fill=ctk.X)
        self.logo = ctk.CTkLabel(self.top_bar, text="ThreadVortex", fg_color="purple", bg_color="purple", text_color="white")
        self.logo.pack(padx=12, pady=1.25)
        
        
        self.choosing_area = ctk.CTkFrame(self, fg_color="#D391FA")
        self.choosing_area.pack(fill=ctk.BOTH, expand=True)
        
        self.login_button = ctk.CTkButton(self.choosing_area, width=300, height=250, text="Login", fg_color="white", text_color="black", hover_color="cyan", command=lambda: controller.show_page(LoginPage))
        self.login_button.pack(padx=1.25, pady=1.25)
        self.register_button = ctk.CTkButton(self.choosing_area, width=300, height=250, text="Register", fg_color="white", text_color="black", hover_color="cyan", command=lambda: controller.show_page(RegisterPage))
        self.register_button.pack(padx=1.25, pady=1.25)


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

        register_button = ctk.CTkButton(self, text="Register", command=lambda: self.user_register_h(controller, name_entry.get(), password_entry.get(), email_entry.get(), age_entry.get(), gender_entry.get(), country_entry.get(), occupation_entry.get(), description_entry.get("1.0", "end-1c")))
        register_button.pack(pady=10)
        
        go_back_button = ctk.CTkButton(self, text="Return to opening screen", command=lambda: controller.show_page(OpeningScreen))
        go_back_button.pack(pady=10)
    
    def user_register_h(self, controller, username, password, mail, age, gender, country, occupation, description):
        global user_profile
        
        current_date = datetime.datetime.now()
        date_creation = f"{current_date.day}/{current_date.month}/{current_date.year} {current_date.hour}:{current_date.minute}"
        
        user_profile = classes.User(username, password, mail, age, gender, country, occupation, date_creation, description)
        self.user_register(controller, user_profile)
    
    def user_register(self, controller, user_profile: classes.User):
        send_with_size(client_socket, handle_encryption.cipher_data(f"REGUSR|{user_profile.username}|{user_profile.password}|{user_profile.mail}|{user_profile.age}|{user_profile.gender}|{user_profile.country}|{user_profile.occupation}|{user_profile.date_creation}|{user_profile.description}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
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
        
        go_back_button = ctk.CTkButton(self, text="Return to opening screen", command=lambda: controller.show_page(OpeningScreen))
        go_back_button.pack(pady=10)
    
    def user_login(self, controller, name, password, email):
        global user_profile
        send_with_size(client_socket, handle_encryption.cipher_data(f"LOGUSR|{name}|{password}|{email}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "LOGUSR":
            if data[1] == "correct_identification":
                user_profile = classes.User(data[2], None, data[3], data[4], data[5], data[6], data[7], data[8], data[9])
                controller.show_page(HomePage_Connected)


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
        self.search_button = ctk.CTkButton(self.top_bar, text="Search🔎", fg_color="white", text_color="black", hover_color="cyan", width=100, command=lambda: controller.show_page(SearchPage, str_to_search=self.search_bar.get()))
        self.search_button.pack(side=ctk.LEFT)
        self.disconnect_button = ctk.CTkButton(self.top_bar, text="Disconnect", fg_color="white", text_color="black", hover_color="cyan", command=lambda: self.disconnect(controller))
        self.disconnect_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)
        self.edit_profile_button = ctk.CTkButton(self.top_bar, text="Edit Profile", fg_color="white", text_color="black", hover_color="cyan", command=lambda: controller.show_page(EditProfilePage))
        self.edit_profile_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)
        
        # view profile button
        view_profile_icon_image = Image.open(fp=os.path.join("assets","default user icon 2.png"))
        self.view_profile_icon = ctk.CTkImage(light_image=view_profile_icon_image, size=(40, 40))
        self.view_profile_button = ctk.CTkButton(self.top_bar, width=100, text="", image=self.view_profile_icon, command=lambda: controller.show_page(ViewProfile, profile_username=user_profile.username, class_return_to=HomePage_Connected, edited_profile=False))
        self.view_profile_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)

        # Sidebar with topics
        self.sidebar = ctk.CTkFrame(self, bg_color="purple", fg_color="purple")
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
        
        # new conversation button
        new_conversation_icon_image = Image.open(fp=os.path.join("assets","plus icon 3.png"))
        self.new_conversation_icon = ctk.CTkImage(light_image=new_conversation_icon_image, size=(40, 40))
        self.new_conversation_button = ctk.CTkButton(self.sidebar, fg_color="white", width=100, text="", image=self.new_conversation_icon, command=lambda: controller.show_page(CreateNewConversation))
        self.new_conversation_button.pack(side=ctk.TOP, padx=1.25, pady=1.25)
        
        
        # change configuration button
        self.configuration_frame = ctk.CTkFrame(self.sidebar, fg_color="white")
        self.configuration_frame.pack()
        
        reconfiguration_icon_image = Image.open(fp=os.path.join("assets","sort icon 1.png"))
        self.reconfiguration_icon = ctk.CTkImage(light_image=reconfiguration_icon_image, size=(40, 40))
        self.reconfiguration_label = ctk.CTkLabel(self.configuration_frame, image=self.reconfiguration_icon, text="")
        self.reconfiguration_label.pack(side=ctk.TOP, padx=1.25, pady=1.25)
        
        optionmenu_var = ctk.StringVar(value="")  # set initial value
        reconfiguration_combobox = ctk.CTkOptionMenu(master=self.configuration_frame,
                                       values=["", "Sort Alphabetically", "Sort Alphabetically (Reverse)", "Sort Chronologically", "Sort Chronologically (Reverse)", "Sort By Popularity", "Sort By Popularity (Reverse)"],
                                       command=self.reconfigure_conversations_screen,
                                       variable=optionmenu_var)
        reconfiguration_combobox.pack(side=ctk.TOP, padx=1.25, pady=1.25)
        
        
        self.topics = ["Gaming", "Cyber", "Tech", "Fashion", "Sports", "History", "Politics", "Physics"]
        for topic in self.topics:
            ctk.CTkButton(self.sidebar, text=topic, fg_color="white", text_color="black", hover_color="cyan", width=100).pack(pady=2)

        # Add messages here
        # Main content area with messages
        self.content_area = ModifiedCTkScrollableFrame(self)
        self.content_area.pack(fill=ctk.BOTH, expand=True)
        
        self.conversation_handler = HandleConversations(self.content_area, controller, 5)
        
        self.content_area.set_func(self.conversation_handler.request_more)
        
        #self.request_conversations_button = ctk.CTkButton(self.content_area, text="More Conversations", fg_color="white",  border_color="black", border_width=2, text_color="black", hover_color="cyan", command=lambda: self.conversation_handler.request_more(self.content_area, controller, 5))
        #self.request_conversations_button.pack(side=ctk.BOTTOM)
    
    def disconnect(self, controller):
        if messagebox.askokcancel("Warning", "You are about to disconnect from the program."):
            controller.show_page(OpeningScreen)
    
    def reconfigure_conversations_screen(self, choice):
        "Sort Alphabetically", "Sort Alphabetically (Reverse)", "Sort Chronologically", "Sort Chronologically (Reverse)", "Sort By Popularity", "Sort By Popularity (Reverse)"
        
        # if the default string was chosen then anyway nothing will change
        if choice == "":
            return
        
        clear_frame(self.content_area)
        
        self.conversation_handler.reconfigure_conversation_order(choice)
    
def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


class SearchPage(ctk.CTkFrame):
    def __init__(self, parent, controller, str_to_search):
            super().__init__(parent)
            self.str_to_search = str_to_search
            self.top_bar = ctk.CTkFrame(self, fg_color="purple", bg_color="purple")
            self.top_bar.pack(fill=ctk.X)
            self.logo = ctk.CTkLabel(self.top_bar, text="ThreadVortex", fg_color="purple", bg_color="purple", text_color="white")
            self.logo.pack(side=ctk.LEFT, padx=12, pady=1.25)
            self.search_bar = ctk.CTkEntry(self.top_bar)
            self.search_bar.pack(side=ctk.LEFT, padx=1)
            self.search_button = ctk.CTkButton(self.top_bar, text="Search🔎", fg_color="white", text_color="black", hover_color="cyan", width=100, command=lambda: self.search_again(self.search_bar.get()))
            self.search_button.pack(side=ctk.LEFT)
            
            # Sidebar with topics
            self.sidebar = ctk.CTkFrame(self, bg_color="purple", fg_color="purple")
            self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
            
            self.go_back_button = ctk.CTkButton(self.sidebar, fg_color="white", text_color="black", hover_color="cyan", width=100, text="Return to Home page", command=lambda: controller.show_page(HomePage_Connected))
            self.go_back_button.pack(side=ctk.TOP, padx=1.25, pady=1.25)
            
            # Main content area with messages
            self.content_area = ctk.CTkScrollableFrame(self)
            self.content_area.pack(fill=ctk.BOTH, expand=True)
            
            self.conversation_handler = HandleConversations(self.content_area, controller, 5, True)
            self.conversation_handler.search_all(str_to_search)
    
    def search_again(self, to_search):
        clear_frame(self.content_area)
        self.conversation_handler.search_all(to_search)
                
                
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

        edit_profile_button = ctk.CTkButton(self, text="Commit changes", command=lambda: self.user_edit_profile_h(controller, password_entry.get(), age_entry.get(), gender_entry.get(), country_entry.get(), occupation_entry.get(), description_entry.get("1.0", "end-1c")))
        edit_profile_button.pack(pady=10)
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: controller.show_page(HomePage_Connected))
        go_back_button.pack(pady=10)
    
    def user_edit_profile_h(self, controller, password, age, gender, country, occupation, description):
        global user_profile
        
        user_profile.edit_profile(age, gender, country, occupation, description)
        self.user_edit_profile(controller, user_profile, password)
    
    def user_edit_profile(self, controller, user_profile: classes.User, password):
        send_with_size(client_socket, handle_encryption.cipher_data(f"EDTUSR|{user_profile.username}|{password}|{user_profile.mail}|{user_profile.age}|{user_profile.gender}|{user_profile.country}|{user_profile.occupation}|{user_profile.date_creation}|{user_profile.description}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "EDTUSR":
            if data[1] == "edited_profile":
                messagebox.showinfo("Info", "User profile updated successfuly")
                controller.show_page(ViewProfile, profile_username=user_profile.username, class_return_to=HomePage_Connected, edited_profile=True)


class ViewProfile(ctk.CTkFrame):
    def __init__(self, parent, controller, profile_username, class_return_to, edited_profile):
        global user_profile
        super().__init__(parent)
        self.profile_username = profile_username
        self.class_return_to = class_return_to
        self.edited_profile = edited_profile
        
        if profile_username == user_profile.username:
            user_data: classes.User = classes.User.clone(user_profile)
        else:
            # i will deal with this later. in this case a will ask the server for the data of the user who has this username, the sever will take it from the database - send to client and it will be displayed.
            user_data = self.get_other_user_data()
            if user_data == "no_user":
                messagebox.showwarning("Warning", "No such user exists in the database")
                controller.show_page(class_return_to)
        
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
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: controller.show_page(class_return_to))
        go_back_button.pack(pady=10)
    
    def get_other_user_data(self):
        send_with_size(client_socket, handle_encryption.cipher_data(f"GETUSR|{self.profile_username}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "GETUSR":
            if data[1] != "no_user":
                user_data = classes.User(data[1], None, data[2], data[3], data[4], data[5], data[6], data[7], data[8])
                return user_data
            else:
                return "no_user"
             

class CreateNewConversation(ctk.CTkFrame):
    def __init__(self, parent, controller):
        global user_profile
        super().__init__(parent)
        
        frame_title_label = ctk.CTkLabel(self, text="Create a new conversation:")
        frame_title_label.pack(pady=4)
        
        
        conversation_title_label = ctk.CTkLabel(self, text="Title of the conversation:")
        conversation_title_label.pack()
        conversation_title_entry = ctk.CTkEntry(self)
        conversation_title_entry.pack()
        
        message_content_label = ctk.CTkLabel(self, text="Message content:")
        message_content_label.pack()
        message_content_entry = ctk.CTkTextbox(self)
        message_content_entry.pack()
        
        restriction_label = ctk.CTkLabel(self, text="Restrict access:")
        restriction_label.pack()
        radio_var = ctk.StringVar()
        restriction_radiobutton1 = ctk.CTkRadioButton(master=self, text="18+", variable= radio_var, value="18+")
        restriction_radiobutton2 = ctk.CTkRadioButton(master=self, text="Unrestricted", variable= radio_var, value="unrestricted")
        restriction_radiobutton1.pack(padx=20, pady=10)
        restriction_radiobutton2.pack(padx=20, pady=10)
        
        add_conversation_button = ctk.CTkButton(self, text="Create conversation", command=lambda: self.add_conversation(controller, conversation_title_entry.get(), message_content_entry.get("1.0", "end-1c"), radio_var.get()))
        add_conversation_button.pack(pady=10)
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: controller.show_page(HomePage_Connected))
        go_back_button.pack(pady=10)
    
    def add_conversation(self, controller, conversation_title, message_content, restriction_status):
        current_date = datetime.datetime.now()
        creation_date = f"{current_date.day}/{current_date.month}/{current_date.year} {current_date.hour}:{current_date.minute}"
        send_with_size(client_socket, handle_encryption.cipher_data(f"NEWCNV|{conversation_title}|{message_content}|{restriction_status}|{creation_date}|{user_profile.username}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "NEWCNV":
            if data[1] == "new_conversation_added":
                messagebox.showinfo("Info", "Created new conversation!")
                controller.show_page(InsideConversationGUI, title=conversation_title)
            elif data[1] == "title_issue":
                #messagebox.showinfo("Info", "Created new conversation!")
                messagebox.showwarning("Warning", "This conversation already exists")
   

class ConversationGUI(ctk.CTkFrame):
    def __init__(self, parent, controller, title, username, date):
        super().__init__(parent, height=100, fg_color="white", corner_radius=50, border_color="black", border_width=2)  # Increase border_width
        self.pack_propagate(False)
        self.pack(fill=ctk.X, padx=4, pady=2)
        self.user_button = ctk.CTkButton(self, text=username, fg_color="white", text_color="black", hover_color="cyan", command= lambda: controller.show_page(ViewProfile, profile_username=username, class_return_to=HomePage_Connected, edited_profile=False))
        self.user_button.pack(side=ctk.LEFT, padx=10)
        self.date_label = ctk.CTkLabel(self, text=date)
        self.date_label.pack(side=ctk.RIGHT, padx=10)
        ####        
        
        mute_icon_image = Image.open(fp=os.path.join("assets","mute icon 1.png"))
        self.mute_icon = ctk.CTkImage(light_image=mute_icon_image, size=(30, 30))
        self.mute_button = ctk.CTkButton(self, width=50, fg_color="white", text="", image=self.mute_icon, command=stop_speech)
        self.mute_button.pack(side=ctk.RIGHT, padx=5)
        
        speaker_icon_image = Image.open(fp=os.path.join("assets","speaker icon 1.png"))
        self.speaker_icon = ctk.CTkImage(light_image=speaker_icon_image, size=(30, 30))
        self.speech_text_button = ctk.CTkButton(self, width=50, fg_color="white", text="", image=self.speaker_icon, command=lambda: threading.Thread(target=speak_text, args=(title,)).start())
        self.speech_text_button.pack(side=ctk.RIGHT, padx=5)
        
        ####
        self.title_button = ctk.CTkButton(self, text=title, fg_color="white", text_color="black", hover_color="cyan", command= lambda: controller.show_page(InsideConversationGUI, title=title))
        self.title_button.pack(side=ctk.TOP, pady=35)
        

class HandleConversations:
    # maybe the mainscreens will get an instance of this class
    def __init__(self, frame_area, controller, amount=5, search_active=False) -> None:
        self.frame_area = frame_area
        self.controller = controller
        self.amount = amount
        if not search_active:
            self.conversations_lst: list[classes.ConversationStruct] = self.get_initial_conversations()
        self.search_conversations_lst = []
    
    def get_initial_conversations(self):
        send_with_size(client_socket, handle_encryption.cipher_data(f"FSTCNV|{self.amount}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "FSTCNV":
            if data[1] != "no_conversations":
                conversations = []
                for convdata in data[1:]:
                    conv_splt = convdata.split('_')
                    conversations.append(classes.ConversationStruct(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
        
                self.draw_conversations(conversations)
        return conversations

    def draw_conversations(self, conversations):
        for conv in conversations:
            ConversationGUI(self.frame_area, self.controller, conv.title, conv.creator_username, conv.creation_date)
    
    def request_more(self):
        send_with_size(client_socket, handle_encryption.cipher_data(f"MORCNV|{self.amount}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "MORCNV":
            if data[1] != "no_conversations":
                conversations = []
                for convdata in data[1:]:
                    conv_splt = convdata.split('_')
                    self.conversations_lst.append(classes.ConversationStruct(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
                    conversations.append(classes.ConversationStruct(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
                self.draw_conversations(conversations)
    
    def reconfigure_conversation_order(self, order_by):
        #self.conversations_lst
        if order_by == "Sort Alphabetically":
            self.conversations_lst = sorted(self.conversations_lst, key=lambda conv: conv.title)
        elif order_by == "Sort Alphabetically (Reverse)":
            self.conversations_lst = sorted(self.conversations_lst, key=lambda conv: conv.title, reverse=True)
        elif order_by == "Sort Chronologically":
            self.conversations_lst = sorted(self.conversations_lst, key=self.sort_by_creation_date)
        elif order_by == "Sort Chronologically (Reverse)":
            self.conversations_lst = sorted(self.conversations_lst, key=self.sort_by_creation_date, reverse=True)
        elif order_by == "Sort By Popularity":
            pass
        elif order_by == "Sort By Popularity (Reverse)":
            pass
        
        self.draw_conversations(self.conversations_lst)
    
    def sort_by_creation_date(self, conversation):
        creation_date = datetime.datetime.strptime(conversation.creation_date, "%d/%m/%Y %H:%M")
        return creation_date
    
    def search_all(self, search_for):
        send_with_size(client_socket, handle_encryption.cipher_data(f"SRCCNV|{search_for}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "SRCCNV":
            if data[1] != "word_not_found":
                found_conversations = []
                for convdata in data[1:]:
                    conv_splt = convdata.split('_')
                    self.search_conversations_lst.append(classes.ConversationStruct(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
                    found_conversations.append(classes.ConversationStruct(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
                self.draw_conversations(found_conversations)


class InsideConversationGUI(ctk.CTkFrame):
    def __init__(self, parent, controller, title):
        global user_profile
        super().__init__(parent)
        
        # Top bar
        self.controller = controller
        self.title = title
        self.top_bar = ctk.CTkFrame(self, fg_color="purple", bg_color="purple")
        self.top_bar.pack(fill=ctk.X)
        self.title_label = ctk.CTkLabel(self.top_bar, text=f"{self.title}", fg_color="purple", bg_color="purple", text_color="white")
        self.title_label.pack(padx=12, pady=1.25)

        # Sidebar with topics
        self.sidebar = ctk.CTkFrame(self, bg_color="purple", fg_color="purple")
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
        
        self.go_back_button = ctk.CTkButton(self.sidebar, fg_color="white", text_color="black", hover_color="cyan", width=100, text="Return to Home page", command=self.go_back_smoothly)
        self.go_back_button.pack(side=ctk.TOP, padx=1.25, pady=1.25)
        
        
        self.bottom_bar = ctk.CTkFrame(self, fg_color="white", height=100)
        self.bottom_bar.pack_propagate(False)
        self.bottom_bar.pack(side=ctk.BOTTOM, fill=ctk.X)

        self.message_content_entry = ctk.CTkTextbox(self.bottom_bar, width=520, border_color="black", border_width=2)
        self.message_content_entry.pack(padx=5, pady=2, side=ctk.LEFT)
        
        self.post_message_button = ctk.CTkButton(self.bottom_bar, fg_color="white", border_color="black", border_width=2, text_color="black", hover_color="cyan", text="Post", command=lambda: self.post_message(self.message_content_entry.get("1.0", "end-1c")))
        self.post_message_button.pack(padx=5, pady=2, side=ctk.RIGHT, fill=ctk.Y)
        # Add messages here
        # Main content area with messages
        self.content_area = ctk.CTkScrollableFrame(self)
        self.content_area.pack(fill=ctk.BOTH, expand=True)
        
        self.messages_handler = HandleMessages(self.content_area, controller, title, 5)
        
        self.check_continuously = ctk.BooleanVar(master=self, value=True)
        self.job = self.after(3000, self.repeat_request)
    
    def repeat_request(self):
        # basiclly continuing the interval from the start in an "endless" loop
        if self.check_continuously.get():
            self.messages_handler.request_more()
            self.job = self.after(3000, self.repeat_request)
    
    def go_back_smoothly(self):
        self.check_continuously.set(value=False)
        self.after_cancel(self.job)
        self.controller.show_page(HomePage_Connected)
    
    def post_message(self, message_content):
        current_date = datetime.datetime.now()
        creation_date = f"{current_date.day}/{current_date.month}/{current_date.year} {current_date.hour}:{current_date.minute}"
        
        self.message_content_entry.delete("1.0","end")
        
        send_with_size(client_socket, handle_encryption.cipher_data(f"NEWMSG|{message_content}|{creation_date}|{user_profile.username}|{self.title}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "NEWMSG":
            if data[1] == "new_message_added":

                messagebox.showinfo("Info", "added new message")        




class HandleMessages:
    # maybe the mainscreens will get an instance of this class
    def __init__(self, frame_area, controller, conversation_title, amount=5) -> None:
        self.frame_area = frame_area
        self.controller = controller
        self.conversation_title = conversation_title
        self.amount = amount
        self.messages_lst = self.get_initial_messages()

    
    def get_initial_messages(self):
        send_with_size(client_socket, handle_encryption.cipher_data(f"FSTMSG|{self.amount}|{self.conversation_title}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "FSTMSG":
            if data[1] != "no_messages":
                messages = []
                for msgdata in data[1:]:
                    msg_splt = msgdata.split('_')
                    messages.append(classes.MessageStruct(msg_splt[0], msg_splt[1], msg_splt[2], msg_splt[3]))
        
        self.draw_messages(messages)
        return messages

    def draw_messages(self, messages: list[classes.MessageStruct]):
        for msg in messages:
            MessageGUI(self.frame_area, self.controller, msg.content, msg.date_published, msg.sender_username)
    
    def request_more(self):
        send_with_size(client_socket, handle_encryption.cipher_data(f"MORMSG|{self.amount}|{self.conversation_title}|{self.messages_lst[-1].content}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "MORMSG":
            if data[1] != "no_messages":
                messages = []
                for msgdata in data[1:]:
                    msg_splt = msgdata.split('_')
                    self.messages_lst.append(classes.MessageStruct(msg_splt[0], msg_splt[1], msg_splt[2], msg_splt[3]))
                    messages.append(classes.MessageStruct(msg_splt[0], msg_splt[1], msg_splt[2], msg_splt[3]))
                self.draw_messages(messages)
                #self.messages_lst.append(messages)   


class MessageGUI(ctk.CTkFrame):
    def __init__(self, parent, controller, content, date, username):
        super().__init__(parent, height=100, fg_color="white", corner_radius=50, border_color="black", border_width=2)  # Increase border_width
        self.pack_propagate(False)
        self.pack(fill=ctk.X, padx=4, pady=2)
        #self.user_label = ctk.CTkLabel(self, text=username)
        #self.user_label.pack(side=ctk.LEFT, padx=10)
        self.user_button = ctk.CTkButton(self, text=username, fg_color="white", text_color="black", hover_color="cyan", command= lambda: controller.show_page(ViewProfile, profile_username=username, class_return_to=InsideConversationGUI, edited_profile=False))
        self.user_button.pack(side=ctk.LEFT, padx=10)
        self.date_label = ctk.CTkLabel(self, text=date)
        self.date_label.pack(side=ctk.RIGHT, padx=10)
        ####
        mute_icon_image = Image.open(fp=os.path.join("assets","mute icon 1.png"))
        self.mute_icon = ctk.CTkImage(light_image=mute_icon_image, size=(30, 30))
        self.mute_button = ctk.CTkButton(self, width=50, fg_color="white", text="", image=self.mute_icon, command=stop_speech)
        self.mute_button.pack(side=ctk.RIGHT, padx=5)
        
        speaker_icon_image = Image.open(fp=os.path.join("assets","speaker icon 1.png"))
        self.speaker_icon = ctk.CTkImage(light_image=speaker_icon_image, size=(30, 30))
        self.speech_text_button = ctk.CTkButton(self, width=50, fg_color="white", text="", image=self.speaker_icon, command=lambda: threading.Thread(target=speak_text, args=(content,)).start())
        self.speech_text_button.pack(side=ctk.RIGHT, padx=5)
        ####
        self.content_label = ctk.CTkLabel(self, text=content)
        self.content_label.pack(side=ctk.TOP, pady=35)


if __name__ == "__main__":
    # perhaps I should have a global: connected_status and maybe in_conversation to know where to return to after reading user's data.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    user_profile = None
    handle_encryption = EncryptionHandler(client_socket)
    #get_conversations_thread = threading.Thread(target=get_conversations)
    app = App()
    app.mainloop()
