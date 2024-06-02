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
        
        ## not sure about this change, but it fixes a bug of exiting and returning to the same conversation
        #if class_to_show == InsideConversationGUI:
        #    self.frame = class_to_show(self.container, self, kwargs.pop("title"))
        #    self.frame.grid(row=0, column=0, sticky="nsew")
        #    return
        
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
            elif "title" in kwargs and "class_return_to" in kwargs:
                title = kwargs.pop("title")
                class_return_to = kwargs.pop("class_return_to")
                # if the value is new then it is a different conversation. Rreset the value for this class and grid it
                if title != self.saved_frames[class_to_show].title or class_return_to != self.saved_frames[class_to_show].class_return_to:
                    self.frame = class_to_show(self.container, self, title, class_return_to)
                    self.saved_frames[class_to_show] = self.frame
                    self.frame.grid(row=0, column=0, sticky="nsew")
                    return
            
            #elif "str_to_search" in kwargs:
            #    str_to_search = kwargs.pop("str_to_search")
            #    if str_to_search != self.saved_frames[class_to_show].str_to_search:
            #        self.frame = class_to_show(self.container, self, str_to_search)
            #        self.saved_frames[class_to_show] = self.frame
            #        self.frame.grid(row=0, column=0, sticky="nsew")
            #        return
            
            # if no kwargs are given or if their values are the same then user tkraise to switch frames
            self.frame = self.saved_frames[class_to_show]
            self.frame.tkraise()
            if class_to_show == InsideConversationGUI:
                self.frame.check_continuously.set(value=True)
                self.frame.repeat_request()
            #elif class_to_show == HomePage_Connected:
            #    self.frame.reload_screen()
        else:
            # if it is a totally new class then create an instance of it and grid it
            if "profile_username" in kwargs and "class_return_to" in kwargs and "edited_profile" in kwargs:
                self.frame = class_to_show(self.container, self, kwargs.pop("profile_username"), kwargs.pop("class_return_to"), kwargs.pop("edited_profile"))
            elif "title" in kwargs and "class_return_to" in kwargs:
                self.frame = class_to_show(self.container, self, kwargs.pop("title"), kwargs.pop("class_return_to"))
            elif "str_to_search" in kwargs:
                self.frame = class_to_show(self.container, self, kwargs.pop("str_to_search"))
            else:
                self.frame = class_to_show(self.container, self)
            
            if class_to_show != SearchPage:
                self.saved_frames[class_to_show] = self.frame
            self.frame.grid(row=0, column=0, sticky="nsew")
    
    def change_pinned(self, conversation_title, **kwargs):
        if "how_to_change" in kwargs:
            how_to_change = kwargs.pop("how_to_change")
        if "class_return_to" in kwargs:
            class_return_to = kwargs.pop("class_return_to")
        
        if how_to_change == "add":
            self.saved_frames[HomePage_Connected].add_pinned_conversation(conversation_title)
            if class_return_to == SearchPage:
                # make sure the gui changes in the homepage as well (the pin number and the color of the button in that conversation)
                self.saved_frames[HomePage_Connected].conversation_handler.convgui_dict[conversation_title].change_pin_manually("pin")
        elif how_to_change == "remove":
            self.saved_frames[HomePage_Connected].remove_pinned_conversation(conversation_title)
            if class_return_to == SearchPage:
                # make sure the gui changes in the homepage as well (the pin number and the color of the button in that conversation)
                self.saved_frames[HomePage_Connected].conversation_handler.convgui_dict[conversation_title].change_pin_manually("unpin")
        

#class OpeningScreen(ctk.CTkFrame):
#    def __init__(self, parent, controller):
#        super().__init__(parent)
#        # Top bar with logo, search bar, and login/register buttons
#        self.top_bar = ctk.CTkFrame(self, fg_color="purple", bg_color="purple")
#        self.top_bar.pack(fill=ctk.X)
#        self.logo = ctk.CTkLabel(self.top_bar, text="ThreadVortex", fg_color="purple", bg_color="purple", text_color="white")
#        self.logo.pack(padx=12, pady=1.25)
#        
#        
#        self.choosing_area = ctk.CTkFrame(self, fg_color="#D391FA")
#        self.choosing_area.pack(fill=ctk.BOTH, expand=True)
#        
#        self.login_button = ctk.CTkButton(self.choosing_area, width=300, height=250, text="Login", fg_color="white", text_color="black", hover_color="cyan", command=lambda: controller.show_page(LoginPage))
#        self.login_button.pack(padx=1.25, pady=1.25)
#        self.register_button = ctk.CTkButton(self.choosing_area, width=300, height=250, text="Register", fg_color="white", text_color="black", hover_color="cyan", command=lambda: controller.show_page(RegisterPage))
#        self.register_button.pack(padx=1.25, pady=1.25)


class OpeningScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Top Frame
        self.top_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.top_frame.pack(side=ctk.TOP, fill=ctk.X, expand=True, padx=20, pady=20)

        # Logo
        logo_icon_image = Image.open(os.path.join("assets","Thread Vortex logo.png"))  # Replace with your logo path
        self.logo_icon = ctk.CTkImage(light_image=logo_icon_image, size=(400, 246))
        logo_label = ctk.CTkLabel(self.top_frame, image=self.logo_icon, text="")
        logo_label.pack(pady=5)

        self.credits_label = ctk.CTkLabel(self.top_frame, text="Created by Idan Barkin", font=("Roboto", 40))
        self.credits_label.pack(pady=5)
       
        # Left Frame
        self.left_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Right Frame
        self.right_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Chat icon
        chat_icon_image = Image.open(os.path.join("assets","conversation icon 2.png"))  # Replace with your icon path
        self.chat_icon = ctk.CTkImage(light_image=chat_icon_image, size=(100, 100))
        self.chat_label = ctk.CTkLabel(self.left_frame, image=self.chat_icon, text="")
        self.chat_label.pack(pady=20)

        self.login_button = ctk.CTkButton(self.left_frame, text="Log-in", command=lambda: controller.show_page(LoginPage), width=120, height=32, font=("Roboto", 14))
        self.login_button.pack(pady=10)

        new_icon_image = Image.open(os.path.join("assets","new icon 2.png"))  # Replace with your icon path
        self.new_icon = ctk.CTkImage(light_image=new_icon_image, size=(100, 100))
        self.new_label = ctk.CTkLabel(self.right_frame, image=self.new_icon, text="")
        self.new_label.pack(pady=20)

        self.register_button = ctk.CTkButton(self.right_frame, text="Register", command=lambda: controller.show_page(RegisterPage), width=120, height=32, font=("Roboto", 14))
        self.register_button.pack(pady=10)


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
        date_creation = f"{current_date.day}/{current_date.month}/{current_date.year} {str(current_date.hour).zfill(2)}:{str(current_date.minute).zfill(2)}"
        
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
        
        self.controller = controller
                
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
        self.reconfiguration_combobox = ctk.CTkOptionMenu(master=self.configuration_frame,
                                       values=["", "Sort Alphabetically", "Sort Alphabetically (Reverse)", "Sort Chronologically", "Sort Chronologically (Reverse)", "Sort By Popularity", "Sort By Popularity (Reverse)"],
                                       command=self.reconfigure_conversations_screen,
                                       variable=optionmenu_var)
        self.reconfiguration_combobox.pack(side=ctk.TOP, padx=1.25, pady=1.25)
        
        
        # choose favorite conversations
        self.setup_favourites()
        
        
        self.topics = ["Gaming", "Cyber", "Tech", "Fashion", "Sports", "History", "Politics", "Physics"]
        for topic in self.topics:
            ctk.CTkButton(self.sidebar, text=topic, fg_color="white", text_color="black", hover_color="cyan", width=100).pack(pady=2)

        # Add messages here
        # Main content area with messages
        self.content_area = ModifiedCTkScrollableFrame(self)
        self.content_area.pack(fill=ctk.BOTH, expand=True)
        
        self.conversation_handler = HandleConversations(self.content_area, controller, HomePage_Connected, 5)
        
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
    
    def enter_pinned_conversation(self, choice):
        if choice != "":
            self.controller.show_page(InsideConversationGUI, title=choice, class_return_to=HomePage_Connected)
    
    def setup_favourites(self):
        #self.pinned_conversations = []
        self.pinned_frame = ctk.CTkFrame(self.sidebar, fg_color="white")
        self.pinned_frame.pack()
        self.pinned_convs_titles = [""]
        # GUVCNV get user pinned conversations
        send_with_size(client_socket, handle_encryption.cipher_data(f"GUPCNV|{user_profile.username}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "GUPCNV":
            if data[1] != "no_pins":
                for convtitle in data[1:]:
                    self.pinned_convs_titles.append(convtitle)
    
        optionmenu_var = ctk.StringVar(value="")  # set initial value
        self.pinned_combobox = ctk.CTkOptionMenu(master=self.pinned_frame,
                                       values=self.pinned_convs_titles,
                                       command=self.enter_pinned_conversation,
                                       variable=optionmenu_var)
        self.pinned_combobox.pack(side=ctk.TOP, padx=1.25, pady=1.25)
    
    def add_pinned_conversation(self, conversation_title):
        self.pinned_convs_titles.append(conversation_title)
        self.pinned_combobox.configure(values=self.pinned_convs_titles)
    
    def remove_pinned_conversation(self, conversation_title):
        # in the future when conversations can be deleted I will get ValueError here.
        self.pinned_convs_titles.remove(conversation_title)
        self.pinned_combobox.configure(values=self.pinned_convs_titles)
    
    #def reload_screen(self):
    #    clear_frame(self.content_area)
    #    self.conversation_handler.reload_conversations()
    
def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


class SearchPage(ctk.CTkFrame):
    def __init__(self, parent, controller, str_to_search):
            global last_search
            super().__init__(parent)
            
            last_search = str_to_search
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
            
            self.conversation_handler = HandleConversations(self.content_area, controller, SearchPage, 5, True)
            self.conversation_handler.search_all(str_to_search)
    
    def search_again(self, to_search):
        global last_search
        clear_frame(self.content_area)
        last_search = to_search
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
        self.controller = controller
        
        if profile_username == user_profile.username:
            user_data: classes.User = classes.User.clone(user_profile)
        else:
            # i will deal with this later. in this case a will ask the server for the data of the user who has this username, the sever will take it from the database - send to client and it will be displayed.
            user_data = self.get_other_user_data()
            if user_data == "no_user":
                messagebox.showwarning("Warning", "No such user exists in the database")
                self.go_back_h()
        
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
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: self.go_back_h())
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
    
    def go_back_h(self):
        if self.class_return_to == SearchPage:
            self.controller.show_page(self.class_return_to, str_to_search=last_search) 
        else:
            self.controller.show_page(self.class_return_to) 

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
        creation_date = f"{current_date.day}/{current_date.month}/{current_date.year} {str(current_date.hour).zfill(2)}:{str(current_date.minute).zfill(2)}"
        send_with_size(client_socket, handle_encryption.cipher_data(f"NEWCNV|{conversation_title}|{message_content}|{restriction_status}|{creation_date}|{user_profile.username}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "NEWCNV":
            if data[1] == "new_conversation_added":
                messagebox.showinfo("Info", "Created new conversation!")
                controller.show_page(InsideConversationGUI, title=conversation_title, class_return_to=HomePage_Connected)
            elif data[1] == "title_issue":
                #messagebox.showinfo("Info", "Created new conversation!")
                messagebox.showwarning("Warning", "This conversation already exists")
   

class ConversationGUI(ctk.CTkFrame):
    def __init__(self, parent, controller, title, username, date, restrictions, class_return_to):
        super().__init__(parent, height=100, fg_color="white", corner_radius=50, border_color="black", border_width=2)  # Increase border_width
        self.pack_propagate(False)
        self.pack(fill=ctk.X, padx=4, pady=2)
        
        self.controller = controller
        self.title = title
        self.restrictions = restrictions
        self.class_return_to = class_return_to
        
        self.user_button = ctk.CTkButton(self, text=username, fg_color="white", text_color="black", hover_color="cyan", command= lambda: controller.show_page(ViewProfile, profile_username=username, class_return_to=class_return_to, edited_profile=False))
        self.user_button.pack(side=ctk.LEFT, padx=10)
        self.date_label = ctk.CTkLabel(self, text=date)
        self.date_label.pack(side=ctk.RIGHT, padx=10)
        
        self.set_pinning()
        
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
        self.title_button = ctk.CTkButton(self, text=title, fg_color="white", text_color="black", hover_color="cyan", command= self.enter_conversation)
        self.title_button.pack(side=ctk.TOP, pady=35)
        
    
    def enter_conversation(self):
        # first we must check the restrictions.
        if self.restrictions == "18+":
            if user_profile.age == "" or int(user_profile.age) < 18:
                messagebox.showwarning("Warning", "Conversation with restricted access - 18+ only")
                return
        self.controller.show_page(InsideConversationGUI, title=self.title, class_return_to=self.class_return_to)
    
    def set_pinning(self):
        # get buttons state (has user already pinned here?), and the current number of pins on this conversation
        send_with_size(client_socket, handle_encryption.cipher_data(f"GEPCNV|{user_profile.username}|{self.title}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "GEPCNV":
            self.pins = data[2]
            self.current_pin_status = data[1]
            
            pin_image = Image.open(fp=os.path.join("assets","pin icon 2.png"))
            self.pin_icon = ctk.CTkImage(light_image=pin_image, size=(30, 30))
            self.pin_button = ctk.CTkButton(self, width=50, text="", image=self.pin_icon, command=self.pin_action)
            self.pin_button.pack(side=ctk.RIGHT, padx=10)
            
            self.pins_label = ctk.CTkLabel(self, text=self.pins)
            self.pins_label.pack(side=ctk.RIGHT, padx=10)
            
            #downvote_icon_image = Image.open(fp=os.path.join("assets","downvote icon 1.png"))
            #self.downvote_icon = ctk.CTkImage(light_image=downvote_icon_image, size=(30, 30))
            #self.downvote_button = ctk.CTkButton(self, width=50, text="", image=self.downvote_icon, command=self.downvote_action)
            #self.downvote_button.pack(side=ctk.RIGHT, padx=10)
            
            if self.current_pin_status == "pinned":
                self.pin_button.configure(fg_color="#FFD700", hover_color="#FFD300")
            #elif self.current_vote == "downvote":
            #    self.downvote_button.configure(fg_color="#ED2939", hover_color="#E60026")


    def pin_action(self):
        if self.current_pin_status == "pinned":
            # reset the color
            self.pin_button.configure(fg_color="#3B8ED0", hover_color="#36719F")
        else:
            # change to yellow
            self.pin_button.configure(fg_color="#FFD700", hover_color="#FFD300")
        
        send_with_size(client_socket, handle_encryption.cipher_data(f"PINCNV|{user_profile.username}|{self.title}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "PINCNV":
            self.pins = data[2]
            self.pins_label.configure(text=self.pins)
            if data[1] == "pinned":
                self.current_pin_status = "pinned"
                
                self.controller.change_pinned(self.title, how_to_change="add", class_return_to=self.class_return_to)
                #self.controller.add_pinned_conversation(self.title, )
            elif data[1] == "no_pin":
                self.current_pin_status = "no_pin"
                
                self.controller.change_pinned(self.title, how_to_change="remove", class_return_to=self.class_return_to)
                #self.controllerremove_pinned_conversation(self.title)
    
    def change_pin_manually(self, pin_status):
        if pin_status == "pin":
            self.current_pin_status = "pinned"
            self.pins = str(int(self.pins)+1)
            self.pin_button.configure(fg_color="#FFD700", hover_color="#FFD300")
            self.pins_label.configure(text=self.pins)
        elif pin_status == "unpin":
            self.current_pin_status = "no_pin"
            self.pins = str(int(self.pins)-1)
            self.pin_button.configure(fg_color="#3B8ED0", hover_color="#36719F")
            self.pins_label.configure(text=self.pins)

            
        
    

class HandleConversations:
    # maybe the mainscreens will get an instance of this class
    def __init__(self, frame_area, controller, class_return_to, amount=5, search_active=False) -> None:
        self.frame_area = frame_area
        self.controller = controller
        self.amount = amount
        self.class_return_to = class_return_to
        self.search_active = search_active
        if not self.search_active:
            self.convgui_dict = {}
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
            convgui = ConversationGUI(self.frame_area, self.controller, conv.title, conv.creator_username, conv.creation_date, conv.restrictions, self.class_return_to)
            if not self.search_active:
                self.convgui_dict[conv.title] = convgui
            
    
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
    
    #def reload_conversations(self):
    #    self.draw_conversations(self.conversations_lst)


class InsideConversationGUI(ctk.CTkFrame):
    def __init__(self, parent, controller, title, class_return_to):
        global user_profile
        super().__init__(parent)
        self.class_return_to = class_return_to
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
        if self.class_return_to == SearchPage:
            self.controller.show_page(self.class_return_to, str_to_search=last_search)
        else:
            self.controller.show_page(self.class_return_to)
    
    def post_message(self, message_content):
        current_date = datetime.datetime.now()
        creation_date = f"{current_date.day}/{current_date.month}/{current_date.year} {str(current_date.hour).zfill(2)}:{str(current_date.minute).zfill(2)}"
        
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
            messages = []
            if data[1] != "no_messages":
                
                for msgdata in data[1:]:
                    msg_splt = msgdata.split('_')
                    messages.append(classes.MessageStruct(msg_splt[1], msg_splt[2], msg_splt[3], msg_splt[4], msg_splt[0]))
        
                self.draw_messages(messages)
        return messages

    def draw_messages(self, messages: list[classes.MessageStruct]):
        for msg in messages:
            MessageGUI(self.frame_area, self.controller, msg.content, msg.date_published, msg.sender_username, msg.conversation_title, str(msg.id))
    
    def request_more(self):
        # {self.messages_lst[-1] won't cause out of range error beacause when creating a conversation the client will write the first message in that conversation
        send_with_size(client_socket, handle_encryption.cipher_data(f"MORMSG|{self.amount}|{self.conversation_title}|{self.messages_lst[-1].id}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "MORMSG":
            if data[1] != "no_messages":
                messages = []
                for msgdata in data[1:]:
                    msg_splt = msgdata.split('_')
                    self.messages_lst.append(classes.MessageStruct(msg_splt[1], msg_splt[2], msg_splt[3], msg_splt[4], msg_splt[0]))
                    messages.append(classes.MessageStruct(msg_splt[1], msg_splt[2], msg_splt[3], msg_splt[4], msg_splt[0]))
                self.draw_messages(messages)
                #self.messages_lst.append(messages)   


class MessageGUI(ctk.CTkFrame):
    def __init__(self, parent, controller, content, date, username, conversation_title, id):
        super().__init__(parent, height=100, fg_color="white", corner_radius=50, border_color="black", border_width=2)  # Increase border_width
        self.pack_propagate(False)
        self.pack(fill=ctk.X, padx=4, pady=2)
        
        self.id = id
        
        #self.user_label = ctk.CTkLabel(self, text=username)
        #self.user_label.pack(side=ctk.LEFT, padx=10)
        self.user_button = ctk.CTkButton(self, text=username, fg_color="white", text_color="black", hover_color="cyan", command= lambda: controller.show_page(ViewProfile, profile_username=username, class_return_to=InsideConversationGUI, edited_profile=False))
        self.user_button.pack(side=ctk.LEFT, padx=10)
        
        self.date_label = ctk.CTkLabel(self, text=date)
        self.date_label.pack(side=ctk.RIGHT, padx=10)
        ####
        
        self.set_voting()
        
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
        #self.content_label = ctk.CTkTextbox(self)
        #self.content_label.insert("1.0", content)
        #self.content_label.configure(state=ctk.DISABLED)
        #self.content_label.pack(side=ctk.TOP, pady=35)
    
    def set_voting(self):
        # get buttons state (has user already votes here?), and the current number of votes on this message
        send_with_size(client_socket, handle_encryption.cipher_data(f"GEVMSG|{user_profile.username}|{self.id}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "GEVMSG":
            self.votes = data[2]
            self.current_vote = data[1]
            
            upvote_image = Image.open(fp=os.path.join("assets","upvote icon 1.png"))
            self.upvote_icon = ctk.CTkImage(light_image=upvote_image, size=(30, 30))
            self.upvote_button = ctk.CTkButton(self, width=50, text="", image=self.upvote_icon, command=self.upvote_action)
            self.upvote_button.pack(side=ctk.RIGHT, padx=10)
            
            self.votes_label = ctk.CTkLabel(self, text=self.votes)
            self.votes_label.pack(side=ctk.RIGHT, padx=10)
            
            downvote_icon_image = Image.open(fp=os.path.join("assets","downvote icon 1.png"))
            self.downvote_icon = ctk.CTkImage(light_image=downvote_icon_image, size=(30, 30))
            self.downvote_button = ctk.CTkButton(self, width=50, text="", image=self.downvote_icon, command=self.downvote_action)
            self.downvote_button.pack(side=ctk.RIGHT, padx=10)
            
            if self.current_vote == "upvote":
                self.upvote_button.configure(fg_color="#66FF00", hover_color="#32CD32")
            elif self.current_vote == "downvote":
                self.downvote_button.configure(fg_color="#ED2939", hover_color="#E60026")


    def upvote_action(self):
        if self.current_vote == "upvote":
            # reset the color
            self.upvote_button.configure(fg_color="#3B8ED0", hover_color="#36719F")
        elif self.current_vote == "downvote":
            # reset the color
            self.downvote_button.configure(fg_color="#3B8ED0", hover_color="#36719F")
            # change to green
            self.upvote_button.configure(fg_color="#66FF00", hover_color="#32CD32")
        else:
            # change to green
            self.upvote_button.configure(fg_color="#66FF00", hover_color="#32CD32")
        
        send_with_size(client_socket, handle_encryption.cipher_data(f"VOTMSG|upvote|{user_profile.username}|{self.id}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "VOTMSG":
            self.votes = data[2]
            self.votes_label.configure(text=self.votes)
            if data[1] == "upvote":
                self.current_vote = "upvote"
            elif data[1] == "downvote":
                self.current_vote = "downvote"
            elif data[1] == "no_vote":
                self.current_vote = "no_vote"
    
    def downvote_action(self):
        if self.current_vote == "upvote":
            # reset the color
            self.upvote_button.configure(fg_color="#3B8ED0", hover_color="#36719F")
            # change to red
            self.downvote_button.configure(fg_color="#ED2939", hover_color="#E60026")
        elif self.current_vote == "downvote":
            # reset the color
            self.downvote_button.configure(fg_color="#3B8ED0", hover_color="#36719F")
        else:
            # chage to red
            self.downvote_button.configure(fg_color="#ED2939", hover_color="#E60026")
            
        send_with_size(client_socket, handle_encryption.cipher_data(f"VOTMSG|downvote|{user_profile.username}|{self.id}"))
        data = handle_encryption.decipher_data(recv_by_size(client_socket)).split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "VOTMSG":
            self.votes = data[2]
            self.votes_label.configure(text=self.votes)
            if data[1] == "upvote":
                self.current_vote = "upvote"
            elif data[1] == "downvote":
                self.current_vote = "downvote"
            elif data[1] == "no_vote":
                self.current_vote = "no_vote"
                #messagebox.showinfo("Info", "added new message")  


class FailedToload(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Thread Vortex")
        self.geometry("800x600")
        self.iconpath = ImageTk.PhotoImage(file=os.path.join("assets","Thread Vortex no text logo.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        # Top Frame
        self.top_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.top_frame.pack(side=ctk.TOP, fill=ctk.X, expand=True, padx=20, pady=10)

        # Logo
        logo_icon_image = Image.open(os.path.join("assets","Thread Vortex logo.png"))  # Replace with your logo path
        self.logo_icon = ctk.CTkImage(light_image=logo_icon_image, size=(400, 246))
        self.logo_label = ctk.CTkLabel(self.top_frame, image=self.logo_icon, text="")
        self.logo_label.pack(pady=5)

        credits_label = ctk.CTkLabel(self.top_frame, text="Created by Idan Barkin", font=("Roboto", 40))
        credits_label.pack(pady=5)
        # Left Frame
        self.center_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.center_frame.pack(side=ctk.BOTTOM, fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Chat icon
        failed_icon_image = Image.open(os.path.join("assets","failed icon 1.png"))  # Replace with your icon path
        self.failed_icon = ctk.CTkImage(light_image=failed_icon_image, size=(100, 100))
        self.failed_icon_label = ctk.CTkLabel(self.center_frame, image=self.failed_icon, text="")
        self.failed_icon_label.pack(pady=5)
        
        self.failed_label = ctk.CTkLabel(self.center_frame, text="Server currently offline.\nTry connecting again later.", font=("Roboto", 40))
        self.failed_label.pack(pady=5)


if __name__ == "__main__":
    # perhaps I should have a global: connected_status and maybe in_conversation to know where to return to after reading user's data.
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', 12345))
            user_profile = None
            handle_encryption = EncryptionHandler(client_socket)
            #get_conversations_thread = threading.Thread(target=get_conversations)
            app = App()
            app.mainloop()
    except ConnectionRefusedError:
        print("Connection refused")
        failed_load_app = FailedToload()
        failed_load_app.mainloop()
        
    # doesn't work. need to figure out a way to show client ht failed load screen if the server disconnects
    #except ConnectionResetError:
    #    print("Connection reset")
    #    app.destroy()
    #    failed_load_app = FailedToload()
    #    failed_load_app.mainloop()
