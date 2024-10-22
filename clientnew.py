__author__ = "Idan"

import socket
import threading
from tcp_by_size import send_with_size, recv_by_size
import email_handler
import customtkinter as ctk
import os
from PIL import ImageTk, Image
import datetime
import classes
from tkinter import messagebox
from modified_gui import ModifiedCTkScrollableFrame
from encryption_handler import EncryptionHandler
from text_to_speech_handler import speak_text, stop_speech


def fail_mechanism():
    """
    Closes the main app window and opens the failed screen.
    """
    
    app.destroy()
    failed_load_app = FailedToload()
    failed_load_app.mainloop()

def send_and_recieve(data_to_send):
    """
    Sends requests to the server and returns the response.
    If the server is disconnected show user the fail screen.

    Args:
        data_to_send (str): The user's request.

    Returns:
        list: The server's response, divided into a list in which every value is related to the user's request (in accordance to the protocol).
    """
    try:
        send_with_size(client_socket, handle_encryption.cipher_data(data_to_send))
        data = handle_encryption.decipher_data(recv_by_size(client_socket))
        if data == "":
            fail_mechanism()
        else:
            return data.split('|')
    except ConnectionResetError:
        fail_mechanism()
        
        

class App(ctk.CTk):
    """
    A class that inherits from the CTk class, and therefore behaves as a customtkinter main app window.
    This class will control the frames which the user can see, and is in a way the base of the GUI.

    Attributes:
        container (customtkinter.CTkFrame): The frame in which all the different screens will be placed.
        saved_frames (dict): A dictionary saving the state of the frames that were already shown to the user (key is the specific frame class, value is the instance of that frame class).
        frame (customtkinter.CTkFrame): The current frame (screen) that is shown to the user.
    """
    
    def __init__(self):
        """
        The constructor for App class.
        """
        
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

        # dictionary to save specific frames that should retain their status {class:frame}
        self.saved_frames = {}
        self.frame = OpeningScreen(self.container, self)
        self.saved_frames[OpeningScreen] = self.frame
        self.frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, class_to_show, **kwargs):
        """
        Switches between the frames that are shown on the screen. Some are saved so that when the user will view them again, their state will remain the same (using tkraise to show them),
        whereas others are created new everytime they are requested (using grid/pack to show them). 

        Args:
            class_to_show (class): A class that inherits from the CTkFrame class (not an instance though!), that will be shown to the user.
            **kwargs: possible kwargs currently: 
                profile_username="username" (str)
                title="title" (str)
                class_return_to=class (class)
                edited_profile=True/False (bool)
                str_to_search="str" (str)
                mail="mail" (str)
                callback=function (def)
        """
        
        # if the requested class is already saved in the dictinary I want to use it in the state it was last left in
        if class_to_show in self.saved_frames.keys():
            # if this parameter is in kwargs then this relates to the InsideConversationGUI class
            if "title" in kwargs and "class_return_to" in kwargs:
                title = kwargs.pop("title")
                class_return_to = kwargs.pop("class_return_to")
                # if the value is new then it is a different conversation. Rreset the value for this class and grid it
                if title != self.saved_frames[class_to_show].title or class_return_to != self.saved_frames[class_to_show].class_return_to:
                    self.frame = class_to_show(self.container, self, title, class_return_to)
                    self.saved_frames[class_to_show] = self.frame
                    self.frame.grid(row=0, column=0, sticky="nsew")
                    return
            
            # if no kwargs are given or if their values are the same then user tkraise to switch frames
            self.frame = self.saved_frames[class_to_show]
            self.frame.tkraise()
            if class_to_show == InsideConversationGUI:
                # inside the conversation will keep looking for new conversations this way
                self.frame.check_continuously.set(value=True)
                self.frame.repeat_request()
        else:
            # if it is a totally new class then create an instance of it and grid it
            if "profile_username" in kwargs and "class_return_to" in kwargs and "edited_profile" in kwargs:
                self.frame = class_to_show(self.container, self, kwargs.pop("profile_username"), kwargs.pop("class_return_to"), kwargs.pop("edited_profile"))
            elif "title" in kwargs and "class_return_to" in kwargs:
                self.frame = class_to_show(self.container, self, kwargs.pop("title"), kwargs.pop("class_return_to"))
            elif "str_to_search" in kwargs:
                self.frame = class_to_show(self.container, self, kwargs.pop("str_to_search"))
            elif "mail" in kwargs and "callback" in kwargs and "class_return_to":
                self.frame = class_to_show(self.container, self, kwargs.pop("mail"), kwargs.pop("callback"), kwargs.pop("class_return_to"))
            elif "mail" in kwargs:
                self.frame = class_to_show(self.container, self, kwargs.pop("mail"))
            else:
                self.frame = class_to_show(self.container, self)
            
            # frames which I wish never to save their status
            if class_to_show != SearchPage and class_to_show != EnterVerificationCode and class_to_show != ChoosePassword and class_to_show != ViewProfile:
                self.saved_frames[class_to_show] = self.frame
            self.frame.grid(row=0, column=0, sticky="nsew")
    
    def change_pinned(self, conversation_title, **kwargs):
        """
        Changes the pin state of a certain conversation (pinned/unpinned)

        Args:
            conversation_title (str): The title of the conversation that was pinned/unpinned by the user.
        """
        
        if "how_to_change" in kwargs:
            how_to_change = kwargs.pop("how_to_change")
        if "class_return_to" in kwargs:
            class_return_to = kwargs.pop("class_return_to")
        
        # this function is related to the pinned conversations combobox. when a conversation is pinned/unpinned it updates the combobox
        # additionaly if the change is done in the search frame it will make sure that the change also happends in the homepage
        
        if how_to_change == "add":
            self.saved_frames[HomePage_Connected].add_pinned_conversation(conversation_title)
            if class_return_to == SearchPage:
                # make sure the gui changes in the homepage as well (the pin number and the color of the button in that conversation)
                self.saved_frames[HomePage_Connected].conversation_handler.convgui_dict[conversation_title].change_pin_manually()
        elif how_to_change == "remove":
            self.saved_frames[HomePage_Connected].remove_pinned_conversation(conversation_title)
            if class_return_to == SearchPage:
                # make sure the gui changes in the homepage as well (the pin number and the color of the button in that conversation)
                self.saved_frames[HomePage_Connected].conversation_handler.convgui_dict[conversation_title].change_pin_manually()
    
    def reset_saved_frames(self):
        """
        When disconnecting, clear the saved_frames dictionary completely and then show the opening screen.
        """
        
        self.saved_frames.clear()
        self.frame = OpeningScreen(self.container, self)
        self.saved_frames[OpeningScreen] = self.frame
        self.frame.grid(row=0, column=0, sticky="nsew")


class OpeningScreen(ctk.CTkFrame):
    """
    A class that inherits from the CTkFrame class, and therefore behaves as a customtkinter frame.
    This class is the opening screen from which the user could connect to his profile.

    Attributes:
    
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Top Frame
        self.top_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.top_frame.pack(side=ctk.TOP, fill=ctk.X, expand=True, padx=20, pady=20)

        # Logo
        logo_icon_image = Image.open(os.path.join("assets","Thread Vortex logo.png"))
        self.logo_icon = ctk.CTkImage(light_image=logo_icon_image, size=(400, 246))
        self.logo_label = ctk.CTkLabel(self.top_frame, image=self.logo_icon, text="")
        self.logo_label.pack(pady=5)

        self.credits_label = ctk.CTkLabel(self.top_frame, text="Created by Idan Barkin", font=("Roboto", 40))
        self.credits_label.pack(pady=5)
       
        # Left Frame
        self.left_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Right Frame
        self.right_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Chat icon
        chat_icon_image = Image.open(os.path.join("assets","conversation icon 2.png"))
        self.chat_icon = ctk.CTkImage(light_image=chat_icon_image, size=(100, 100))
        self.chat_label = ctk.CTkLabel(self.left_frame, image=self.chat_icon, text="")
        self.chat_label.pack(pady=10)

        self.login_button = ctk.CTkButton(self.left_frame, text="Log-in", command=lambda: controller.show_page(LoginPage), width=120, height=32, font=("Roboto", 14))
        self.login_button.pack(pady=5)
        
        self.forgot_password_button = ctk.CTkButton(self.left_frame, text="Forgot password", command=lambda: controller.show_page(ForgotPassword), width=120, height=32, font=("Roboto", 14))
        self.forgot_password_button.pack(pady=5)
        
        new_icon_image = Image.open(os.path.join("assets","new icon 2.png")) 
        self.new_icon = ctk.CTkImage(light_image=new_icon_image, size=(100, 100))
        self.new_label = ctk.CTkLabel(self.right_frame, image=self.new_icon, text="")
        self.new_label.pack(pady=5)

        self.register_button = ctk.CTkButton(self.right_frame, text="Register", command=lambda: controller.show_page(RegisterPage), width=120, height=32, font=("Roboto", 14))
        self.register_button.pack(pady=5)


class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller

        self.bottom_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.bottom_frame.pack(side=ctk.BOTTOM, padx=10, pady=5)

        self.top_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.top_frame.pack(side=ctk.TOP, padx=10, pady=10)

        self.label = ctk.CTkLabel(self.top_frame, text="Register Page", font=("Helvetica", 32))
        self.label.pack(pady=10, padx=10)
        
        #self.line = ctk.CTkFrame(self, height=1, fg_color="black", border_color="black", border_width=1)
        #self.line.pack(fill=ctk.X, expand=True)

        # Left Frame
        self.left_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=20, pady=10)

        # Right Frame
        self.right_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=10)

        self.mandate_label = ctk.CTkLabel(self.left_frame, text="Mandatory fields:", font=("Helvetica", 26))
        self.mandate_label.pack(pady=2)

        self.name_label = ctk.CTkLabel(self.left_frame, text="Name:")
        self.name_label.pack(pady=2)
        self.name_entry = ctk.CTkEntry(self.left_frame)
        self.name_entry.pack(pady=2)

        self.password_label = ctk.CTkLabel(self.left_frame, text="Password:")
        self.password_label.pack(pady=2)
        self.password_entry = ctk.CTkEntry(self.left_frame, show="*")
        self.password_entry.pack(pady=2)

        self.email_label = ctk.CTkLabel(self.left_frame, text="Email:")
        self.email_label.pack(pady=2)
        self.email_entry = ctk.CTkEntry(self.left_frame)
        self.email_entry.pack(pady=2)
        
        self.age_label = ctk.CTkLabel(self.right_frame, text="Age:")
        self.age_label.pack(pady=2)
        self.age_entry = ctk.CTkEntry(self.right_frame)
        self.age_entry.pack(pady=2)

        self.gender_label = ctk.CTkLabel(self.right_frame, text="Gender:")
        self.gender_label.pack(pady=2)
        self.gender_entry = ctk.CTkEntry(self.right_frame)
        self.gender_entry.pack(pady=2)

        self.country_label = ctk.CTkLabel(self.right_frame, text="Country:")
        self.country_label.pack(pady=2)
        self.country_entry = ctk.CTkEntry(self.right_frame)
        self.country_entry.pack(pady=2)

        self.occupation_label = ctk.CTkLabel(self.right_frame, text="Occupation:")
        self.occupation_label.pack(pady=2)
        self.occupation_entry = ctk.CTkEntry(self.right_frame)
        self.occupation_entry.pack(pady=2)

        self.description_label = ctk.CTkLabel(self.right_frame, text="Description:")
        self.description_label.pack(pady=1)
        self.description_entry = ctk.CTkTextbox(self.right_frame, wrap="word")
        self.description_entry.pack(pady=4)

        self.register_button = ctk.CTkButton(self.bottom_frame, text="Register", command=lambda: self.user_register_h(self.name_entry.get(), self.password_entry.get(), self.email_entry.get(), self.age_entry.get(), self.gender_entry.get(), self.country_entry.get(), self.occupation_entry.get(), self.description_entry.get("1.0", "end-1c")))
        self.register_button.pack(padx=5, pady=10)
        
        self.go_back_button = ctk.CTkButton(self.bottom_frame, text="Return to opening screen", command=lambda: controller.show_page(OpeningScreen))
        self.go_back_button.pack(padx=5, pady=10)
    
    def user_register_h(self, username, password, mail, age: str, gender, country, occupation, description):
        #global user_profile
        
        current_date = datetime.datetime.now()
        date_creation = f"{current_date.day}/{current_date.month}/{current_date.year} {str(current_date.hour).zfill(2)}:{str(current_date.minute).zfill(2)}"
        
        if not age.isnumeric() and age != "":
            messagebox.showwarning("Warning", "Age must be numeric.")
            return

        if username == "[DELETED]":
                messagebox.showwarning("Warning", "[DELETED] isn't a valid username")
                return
        
        for val in (username, password, mail, age, gender, country, occupation, description):
            if '|' in val or '_' in val:
                messagebox.showwarning("Warning", "User input can't contain | or _")
                return
        
        self.temp_user_profile = classes.User(username, password, mail, age, gender, country, occupation, date_creation, description)
        
        self.verification(mail)
        
    
    def user_register(self, user_profile: classes.User):
        data = send_and_recieve(f"REGUSR|{user_profile.username}|{user_profile.password}|{user_profile.mail}|{user_profile.age}|{user_profile.gender}|{user_profile.country}|{user_profile.occupation}|{user_profile.date_creation}|{user_profile.description}")
        
        if data[0] == "REGUSR":
            if data[1] == "new_user":
                self.controller.show_page(HomePage_Connected)
                return
            elif data[1] == "name_taken":
                messagebox.showwarning("Warning", "Username already in use")
            elif data[1] == "mail_taken":
                messagebox.showwarning("Warning", "Mail already in use")
            
            self.controller.show_page(RegisterPage)
    
    def verification(self, mail):
        self.controller.show_page(EnterVerificationCode, mail=mail, callback=self.after_verification, class_return_to=RegisterPage)

    def after_verification(self):
        global user_profile
        user_profile = self.temp_user_profile
        self.temp_user_profile = None
        
        self.user_register(user_profile)
        
        

class EnterVerificationCode(ctk.CTkFrame):
    def __init__(self, parent, controller, mail, callback, class_return_to):
        global current_conf_code
        super().__init__(parent)
        
        self.controller = controller
        current_conf_code = email_handler.send_conformation_mail(mail)
        if current_conf_code is None:
            # at this point the timer hasn't started yet so no need to stop it.
            messagebox.showerror("Error", "Email address entered is not in the affirmative format.")
            self.controller.show_page(class_return_to)
        self.callback = callback
        self.class_return_to = class_return_to

        self.top_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.top_frame.pack(side=ctk.TOP, padx=10, pady=10)

        self.label = ctk.CTkLabel(self.top_frame, text="Verification Page", font=("Helvetica", 32))
        self.label.pack(pady=10, padx=10)
        
        self.first_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.first_frame.pack(padx=20, pady=10)
        
        #wwe
        self.picture_frame = ctk.CTkFrame(self)
        self.picture_frame.pack(padx=20, pady=5)
        #welcome back icon 1.png
        mail_verify_image = Image.open(fp=os.path.join("assets","mail verify icon 1.png"))
        self.mail_verify_icon = ctk.CTkImage(light_image=mail_verify_image, size=(200, 200))
        self.mail_verify_label = ctk.CTkLabel(self.picture_frame, text="", image=self.mail_verify_icon)
        self.mail_verify_label.pack(pady=2)
        
        self.bottom_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.bottom_frame.pack(side=ctk.BOTTOM, padx=10, pady=10)

        self.verify_label = ctk.CTkLabel(self.first_frame, text="Enter verification code (sent in mail):")
        self.verify_label.pack(padx=10, pady=5)
        self.verify_entry = ctk.CTkEntry(self.first_frame)
        self.verify_entry.pack(padx=10, pady=5)
        
        self.timer = DynamicTime(self.first_frame, self.controller, mail, self.class_return_to)
        
        self.confirm_button = ctk.CTkButton(self.bottom_frame, text="Confirm", command=lambda: self.check_verify(self.verify_entry.get()))
        self.confirm_button.pack(padx=10, pady=5)
        
        self.go_back_button = ctk.CTkButton(self.bottom_frame, text="Return to previous screen", command=self.return_and_stop_time)
        self.go_back_button.pack(padx=10, pady=5)
    
    def check_verify(self, code):
        if code == current_conf_code:
            # verified
            self.timer.stop_timer_smoothly()
            self.callback()
        else:
            messagebox.showwarning("Warning", "Wrong code")
    
    def return_and_stop_time(self):
        self.timer.stop_timer_smoothly()
        
        self.controller.show_page(self.class_return_to)


class DynamicTime(ctk.CTkFrame):
    def __init__(self, parent, controller, mail, class_return_to):
        super().__init__(parent)
        
        self.pack(pady=5)
        
        self.controller = controller
        self.mail = mail
        self.class_return_to = class_return_to
        
        # Initialize timer duration (in seconds)
        self.timer_duration = 300  # 5 minutes
        
        # Create timer label
        self.timer_label = ctk.CTkLabel(self, text="", font=("Helvetica", 26))
        self.timer_label.pack(padx=5, pady=20)
        
        self.update_continuously = ctk.BooleanVar(master=self, value=True)

        # Start the timer
        self.start_timer()
    
    def start_timer(self):
        self.update_timer()
    
    def update_timer(self):
        global current_conf_code
        if self.update_continuously.get():
            if self.timer_duration > 0:
                minutes, seconds = divmod(self.timer_duration, 60)
                self.timer_label.configure(text=f"Time left: {minutes:02d}:{seconds:02d}")
                self.timer_duration -= 1
                self.job = self.after(1000, self.update_timer)  # Update every second
            else:
                #self.timer_label.configure(text="Time's up! Click 'Extend' to add 5 more minutes.")
                self.timer_label.configure(text="")
                if messagebox.askokcancel("Notify", "Time's up! Click 'OK' to resend conformation code and add 5 more minutes."):
                    self.timer_duration = 300
                    current_conf_code = email_handler.send_conformation_mail(self.mail)
                    self.update_timer()
                else:
                    self.stop_timer_smoothly()
                    self.controller.show_page(self.class_return_to)
            
    def stop_timer_smoothly(self):
        self.update_continuously = ctk.BooleanVar(master=self, value=False)
        self.after_cancel(self.job)


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.top_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.top_frame.pack(side=ctk.TOP, padx=10, pady=10)

        label = ctk.CTkLabel(self.top_frame, text="Login Page", font=("Helvetica", 32))
        label.pack(pady=10, padx=10)
        
        self.first_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.first_frame.pack(padx=20, pady=10)
        
        self.second_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.second_frame.pack(padx=20, pady=10)

        self.third_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.third_frame.pack(padx=20, pady=10)
        
        self.picture_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.picture_frame.pack(padx=20, pady=5)
        #welcome back icon 1.png
        welcome_icon_image = Image.open(fp=os.path.join("assets","welcome back icon 1.png"))
        self.welcome_icon = ctk.CTkImage(light_image=welcome_icon_image, size=(100, 100))
        self.welcome_label = ctk.CTkLabel(self.picture_frame, text="", image=self.welcome_icon)
        self.welcome_label.pack(pady=2)
        
        self.bottom_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.bottom_frame.pack(side=ctk.BOTTOM, padx=10, pady=10)

        name_label = ctk.CTkLabel(self.first_frame, text="Name:")
        name_label.pack(padx=5, pady=5)
        name_entry = ctk.CTkEntry(self.first_frame)
        name_entry.pack(padx=5, pady=5)

        password_label = ctk.CTkLabel(self.second_frame, text="Password:")
        password_label.pack(padx=5, pady=5)
        password_entry = ctk.CTkEntry(self.second_frame, show="*")
        password_entry.pack(padx=5, pady=5)
        
        email_label = ctk.CTkLabel(self.third_frame, text="Email:")
        email_label.pack(padx=5, pady=5)
        email_entry = ctk.CTkEntry(self.third_frame)
        email_entry.pack(padx=5, pady=5)

        login_button = ctk.CTkButton(self.bottom_frame, text="Login", command=lambda: self.user_login(controller, name_entry.get(), password_entry.get(), email_entry.get()))
        login_button.pack(padx=5, pady=10)
        
        go_back_button = ctk.CTkButton(self.bottom_frame, text="Return to opening screen", command=lambda: controller.show_page(OpeningScreen))
        go_back_button.pack(padx=5, pady=10)
    
    def user_login(self, controller, name, password, email):
        global user_profile
        
        if name == "[DELETED]":
            messagebox.showwarning("Warning", "[DELETED] isn't a valid username")
            return
        
        for val in (name, password, email):
            if '|' in val or '_' in val:
                messagebox.showwarning("Warning", "User input can't contain | or _")
                return
        
        data = send_and_recieve(f"LOGUSR|{name}|{password}|{email}")
        
        if data[0] == "LOGUSR":
            if data[1] == "correct_identification":
                user_profile = classes.User(data[2], None, data[3], data[4], data[5], data[6], data[7], data[8], data[9])
                controller.show_page(HomePage_Connected)
            elif data[1] == "failed_identification":
                messagebox.showerror("Error", "False user data")


class ForgotPassword(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        
        self.top_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.top_frame.pack(side=ctk.TOP, padx=10, pady=10)

        label = ctk.CTkLabel(self.top_frame, text="Forgot Password Page", font=("Helvetica", 32))
        label.pack(pady=10, padx=10)
        
        self.first_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.first_frame.pack(padx=10, pady=10)
        
        self.bottom_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.bottom_frame.pack(side=ctk.BOTTOM, padx=10, pady=10)
        
        self.email_label = ctk.CTkLabel(self.first_frame, text="Email:")
        self.email_label.pack(padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(self.first_frame)
        self.email_entry.pack(padx=10, pady=5)
        
        self.picture_frame = ctk.CTkFrame(self)
        self.picture_frame.pack(padx=20, pady=5)

        shield_icon_image = Image.open(fp=os.path.join("assets","shield checkbox icon 1.png"))
        self.shield_icon = ctk.CTkImage(light_image=shield_icon_image, size=(200, 200))
        self.shield_label = ctk.CTkLabel(self.picture_frame, text="", image=self.shield_icon)
        self.shield_label.pack(pady=20)
        
        self.verify_mail_button = ctk.CTkButton(self.bottom_frame, text="Verify Email", command=self.go_verify)
        self.verify_mail_button.pack(pady=10)

        #new_password_button = ctk.CTkButton(self, text="Login", command=lambda: self.user_login(controller, name_entry.get(), password_entry.get(), email_entry.get()))
        #new_password_button.pack(pady=10)
        
        self.go_back_button = ctk.CTkButton(self.bottom_frame, text="Return to opening screen", command=lambda: controller.show_page(OpeningScreen))
        self.go_back_button.pack(padx=5, pady=10)
    
    def go_verify(self):
        self.mail = self.email_entry.get()
        
        if '|' in self.mail or '_' in self.mail:
                messagebox.showwarning("Warning", "User input can't contain | or _ or be equel to [DELETED]")
                return
        
        self.controller.show_page(EnterVerificationCode, mail=self.mail, callback=self.choose_new_password, class_return_to=ForgotPassword)
    
    def choose_new_password(self):
        self.controller.show_page(ChoosePassword, mail=self.mail)

class ChoosePassword(ctk.CTkFrame):
    def __init__(self, parent, controller, mail):
        super().__init__(parent)
        
        self.controller = controller
        self.mail = mail
        
        self.top_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.top_frame.pack(side=ctk.TOP, padx=10, pady=10)

        label = ctk.CTkLabel(self.top_frame, text="Choose a new password", font=("Helvetica", 32))
        label.pack(pady=10, padx=10)
        
        self.first_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.first_frame.pack(padx=10, pady=10)
        
        self.bottom_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.bottom_frame.pack(side=ctk.BOTTOM, padx=10, pady=10)
        #wwe
        
        self.new_password_label = ctk.CTkLabel(self.first_frame, text="Enter new password:")
        self.new_password_label.pack(padx=10, pady=5)
        self.new_password_entry = ctk.CTkEntry(self.first_frame)
        self.new_password_entry.pack(padx=10, pady=5)
        self.new_password_button = ctk.CTkButton(self.bottom_frame, text="Set new password", command=lambda: self.send_new_password_server(self.new_password_entry.get()))
        self.new_password_button.pack(padx=10, pady=5)
        
        
        self.picture_frame = ctk.CTkFrame(self)
        self.picture_frame.pack(padx=20, pady=10)

        new_pass_icon_image = Image.open(fp=os.path.join("assets","new password icon 1.png"))
        self.new_pass_icon = ctk.CTkImage(light_image=new_pass_icon_image, size=(220, 222))
        self.new_pass_label = ctk.CTkLabel(self.picture_frame, text="", image=self.new_pass_icon)
        self.new_pass_label.pack(padx=10, pady=5)
        
        self.go_back_button = ctk.CTkButton(self.bottom_frame, text="Return to forgot password screen", command=lambda: controller.show_page(ForgotPassword))
        self.go_back_button.pack(padx=10, pady=5)
    
    
    def send_new_password_server(self, new_password):
        for val in (self.mail, new_password):
            if '|' in val or '_' in val:
                messagebox.showwarning("Warning", "User input can't contain | or _")
                return
        
        data = send_and_recieve(f"NPSUSR|{self.mail}|{new_password}")
        
        if data[0] == "NPSUSR":
            if data[1] == "password_updated":
                messagebox.showinfo("Info", "Password updated successfully")
                self.controller.show_page(LoginPage)

class HomePage_Connected(ctk.CTkFrame):
    def __init__(self, parent, controller):
        global user_profile
        super().__init__(parent)
        
        self.controller = controller
                
        # Top bar with logo, search bar, and login/register buttons
        self.top_bar = ctk.CTkFrame(self, fg_color="purple", bg_color="purple")
        self.top_bar.pack(fill=ctk.X)
        
        
        logo_icon_image = Image.open(os.path.join("assets","Thread Vortex logo.png"))
        self.logo_icon = ctk.CTkImage(light_image=logo_icon_image, size=(120, 73))
        self.logo_label = ctk.CTkLabel(self.top_bar, image=self.logo_icon, text="", fg_color="white", bg_color="purple")
        self.logo_label.pack(side=ctk.LEFT, padx=12, pady=1.25)
        
        
        self.search_bar = ctk.CTkEntry(self.top_bar)
        self.search_bar.pack(side=ctk.LEFT, padx=1)
        self.search_button = ctk.CTkButton(self.top_bar, text="Search🔎", border_color="black", border_width=3, fg_color="white", text_color="black", hover_color="cyan", width=100, command=lambda: self.search_h(self.search_bar.get()))
        self.search_button.pack(side=ctk.LEFT)
        self.disconnect_button = ctk.CTkButton(self.top_bar, text="Disconnect", fg_color="white", text_color="black", hover_color="cyan", border_color="black", border_width=3, command=lambda: self.disconnect(controller))
        self.disconnect_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)
        self.edit_profile_button = ctk.CTkButton(self.top_bar, text="Edit Profile", fg_color="white", text_color="black", hover_color="cyan", border_color="black", border_width=3, command=lambda: controller.show_page(EditProfilePage))
        self.edit_profile_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)
        
        # view profile button
        view_profile_icon_image = Image.open(fp=os.path.join("assets","default user icon 2.png"))
        self.view_profile_icon = ctk.CTkImage(light_image=view_profile_icon_image, size=(40, 40))
        self.view_profile_button = ctk.CTkButton(self.top_bar, width=100, border_color="black", border_width=3, text="", image=self.view_profile_icon, command=lambda: controller.show_page(ViewProfile, profile_username=user_profile.username, class_return_to=HomePage_Connected, edited_profile=False))
        self.view_profile_button.pack(side=ctk.RIGHT, padx=1.25, pady=1.25)

        # sidebar
        self.sidebar = ctk.CTkFrame(self, bg_color="purple", fg_color="purple")
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
        
        # new conversation button
        new_conversation_icon_image = Image.open(fp=os.path.join("assets","plus icon 3.png"))
        self.new_conversation_icon = ctk.CTkImage(light_image=new_conversation_icon_image, size=(40, 40))
        self.new_conversation_button = ctk.CTkButton(self.sidebar, fg_color="white", width=100, border_color="black", border_width=3, text="", image=self.new_conversation_icon, command=lambda: controller.show_page(CreateNewConversation))
        self.new_conversation_button.pack(side=ctk.TOP, padx=2, pady=5)
        
        
        # change configuration button
        self.configuration_frame = ctk.CTkFrame(self.sidebar, fg_color="white", border_color="black", border_width=3)
        self.configuration_frame.pack(side=ctk.TOP, padx=2, pady=8)
        
        reconfiguration_icon_image = Image.open(fp=os.path.join("assets","sort icon 1.png"))
        self.reconfiguration_icon = ctk.CTkImage(light_image=reconfiguration_icon_image, size=(40, 40))
        self.reconfiguration_label = ctk.CTkLabel(self.configuration_frame, image=self.reconfiguration_icon, text="")
        self.reconfiguration_label.pack(side=ctk.TOP, padx=5, pady=5)
        
        optionmenu_var = ctk.StringVar(value="")  # set initial value
        self.reconfiguration_combobox = ctk.CTkOptionMenu(master=self.configuration_frame, width=100,
                                       values=["", "Sort Alphabetically", "Sort Alphabetically (Reverse)", "Sort Chronologically", "Sort Chronologically (Reverse)", "Sort By Popularity", "Sort By Popularity (Reverse)"],
                                       command=self.reconfigure_conversations_screen,
                                       variable=optionmenu_var)
        self.reconfiguration_combobox.pack(side=ctk.TOP, padx=5, pady=5)

        # choose favorite conversations
        self.setup_favourites()

        # main content area with conversation to click and get into
        self.content_area = ModifiedCTkScrollableFrame(self)
        self.content_area.pack(fill=ctk.BOTH, expand=True)
        
        self.conversation_handler = HandleConversations(self.content_area, controller, HomePage_Connected, 5)
        
        self.content_area.set_func(self.conversation_handler.request_more)
    
    def search_h(self, to_search):
        if '|' in to_search or '_' in to_search:
                messagebox.showwarning("Warning", "User input can't contain | or _")
                return
        
        self.controller.show_page(SearchPage, str_to_search=to_search)
    
    def disconnect(self, controller):
        if messagebox.askokcancel("Warning", "You are about to disconnect from the program."):
            controller.reset_saved_frames()
            #controller.show_page(OpeningScreen)
    
    def reconfigure_conversations_screen(self, choice):
        #"Sort Alphabetically", "Sort Alphabetically (Reverse)", "Sort Chronologically", "Sort Chronologically (Reverse)", "Sort By Popularity", "Sort By Popularity (Reverse)"
        
        # if the default string was chosen then anyway nothing will change
        if choice == "":
            return
        
        forget_frame_widgets(self.content_area)
        
        # change the order shown on screen of the conversations
        self.conversation_handler.reconfigure_conversation_order(choice)
    
    def enter_pinned_conversation(self, choice):
        if choice != "":
            self.controller.show_page(InsideConversationGUI, title=choice, class_return_to=HomePage_Connected)
    
    def setup_favourites(self):
        #self.pinned_conversations = []
        self.pinned_frame = ctk.CTkFrame(self.sidebar, fg_color="white", border_color="black", border_width=3)
        self.pinned_frame.pack(padx=2, pady=10)
        
        pinned_image = Image.open(fp=os.path.join("assets","pin icon 2.png"))
        self.pinned_icon = ctk.CTkImage(light_image=pinned_image, size=(40, 40))
        self.pinned_label = ctk.CTkLabel(self.pinned_frame, fg_color="white", width=100, text="", image=self.pinned_icon)
        self.pinned_label.pack(side=ctk.TOP, padx=5, pady=5)
        
        self.pinned_convs_titles = [""]
        # GUVCNV get user pinned conversations
        data = send_and_recieve(f"GUPCNV|{user_profile.username}")
        
        if data[0] == "GUPCNV":
            if data[1] != "no_pins":
                for convtitle in data[1:]:
                    self.pinned_convs_titles.append(convtitle)
    
        optionmenu_var = ctk.StringVar(value="")  # set initial value
        self.pinned_combobox = ctk.CTkOptionMenu(master=self.pinned_frame, width=100,
                                       values=self.pinned_convs_titles,
                                       command=self.enter_pinned_conversation,
                                       variable=optionmenu_var)
        self.pinned_combobox.pack(side=ctk.TOP, padx=5, pady=5)
    
    def add_pinned_conversation(self, conversation_title):
        self.pinned_convs_titles.append(conversation_title)
        self.pinned_combobox.configure(values=self.pinned_convs_titles)
    
    def remove_pinned_conversation(self, conversation_title):
        # in the future when conversations can be deleted I will get ValueError here.
        self.pinned_convs_titles.remove(conversation_title)
        self.pinned_combobox.configure(values=self.pinned_convs_titles)
    
def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()

def forget_frame_widgets(frame):
    for widgets in frame.winfo_children():
        widgets.forget()

class SearchPage(ctk.CTkFrame):
    def __init__(self, parent, controller, str_to_search):
            global last_search
            super().__init__(parent)
            
            last_search = str_to_search
            self.str_to_search = str_to_search
            self.top_bar = ctk.CTkFrame(self, fg_color="purple", bg_color="purple")
            self.top_bar.pack(fill=ctk.X)
            
            logo_icon_image = Image.open(os.path.join("assets","Thread Vortex logo.png"))
            self.logo_icon = ctk.CTkImage(light_image=logo_icon_image, size=(120, 73))
            self.logo_label = ctk.CTkLabel(self.top_bar, image=self.logo_icon, text="", fg_color="white", bg_color="purple")
            self.logo_label.pack(side=ctk.LEFT, padx=12, pady=1.25)
            
            self.search_bar = ctk.CTkEntry(self.top_bar)
            self.search_bar.pack(side=ctk.LEFT, padx=1)
            self.search_button = ctk.CTkButton(self.top_bar, text="Search🔎", fg_color="white", border_color="black", border_width=3, text_color="black", hover_color="cyan", width=100, command=lambda: self.search_again_h(self.search_bar.get()))
            self.search_button.pack(side=ctk.LEFT)
            
            # Sidebar with topics
            self.sidebar = ctk.CTkFrame(self, bg_color="purple", fg_color="purple")
            self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
            
            self.go_back_button = ctk.CTkButton(self.sidebar, fg_color="white", border_color="black", border_width=3, text_color="black", hover_color="cyan", width=100, text="Return to Home page", command=lambda: controller.show_page(HomePage_Connected))
            self.go_back_button.pack(side=ctk.TOP, padx=1.25, pady=1.25)
            
            # Main content area with messages
            self.content_area = ctk.CTkScrollableFrame(self)
            self.content_area.pack(fill=ctk.BOTH, expand=True)
            
            self.conversation_handler = HandleConversations(self.content_area, controller, SearchPage, 5, True)
            self.conversation_handler.search_all(str_to_search)
    
    def search_again_h(self, to_search):
        if '|' in to_search or '_' in to_search:
            messagebox.showwarning("Warning", "User input can't contain | or _")
            return

        self.search_again(to_search)
    
    def search_again(self, to_search):
        global last_search
        clear_frame(self.content_area)
        last_search = to_search
        self.conversation_handler.search_all(to_search)
                
                
class EditProfilePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        global user_profile
        super().__init__(parent)
        
        self.bottom_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.bottom_frame.pack(side=ctk.BOTTOM, padx=10, pady=10)
        
        self.top_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.top_frame.pack(side=ctk.TOP, padx=10, pady=10)
        
        label = ctk.CTkLabel(self.top_frame, text="Edit Profile Page", font=("Helvetica", 32))
        label.pack(padx=10, pady=5)
        
        # Left Frame
        self.left_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=20, pady=10)

        # Right Frame
        self.right_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=10)
        

        password_label = ctk.CTkLabel(self.left_frame, text="Password:")
        password_label.pack(padx=5, pady=5)
        password_entry = ctk.CTkEntry(self.left_frame, show="*")
        password_entry.pack(padx=5, pady=5)
        
        age_label = ctk.CTkLabel(self.left_frame, text="Age:")
        age_label.pack(padx=5, pady=5)
        age_entry = ctk.CTkEntry(self.left_frame)
        age_entry.insert(0, user_profile.age)
        age_entry.pack(padx=5, pady=5)

        gender_label = ctk.CTkLabel(self.left_frame, text="Gender:")
        gender_label.pack(padx=5, pady=5)
        gender_entry = ctk.CTkEntry(self.left_frame)
        gender_entry.insert(0, user_profile.gender)
        gender_entry.pack(padx=5, pady=5)

        country_label = ctk.CTkLabel(self.left_frame, text="Country:")
        country_label.pack(padx=5, pady=5)
        country_entry = ctk.CTkEntry(self.left_frame)
        country_entry.insert(0, user_profile.country)
        country_entry.pack(padx=5, pady=5)

        occupation_label = ctk.CTkLabel(self.right_frame, text="Occupation:")
        occupation_label.pack(padx=5, pady=5)
        occupation_entry = ctk.CTkEntry(self.right_frame)
        occupation_entry.insert(0, user_profile.occupation)
        occupation_entry.pack(padx=5, pady=5)

        description_label = ctk.CTkLabel(self.right_frame, text="Description:")
        description_label.pack(padx=5, pady=5)
        description_entry = ctk.CTkTextbox(self.right_frame, wrap="word")
        description_entry.insert('1.0', user_profile.description)
        description_entry.pack(padx=5, pady=5)

        edit_profile_button = ctk.CTkButton(self.bottom_frame, text="Commit changes", command=lambda: self.user_edit_profile_h(controller, password_entry.get(), age_entry.get(), gender_entry.get(), country_entry.get(), occupation_entry.get(), description_entry.get("1.0", "end-1c")))
        edit_profile_button.pack(padx=5, pady=10)
        
        go_back_button = ctk.CTkButton(self.bottom_frame, text="Return to main screen", command=lambda: controller.show_page(HomePage_Connected))
        go_back_button.pack(padx=5, pady=10)
    
    def user_edit_profile_h(self, controller, password, age: str, gender, country, occupation, description):
        global user_profile
        
        if not age.isnumeric() and age != "":
            messagebox.showwarning("Warning", "Age must be numeric.")
            return
        
        for val in (password, age, gender, country, occupation, description):
            if '|' in val or '_' in val:
                messagebox.showwarning("Warning", "User input can't contain | or _")
                return
        
        user_profile.edit_profile(age, gender, country, occupation, description)
        self.user_edit_profile(controller, user_profile, password)
    
    def user_edit_profile(self, controller, user_profile: classes.User, password):
        data = send_and_recieve(f"EDTUSR|{user_profile.username}|{password}|{user_profile.mail}|{user_profile.age}|{user_profile.gender}|{user_profile.country}|{user_profile.occupation}|{user_profile.date_creation}|{user_profile.description}")
        
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
            user_data = self.get_other_user_data()
            if user_data == "no_user":
                user_data = classes.User("[DELETED]", "", "", "", "", "", "", "", "")
            elif user_data == "user_deleted":
                user_data = classes.User("[DELETED]", "", "", "", "", "", "", "", "")
        
        self.bottom_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.bottom_frame.pack(side=ctk.BOTTOM, padx=10, pady=10)
        
        if user_data.username != "[DELETED]":
            
            self.top_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
            self.top_frame.pack(side=ctk.TOP, padx=10, pady=10)
            
            self.left_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
            self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=20, pady=10)

            self.right_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
            self.right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=10)
                
            name_label = ctk.CTkLabel(self.top_frame, text=f"The info page of \"{user_data.username}\"", font=("Helvetica", 32))
            name_label.pack(padx=10, pady=5)

            email_label = ctk.CTkLabel(self.left_frame, text=f"Email:\n{user_data.mail}", font=("Helvetica", 24), )
            email_label.pack(padx=5, pady=5)
            
            self.seperate_label1 = ctk.CTkLabel(self.left_frame, text="_____")
            self.seperate_label1.pack(padx=5, pady=5)
            
            age_label = ctk.CTkLabel(self.left_frame, text=f"Age:\n{user_data.age}", font=("Helvetica", 24))
            age_label.pack(padx=5, pady=5)
            
            self.seperate_label2 = ctk.CTkLabel(self.left_frame, text="_____")
            self.seperate_label2.pack(padx=5, pady=5)

            gender_label = ctk.CTkLabel(self.left_frame, text=f"Gender:\n{user_data.gender}", font=("Helvetica", 24))
            gender_label.pack(padx=5, pady=5)
            
            self.seperate_label3 = ctk.CTkLabel(self.left_frame, text="_____")
            self.seperate_label3.pack(padx=5, pady=5)

            country_label = ctk.CTkLabel(self.left_frame, text=f"Country:\n{user_data.country}", font=("Helvetica", 24))
            country_label.pack(padx=5, pady=5)

            occupation_label = ctk.CTkLabel(self.right_frame, text=f"Occupation:\n{user_data.occupation}", font=("Helvetica", 24))
            occupation_label.pack(padx=5, pady=5)
            
            self.seperate_label4 = ctk.CTkLabel(self.right_frame, text="_____")
            self.seperate_label4.pack(padx=5, pady=5)
            
            member_since_label = ctk.CTkLabel(self.right_frame, text=f"Member Since:\n{user_data.date_creation}", font=("Helvetica", 24))
            member_since_label.pack(padx=5, pady=5)
            
            self.seperate_label5 = ctk.CTkLabel(self.right_frame, text="_____")
            self.seperate_label5.pack(padx=5, pady=5)

            self.description_label = ctk.CTkTextbox(self.right_frame, wrap="word")
            self.description_label.tag_config("center", justify="center")
            self.description_label.insert("1.0", user_data.description, "center")
            self.description_label.configure(spacing1=20)
            self.description_label.configure(state=ctk.DISABLED)
            self.description_label.pack(padx=5, pady=5)
            
            if profile_username == user_profile.username:
                delete_user_button = ctk.CTkButton(self.bottom_frame, text="Delete user", command= self.delete_user)
                delete_user_button.pack(pady=10)
        else:
            info_label = ctk.CTkLabel(self, text=f"This account exists no longer!", font=("Helvetica", 32))
            info_label.pack(padx=5, pady=5)
        
        go_back_button = ctk.CTkButton(self.bottom_frame, text="Return to main screen", command=lambda: self.go_back_h())
        go_back_button.pack(padx=10, pady=10)
    
    def get_other_user_data(self):
        data = send_and_recieve(f"GETUSR|{self.profile_username}")
        
        if data[0] == "GETUSR":
            if data[1] == "no_user":
                return "no_user"
            elif data[1] == "user_deleted":
                return "user_deleted"
            else: 
                user_data = classes.User(data[1], None, data[2], data[3], data[4], data[5], data[6], data[7], data[8])
                return user_data
    
    def go_back_h(self):
        if self.class_return_to == SearchPage:
            self.controller.show_page(self.class_return_to, str_to_search=last_search) 
        else:
            self.controller.show_page(self.class_return_to)
    
    def delete_user(self):
        if messagebox.askokcancel("Warning", "You are about to permenantly delete your profile and be disconnected"):
            data = send_and_recieve(f"DELUSR|{self.profile_username}")

            if data[0] == "DELUSR":
                if data[1] == "done":
                    # disconnect from the account
                    self.controller.reset_saved_frames()

class CreateNewConversation(ctk.CTkFrame):
    def __init__(self, parent, controller):
        global user_profile
        super().__init__(parent)
        
        self.bottom_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.bottom_frame.pack(side=ctk.BOTTOM, padx=10, pady=10)
        
        self.top_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.top_frame.pack(side=ctk.TOP, padx=10, pady=10)
        
        # Left Frame
        self.big_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.big_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=8)
        
        frame_title_label = ctk.CTkLabel(self.top_frame, text="Create a new conversation", font=("Helvetica", 32))
        frame_title_label.pack(padx=5, pady=5)
        
        conversation_title_label = ctk.CTkLabel(self.big_frame, text="Title of the conversation:")
        conversation_title_label.pack(padx=5, pady=5)
        conversation_title_entry = ctk.CTkEntry(self.big_frame)
        conversation_title_entry.pack(padx=5, pady=5)
        
        message_content_label = ctk.CTkLabel(self.big_frame, text="Message content:")
        message_content_label.pack(padx=5, pady=5)
        message_content_entry = ctk.CTkTextbox(self.big_frame, wrap="word")
        message_content_entry.pack(padx=5, pady=5)
        
        restriction_label = ctk.CTkLabel(self.big_frame, text="Restrict access:")
        restriction_label.pack(padx=5, pady=5)
        radio_var = ctk.StringVar()
        restriction_radiobutton1 = ctk.CTkRadioButton(master=self.big_frame, text="18+", variable= radio_var, value="18+")
        restriction_radiobutton2 = ctk.CTkRadioButton(master=self.big_frame, text="Unrestricted", variable= radio_var, value="unrestricted")
        restriction_radiobutton1.pack(padx=10, pady=2)
        restriction_radiobutton2.pack(padx=10, pady=2)
        
        add_conversation_button = ctk.CTkButton(self.bottom_frame, text="Create conversation", command=lambda: self.add_conversation(controller, conversation_title_entry.get(), message_content_entry.get("1.0", "end-1c"), radio_var.get()))
        add_conversation_button.pack(padx=10, pady=5)
        
        go_back_button = ctk.CTkButton(self.bottom_frame, text="Return to main screen", command=lambda: controller.show_page(HomePage_Connected))
        go_back_button.pack(padx=10, pady=5)
    
    def add_conversation(self, controller, conversation_title, message_content, restriction_status):
        current_date = datetime.datetime.now()
        creation_date = f"{current_date.day}/{current_date.month}/{current_date.year} {str(current_date.hour).zfill(2)}:{str(current_date.minute).zfill(2)}"
        
        for val in (conversation_title, message_content):
            if '|' in val or '_' in val:
                messagebox.showwarning("Warning", "User input can't contain | or _")
                return
        
        if restriction_status == "":
            restriction_status = "unrestricted"
        
        if restriction_status == "18+" and (user_profile.age == "" or int(user_profile.age) < 18):
            messagebox.showwarning("Warning", "To restrict access to 18+ you must be yourself 18+.")
            return
        
        data = send_and_recieve(f"NEWCNV|{conversation_title}|{message_content}|{restriction_status}|{creation_date}|{user_profile.username}")

        if data[0] == "NEWCNV":
            if data[1] == "new_conversation_added":
                messagebox.showinfo("Info", "Created new conversation!")
                controller.show_page(InsideConversationGUI, title=conversation_title, class_return_to=HomePage_Connected)
            elif data[1] == "title_issue":
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
        self.date = date
        
        self.user_button = ctk.CTkButton(self, text=username, fg_color="white", text_color="black", hover_color="cyan", command= lambda: controller.show_page(ViewProfile, profile_username=username, class_return_to=class_return_to, edited_profile=False))
        self.user_button.pack(side=ctk.LEFT, padx=10)
        self.date_label = ctk.CTkLabel(self, text=date)
        self.date_label.pack(side=ctk.RIGHT, padx=10)
        
        self.set_pinning()
        
        ####        
        
        self.voice_frame = ctk.CTkFrame(self, fg_color="white", border_color="black", border_width=2)
        self.voice_frame.pack(side=ctk.RIGHT, padx=5, pady=2)
        
        mute_icon_image = Image.open(fp=os.path.join("assets","mute icon 1.png"))
        self.mute_icon = ctk.CTkImage(light_image=mute_icon_image, size=(30, 30))
        self.mute_button = ctk.CTkButton(self.voice_frame, width=50, fg_color="white", text="", image=self.mute_icon, command=stop_speech)
        self.mute_button.pack(side=ctk.BOTTOM, padx=5, pady=3)
        
        speaker_icon_image = Image.open(fp=os.path.join("assets","speaker icon 1.png"))
        self.speaker_icon = ctk.CTkImage(light_image=speaker_icon_image, size=(30, 30))
        self.speech_text_button = ctk.CTkButton(self.voice_frame, width=50, fg_color="white", text="", image=self.speaker_icon, command=lambda: threading.Thread(target=speak_text, args=(title,)).start())
        self.speech_text_button.pack(side=ctk.TOP, padx=5, pady=3)
        
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
        data = send_and_recieve(f"GEPCNV|{user_profile.username}|{self.title}")

        if data[0] == "GEPCNV":
            self.pins = data[2]
            self.current_pin_status = data[1]
            
            self.pins_frame = ctk.CTkFrame(self, fg_color="white", border_color="black", border_width=2)
            self.pins_frame.pack(side=ctk.RIGHT, padx=5, pady=2)
            
            pin_image = Image.open(fp=os.path.join("assets","pin icon 2.png"))
            self.pin_icon = ctk.CTkImage(light_image=pin_image, size=(30, 30))
            self.pin_button = ctk.CTkButton(self.pins_frame, width=50, text="", image=self.pin_icon, command=self.pin_action)
            self.pin_button.pack(side=ctk.TOP, padx=5, pady=3)
            
            self.pins_label = ctk.CTkLabel(self.pins_frame, text=self.pins)
            self.pins_label.pack(side=ctk.BOTTOM, padx=5, pady=3)
            
            if self.current_pin_status == "pinned":
                self.pin_button.configure(fg_color="#FFD700", hover_color="#FFD300")

    def pin_action(self):
        if self.current_pin_status == "pinned":
            # reset the color
            self.pin_button.configure(fg_color="#3B8ED0", hover_color="#36719F")
        else:
            # change to yellow
            self.pin_button.configure(fg_color="#FFD700", hover_color="#FFD300")
        
        data = send_and_recieve(f"PINCNV|{user_profile.username}|{self.title}")
        
        if data[0] == "PINCNV":
            self.pins = data[2]
            self.pins_label.configure(text=self.pins)
            if data[1] == "pinned":
                self.current_pin_status = "pinned"
                
                self.controller.change_pinned(self.title, how_to_change="add", class_return_to=self.class_return_to)
            elif data[1] == "no_pin":
                self.current_pin_status = "no_pin"
                
                self.controller.change_pinned(self.title, how_to_change="remove", class_return_to=self.class_return_to)
    
    def change_pin_manually(self):
        data = send_and_recieve(f"GEPCNV|{user_profile.username}|{self.title}")

        if data[0] == "GEPCNV":
            self.pins = data[2]
            self.current_pin_status = data[1]
            
        if self.current_pin_status == "pinned":
            self.pin_button.configure(fg_color="#FFD700", hover_color="#FFD300")
            self.pins_label.configure(text=self.pins)
        elif self.current_pin_status == "no_pin":
            self.pin_button.configure(fg_color="#3B8ED0", hover_color="#36719F")
            self.pins_label.configure(text=self.pins)
    
    def re_pack(self):
        self.pack_propagate(False)
        self.pack(fill=ctk.X, padx=4, pady=2)
        
class HandleConversations:
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
        data = send_and_recieve(f"FSTCNV|{self.amount}")

        if data[0] == "FSTCNV":
            if data[1] != "no_conversations":
                conversations = []
                for convdata in data[1:]:
                    conv_splt = convdata.split('_')
                    conversations.append(classes.ConversationStruct(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
                conversations = list(reversed(conversations))
                self.draw_conversations(conversations)
        return conversations

    def draw_conversations(self, conversations):
        for conv in conversations:
            convgui = ConversationGUI(self.frame_area, self.controller, conv.title, conv.creator_username, conv.creation_date, conv.restrictions, self.class_return_to)
            if not self.search_active:
                self.convgui_dict[conv.title] = convgui
            
    
    def request_more(self):
        data = send_and_recieve(f"MORCNV|{self.amount}")

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
            self.convgui_dict = {key: value for key, value in sorted(self.convgui_dict.items(), key=lambda item: (item[1].title))}
        elif order_by == "Sort Alphabetically (Reverse)":
            self.convgui_dict = {key: value for key, value in sorted(self.convgui_dict.items(), key=lambda item: (item[1].title), reverse=True)}
        elif order_by == "Sort Chronologically":
            self.convgui_dict = {key: value for key, value in sorted(self.convgui_dict.items(), key=lambda item: (self.sort_by_creation_date(item[1].date)))}
        elif order_by == "Sort Chronologically (Reverse)":
            self.convgui_dict = {key: value for key, value in sorted(self.convgui_dict.items(), key=lambda item: (self.sort_by_creation_date(item[1].date)), reverse=True)}
        elif order_by == "Sort By Popularity":
            # Sort the dictionary by 'pins' attribute
            # for normal order reverse is needed because of the mechanism this lambda follows
            self.convgui_dict = {key: value for key, value in sorted(self.convgui_dict.items(), key=lambda item: (item[1].pins), reverse=True)}
                
        elif order_by == "Sort By Popularity (Reverse)":
            # Sort the dictionary by 'pins' attribute
            # for normal order reverse is needed because of the mechanism this lambda follows
            self.convgui_dict = {key: value for key, value in sorted(self.convgui_dict.items(), key=lambda item: (item[1].pins))}

        self.draw_dict()
    
    def draw_dict(self):
        for item in self.convgui_dict.items():
            item[1].re_pack()
            
    def sort_by_creation_date(self, date):
        creation_date = datetime.datetime.strptime(date, "%d/%m/%Y %H:%M")
        return creation_date
    
    def search_all(self, search_for):
        data = send_and_recieve(f"SRCCNV|{search_for}")

        if data[0] == "SRCCNV":
            if data[1] != "word_not_found":
                found_conversations = []
                for convdata in data[1:]:
                    conv_splt = convdata.split('_')
                    self.search_conversations_lst.append(classes.ConversationStruct(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
                    found_conversations.append(classes.ConversationStruct(conv_splt[0], conv_splt[1], conv_splt[2], conv_splt[3]))
                self.draw_conversations(found_conversations)

class InsideConversationGUI(ctk.CTkFrame):
    def __init__(self, parent, controller, title, class_return_to):
        global user_profile
        super().__init__(parent)
        self.class_return_to = class_return_to

        self.controller = controller
        self.title = title
        self.top_bar = ctk.CTkFrame(self, fg_color="purple", bg_color="purple")
        self.top_bar.pack(fill=ctk.X)
        self.title_label = ctk.CTkLabel(self.top_bar, text=f"{self.title}", fg_color="purple", bg_color="purple", text_color="white", font=("Helvetica", 24))
        self.title_label.pack(padx=12, pady=1.25)

        self.sidebar = ctk.CTkFrame(self, bg_color="purple", fg_color="purple")
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)
        
        self.go_back_button = ctk.CTkButton(self.sidebar, fg_color="white", text_color="black", hover_color="cyan", width=100, text="Return to Home page", command=self.go_back_smoothly)
        self.go_back_button.pack(side=ctk.TOP, padx=1.25, pady=1.25)
        
        
        self.bottom_bar = ctk.CTkFrame(self, fg_color="white", height=100)
        self.bottom_bar.pack_propagate(False)
        self.bottom_bar.pack(side=ctk.BOTTOM, fill=ctk.X)

        self.message_content_entry = ctk.CTkTextbox(self.bottom_bar, border_color="black", border_width=2, wrap="word")
        self.message_content_entry.pack(padx=5, pady=2, side=ctk.LEFT, fill=ctk.X, expand=True)
        
        self.post_message_button = ctk.CTkButton(self.bottom_bar, fg_color="white", border_color="black", border_width=2, text_color="black", hover_color="cyan", text="Post", command=lambda: self.post_message(self.message_content_entry.get("1.0", "end-1c")))
        self.post_message_button.pack(padx=5, pady=2, side=ctk.RIGHT, fill=ctk.Y)
        
        # content area with messages to read
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
        
        if '|' in message_content or '_' in message_content:
            messagebox.showwarning("Warning", "User input can't contain | or _")
            return
        
        self.message_content_entry.delete("1.0","end")
        
        data = send_and_recieve(f"NEWMSG|{message_content}|{creation_date}|{user_profile.username}|{self.title}")

        if data[0] == "NEWMSG":
            if data[1] == "new_message_added":

                messagebox.showinfo("Info", "added new message")        

class HandleMessages:
    def __init__(self, frame_area, controller, conversation_title, amount=5) -> None:
        self.frame_area = frame_area
        self.controller = controller
        self.conversation_title = conversation_title
        self.amount = amount
        self.messages_lst = self.get_initial_messages()

    
    def get_initial_messages(self):
        data = send_and_recieve(f"FSTMSG|{self.amount}|{self.conversation_title}")

        if data[0] == "FSTMSG":
            messages = []
            if data[1] != "no_messages":
                
                for msgdata in data[1:]:
                    msg_splt = msgdata.split('_')
                    messages.append(classes.MessageStruct(msg_splt[1], msg_splt[2], msg_splt[3], msg_splt[4], msg_splt[0]))
        
                self.draw_messages(messages)
        return messages

    def draw_messages(self, messages):
        # messages: list[classes.MessageStruct]
        for msg in messages:
            MessageGUI(self.frame_area, self.controller, msg.content, msg.date_published, msg.sender_username, msg.conversation_title, str(msg.id), self)
    
    def request_more(self):
        # {self.messages_lst[-1] won't cause out of range error beacause when creating a conversation the client will write the first message in that conversation
        
        try:
        
            data = send_and_recieve(f"MORMSG|{self.amount}|{self.conversation_title}|{self.messages_lst[-1].id}")

            if data[0] == "MORMSG":
                if data[1] != "no_messages":
                    messages = []
                    for msgdata in data[1:]:
                        msg_splt = msgdata.split('_')
                        self.messages_lst.append(classes.MessageStruct(msg_splt[1], msg_splt[2], msg_splt[3], msg_splt[4], msg_splt[0]))
                        messages.append(classes.MessageStruct(msg_splt[1], msg_splt[2], msg_splt[3], msg_splt[4], msg_splt[0]))
                    self.draw_messages(messages)
                    #self.messages_lst.append(messages)
        
        except IndexError:
            self.messages_lst = self.get_initial_messages()
        
    
    def delete_message_from_lst(self, id_message):
        self.messages_lst = [message for message in self.messages_lst if message.id != id_message]
        print()
           
class MessageGUI(ctk.CTkFrame):
    def __init__(self, parent, controller, content, date, username, conversation_title, id, the_handler):
        super().__init__(parent, height=100, fg_color="white", corner_radius=50, border_color="black", border_width=2)  # Increase border_width
        self.pack(fill=ctk.X, padx=4, pady=2)
        
        self.id = id
        self.the_handler = the_handler
        
        # this frame will know its place, but will not be shown. shown only if its the user, later in the function.
        self.del_edit_frame = ctk.CTkFrame(self, fg_color="white", width=0, height=0)
        self.del_edit_frame.pack(side=ctk.BOTTOM, padx=5, pady=5)
        
        self.user_button = ctk.CTkButton(self, text=username, fg_color="white", text_color="black", hover_color="cyan", command= lambda: controller.show_page(ViewProfile, profile_username=username, class_return_to=InsideConversationGUI, edited_profile=False))
        self.user_button.pack(side=ctk.LEFT, padx=10)
        
        self.date_label = ctk.CTkLabel(self, text=date)
        self.date_label.pack(side=ctk.RIGHT, padx=10)
        ####
        
        self.set_voting()
        
        ####
        
        self.voice_frame = ctk.CTkFrame(self, fg_color="white", border_color="black", border_width=2)
        self.voice_frame.pack(side=ctk.RIGHT, padx=5, pady=2)
        
        mute_icon_image = Image.open(fp=os.path.join("assets","mute icon 1.png"))
        self.mute_icon = ctk.CTkImage(light_image=mute_icon_image, size=(30, 30))
        self.mute_button = ctk.CTkButton(self.voice_frame, width=50, fg_color="white", text="", image=self.mute_icon, command=stop_speech)
        self.mute_button.pack(side=ctk.BOTTOM, padx=5, pady=3)
        
        speaker_icon_image = Image.open(fp=os.path.join("assets","speaker icon 1.png"))
        self.speaker_icon = ctk.CTkImage(light_image=speaker_icon_image, size=(30, 30))
        self.speech_text_button = ctk.CTkButton(self.voice_frame, width=50, fg_color="white", text="", image=self.speaker_icon, command=lambda: threading.Thread(target=speak_text, args=(content,)).start())
        self.speech_text_button.pack(side=ctk.TOP, padx=5, pady=3)
        ####

        self.content_label = ctk.CTkTextbox(self, fg_color="#E5E4E2", height=150, wrap="word")
        self.content_label.tag_config("center", justify="center")
        self.content_label.insert("1.0", content, "center")
        self.content_label.configure(spacing1=20)
        self.content_label.configure(state=ctk.DISABLED)
        self.content_label.pack(side=ctk.LEFT, pady=10, fill=ctk.X, expand=True)
        
        
        if username == user_profile.username:
            self.configure(fg_color="#BEDBED")
            self.user_button.configure(fg_color="#BEDBED")
            self.date_label.configure(fg_color="#BEDBED")
            self.mute_button.configure(fg_color="#BEDBED")
            self.speech_text_button.configure(fg_color="#BEDBED")
            self.content_label.configure(fg_color="#ADD8E6")
            self.votes_frame.configure(fg_color="#BEDBED")
            self.del_edit_frame.configure(fg_color="#BEDBED")
            self.voice_frame.configure(fg_color="#BEDBED")
            
            delete_image = Image.open(fp=os.path.join("assets","delete icon 1.png"))
            self.delete_icon = ctk.CTkImage(light_image=delete_image, size=(30, 30))
            self.delete_button = ctk.CTkButton(self.del_edit_frame, width=50, text="", image=self.delete_icon, command=self.delete_message)
            self.delete_button.pack(side=ctk.RIGHT, pady=3)
            
            edit_image = Image.open(fp=os.path.join("assets","edit icon 1.png"))
            self.edit_icon = ctk.CTkImage(light_image=edit_image, size=(30, 30))
            self.edit_button = ctk.CTkButton(self.del_edit_frame, width=50, text="", image=self.edit_icon, command=self.edit_message)
            self.edit_button.pack(side=ctk.RIGHT, pady=3)
            
            confirm_image = Image.open(fp=os.path.join("assets","confirm icon 1.png"))
            self.confirm_icon = ctk.CTkImage(light_image=confirm_image, size=(30, 30))
            self.confirm_button = ctk.CTkButton(self.del_edit_frame, width=50, text="", image=self.confirm_icon, command=self.confirm_edit)
            
    def delete_message(self):
        self.destroy()
        
        data = send_and_recieve(f"DELMSG|{self.id}|{user_profile.username}")

        if data[0] == "DELMSG":
            if data[1] == "success":
                self.the_handler.delete_message_from_lst(self.id)
                messagebox.showinfo("Info", "message deleted successfully")
    
    def edit_message(self):
        self.content_label.configure(state=ctk.NORMAL)
        self.edit_button.forget()
        self.confirm_button.pack(side=ctk.RIGHT, pady=3)
    
    def confirm_edit(self):
        self.content_label.configure(state=ctk.DISABLED)
        self.confirm_button.forget()
        self.edit_button.pack(side=ctk.RIGHT, pady=3)
        
        content = self.content_label.get("1.0", "end-1c")
        data = send_and_recieve(f"EDTMSG|{self.id}|{content}")

        if data[0] == "EDTMSG":
            if data[1] == "success":
                messagebox.showinfo("Info", "message edited successfully")

        
    def set_voting(self):
        # get buttons state (has user already votes here?), and the current number of votes on this message
        data = send_and_recieve(f"GEVMSG|{user_profile.username}|{self.id}")

        if data[0] == "GEVMSG":
            self.votes = data[2]
            self.current_vote = data[1]
            
            self.votes_frame = ctk.CTkFrame(self, fg_color="white", border_color="black", border_width=2)
            self.votes_frame.pack(side=ctk.RIGHT, padx=10, pady=5)
            
            upvote_image = Image.open(fp=os.path.join("assets","upvote icon 1.png"))
            self.upvote_icon = ctk.CTkImage(light_image=upvote_image, size=(30, 30))
            self.upvote_button = ctk.CTkButton(self.votes_frame, width=50, text="", image=self.upvote_icon, command=self.upvote_action)
            self.upvote_button.pack(side=ctk.TOP, padx=10, pady=3)
            
            self.votes_label = ctk.CTkLabel(self.votes_frame, text=self.votes)
            self.votes_label.pack(padx=10, pady=3)
            
            downvote_icon_image = Image.open(fp=os.path.join("assets","downvote icon 1.png"))
            self.downvote_icon = ctk.CTkImage(light_image=downvote_icon_image, size=(30, 30))
            self.downvote_button = ctk.CTkButton(self.votes_frame, width=50, text="", image=self.downvote_icon, command=self.downvote_action)
            self.downvote_button.pack(side=ctk.BOTTOM, padx=10, pady=3)
            
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
        
        data = send_and_recieve(f"VOTMSG|upvote|{user_profile.username}|{self.id}")

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
            
        data = send_and_recieve(f"VOTMSG|downvote|{user_profile.username}|{self.id}")

        if data[0] == "VOTMSG":
            self.votes = data[2]
            self.votes_label.configure(text=self.votes)
            if data[1] == "upvote":
                self.current_vote = "upvote"
            elif data[1] == "downvote":
                self.current_vote = "downvote"
            elif data[1] == "no_vote":
                self.current_vote = "no_vote"

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
        logo_icon_image = Image.open(os.path.join("assets","Thread Vortex logo.png"))
        self.logo_icon = ctk.CTkImage(light_image=logo_icon_image, size=(400, 246))
        self.logo_label = ctk.CTkLabel(self.top_frame, image=self.logo_icon, text="")
        self.logo_label.pack(pady=5)

        credits_label = ctk.CTkLabel(self.top_frame, text="Created by Idan Barkin", font=("Roboto", 40))
        credits_label.pack(pady=5)
        # Left Frame
        self.center_frame = ctk.CTkFrame(self, border_color="black", border_width=2)
        self.center_frame.pack(side=ctk.BOTTOM, fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Chat icon
        failed_icon_image = Image.open(os.path.join("assets","failed icon 1.png"))  
        self.failed_icon = ctk.CTkImage(light_image=failed_icon_image, size=(100, 100))
        self.failed_icon_label = ctk.CTkLabel(self.center_frame, image=self.failed_icon, text="")
        self.failed_icon_label.pack(pady=5)
        
        self.failed_label = ctk.CTkLabel(self.center_frame, text="Server currently offline.\nTry connecting again later.", font=("Roboto", 40))
        self.failed_label.pack(pady=5)

if __name__ == "__main__":
    try:
        # with open the socket so that it closes if any bug occurs.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', 12345))
            user_profile = None
            handle_encryption = EncryptionHandler(client_socket)
            app = App()
            app.mainloop()
    except ConnectionRefusedError:
        # In this case the server is not active.
        print("Connection refused")
        failed_load_app = FailedToload()
        failed_load_app.mainloop()
