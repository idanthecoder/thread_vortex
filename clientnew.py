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
        self.frame = OpeningScreen(self.container, self)
        self.frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, cont, **kwargs): # possible kwargs currently are: profile_username=user_profile.username, connected_status="connected"
        #frame = self.frames[cont]
        #frame.tkraise()
        
        # use forget on the current used class frame and grid the new class frame i want to use
        self.frame.forget()
        if "profile_username" in kwargs:
                self.frame = cont(self.container, self, kwargs.pop("profile_username"))
        else:
            self.frame = cont(self.container, self)
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
        
        go_back_button = ctk.CTkButton(self, text="Return to opening screen", command=lambda: controller.show_page(OpeningScreen))
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
        
        # view profile button
        view_profile_icon_image = Image.open(fp=os.path.join("assets","default user icon 2.png"))
        self.view_profile_icon = ctk.CTkImage(light_image=view_profile_icon_image, size=(40, 40))
        self.view_profile_button = ctk.CTkButton(self.top_bar, width=100, text="", image=self.view_profile_icon, command=lambda: controller.show_page(ViewProfile, profile_username=user_profile.username, connected_status="connected"))
        self.view_profile_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)

        # Sidebar with topics
        self.sidebar = ctk.CTkFrame(self, bg_color="purple", fg_color="purple")
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
        
        # new conversation button
        new_conversation_icon_image = Image.open(fp=os.path.join("assets","plus icon 3.png"))
        self.new_conversation_icon = ctk.CTkImage(light_image=new_conversation_icon_image, size=(40, 40))
        self.new_conversation_button = ctk.CTkButton(self.sidebar, fg_color="white", width=100, text="", image=self.new_conversation_icon, command=lambda: controller.show_page(CreateNewConversation))
        self.new_conversation_button.pack(side=ctk.TOP, padx=1.25, pady=1.25)
        
        self.topics = ["Gaming", "Cyber", "Tech", "Fashion", "Sports", "History", "Politics", "Physics"]
        for topic in self.topics:
            ctk.CTkButton(self.sidebar, text=topic, fg_color="white", text_color="black", hover_color="cyan", width=100).pack(pady=2)

        # Add messages here
        # Main content area with messages
        self.content_area = ctk.CTkScrollableFrame(self)
        self.content_area.pack(fill=ctk.BOTH, expand=True)
        
        self.conversation_handler = HandleConversations(self.content_area, 5)
        
        #request_conversations(5, self.content_area)
        #
        self.request_conversations_button = ctk.CTkButton(self.content_area, text="More Conversations", fg_color="white",  border_color="black", border_width=2, text_color="black", hover_color="cyan", command=lambda: self.conversation_handler.request_more(self.content_area, 5))
        self.request_conversations_button.pack()
        
        #self.messages = [
        #    {"user": "User1", "date": "22.2.24", "content": "What does the 'yield' keyword do in Python?"},
        #    {"user": "User2", "date": "20.2.24", "content": "🤔 IF YOU MAKE THE UNIVERSE A BETTER PLACE..."},
        #    # Add more messages here...
        #]
        #for message in self.messages:
        #    Message(self.content_area, message["user"], message["date"], message["content"])
    
    def disconnect(self, controller):
        if messagebox.askokcancel("Warning", "You are about to disconnect from the program."):
            controller.show_page(OpeningScreen)


#def request_conversations(amount,  frame_area):
#    send_with_size(client_socket, f"GETCNV|{amount}")
#    data = recv_by_size(client_socket).decode().split('|')
#    if len(data) <= 1:
#        return
#    
#    if data[0] == "GETCNV":
#        if data[1] != "no_conversations":
#            conversations = []
#            for i, convdata in enumerate(data[2:]):
#                conv_splt = convdata.split(',')
#                conversations.append(classes.ConversationVServer(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
#            
#            for i, conv in enumerate(conversations):
#                ConversationGUI(frame_area, conv.title, conv.creator_username, conv.creation_date)
                
                
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
    def __init__(self, parent, controller, profile_username):
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
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: controller.show_page(HomePage_Connected))
        go_back_button.pack(pady=10)
             

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
        message_content_entry = ctk.CTkEntry(self)
        message_content_entry.pack()
        
        restriction_label = ctk.CTkLabel(self, text="Restrict access:")
        restriction_label.pack()
        radio_var = ctk.StringVar()
        restriction_radiobutton1 = ctk.CTkRadioButton(master=self, text="18+", variable= radio_var, value="18+")
        restriction_radiobutton2 = ctk.CTkRadioButton(master=self, text="Unrestricted", variable= radio_var, value="unrestricted")
        restriction_radiobutton1.pack(padx=20, pady=10)
        restriction_radiobutton2.pack(padx=20, pady=10)
        
        add_conversation_button = ctk.CTkButton(self, text="Commit changes", command=lambda: self.add_conversation(controller, conversation_title_entry.get(), message_content_entry.get(), radio_var.get()))
        add_conversation_button.pack(pady=10)
        
        go_back_button = ctk.CTkButton(self, text="Return to main screen", command=lambda: controller.show_page(HomePage_Connected))
        go_back_button.pack(pady=10)
    
    def add_conversation(self, controller, conversation_title, message_content, restriction_status):
        current_date = datetime.datetime.now()
        creation_date = f"{current_date.day}/{current_date.month}/{current_date.year} {current_date.hour}:{current_date.minute}"
        send_with_size(client_socket, f"NEWCON|{conversation_title}|{message_content}|{restriction_status}|{creation_date}|{user_profile.username}")
        data = recv_by_size(client_socket).decode().split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "NEWCON":
            if data[1] == "new_conversation_added":
                #user_profile = classes.User(data[2], None, data[3], int(data[4]), data[5], data[6], data[7], data[8], data[9])
                #controller.show_page(HomePage_Connected)
                # for now you return to main screen. later you will be in your conversation.
                messagebox.showinfo("Info", "Created new conversation!")
                controller.show_page(HomePage_Connected)
   

class ConversationGUI(ctk.CTkFrame):
    def __init__(self, parent, title, username, date):
        super().__init__(parent, height=100, fg_color="white", corner_radius=50, border_color="black", border_width=2)  # Increase border_width
        self.pack_propagate(False)
        self.pack(fill=ctk.X, padx=4, pady=2)
        self.user_label = ctk.CTkLabel(self, text=username)
        self.user_label.pack(side=ctk.LEFT, padx=10)
        self.date_label = ctk.CTkLabel(self, text=date)
        self.date_label.pack(side=ctk.RIGHT, padx=10)
        self.title_label = ctk.CTkLabel(self, text=title)
        self.title_label.pack(side=ctk.TOP, pady=35)


#def get_conversations():
#    send_with_size(client_socket, f"EDTUSR|{user_profile.username}|{password}|{user_profile.mail}|{user_profile.age}|{user_profile.gender}|{user_profile.country}|{user_profile.occupation}|{user_profile.date_creation}|{user_profile.description}")
#    data = recv_by_size(client_socket).decode().split('|')
#    if len(data) <= 1:
#        return
#    
#    if data[0] == "EDTUSR":
#        if data[1] == "edited_profile":
#            messagebox.showinfo("Info", "User profile updated successfuly")
#            controller.show_page(HomePage_Connected)

#def get_initial_conversations(amount):
#    send_with_size(client_socket, f"GETCNV|{amount}")
#    data = recv_by_size(client_socket).decode().split('|')
#    if len(data) <= 1:
#        return
#    
#    if data[0] == "GETCNV":
#        if data[1] != "no_conversations":
#            conversations = []
#            for i, convdata in enumerate(data[2:]):
#                conv_splt = convdata.split(',')
#                conversations.append(classes.ConversationVServer(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
#    return conversations


#def draw_conversation(conversations: list[classes.ConversationVServer], frame_area):
#    for i, conv in enumerate(conversations):
#        ConversationGUI(frame_area, conv.title, conv.creator_username, conv.creation_date)
        

class HandleConversations:
    # maybe the mainscreens will get an instance of this class
    def __init__(self, frame_area, amount=5) -> None:
        self.conversations_lst: list[classes.ConversationVServer] = self.get_initial_conversations(frame_area, amount)
    
    def get_initial_conversations(self, frame_area, amount=5):
        send_with_size(client_socket, f"FSTCNV|{amount}")
        data = recv_by_size(client_socket).decode().split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "FSTCNV":
            if data[1] != "no_conversations":
                conversations = []
                for convdata in data[2:]:
                    conv_splt = convdata.split(',')
                    conversations.append(classes.ConversationVServer(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
        
        self.draw_conversations(conversations, frame_area)
        return conversations

    def draw_conversations(self, conversations, frame_area):
        for conv in conversations:
            ConversationGUI(frame_area, conv.title, conv.creator_username, conv.creation_date)
    
    def request_more(self, frame_area, amount=5):
        send_with_size(client_socket, f"MORCNV|{amount}")
        data = recv_by_size(client_socket).decode().split('|')
        if len(data) <= 1:
            return
        
        if data[0] == "MORCNV":
            if data[1] != "no_conversations":
                conversations = []
                for convdata in data[2:]:
                    conv_splt = convdata.split(',')
                    self.conversations_lst.append(classes.ConversationVServer(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
                    conversations.append(classes.ConversationVServer(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
                self.draw_conversations(conversations, frame_area)
                self.conversations_lst.append(conversations) 
    

if __name__ == "__main__":
    # perhaps I should have a global: connected_status and maybe in_conversation to know where to return to after reading user's data.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    user_profile = None
    #get_conversations_thread = threading.Thread(target=get_conversations)
    app = App()
    app.mainloop()
