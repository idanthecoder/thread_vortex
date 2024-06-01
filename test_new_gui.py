#import customtkinter as ctk
#from PIL import Image, ImageTk
#import os
#
##ctk.set_appearance_mode("dark")
##ctk.set_default_color_theme("dark-blue")
#
#app = ctk.CTk()
#app.geometry("700x450")
#app.title("Thread Vortex")
#
## Logo
#logo_icon_image = Image.open(fp=os.path.join("assets","Thread Vortex logo.png"))
#logo_icon = ctk.CTkImage(light_image=logo_icon_image, size=(150, 50))
#logo_label = ctk.CTkLabel(app, text="", image=logo_icon)
#logo_label.place(relx=0.05, rely=0.05)
#
##logo_image = Image.open(os.path.join("assets","Thread Vortex logo.png"))  # Replace with actual path to your logo
##logo_image = logo_image.resize((150, 50))  # Adjust size as needed
##logo_image = ImageTk.PhotoImage(logo_image)
##logo_label = ctk.CTkLabel(app, image=logo_image, text="")
##logo_label.image = logo_image  # Keep a reference to avoid garbage collection
##logo_label.place(relx=0.05, rely=0.05)
#
## Image & Caption
#earth_icon_image = Image.open(fp=os.path.join("assets","earth icon 1.png"))
#earth_icon = ctk.CTkImage(light_image=earth_icon_image, size=(250, 250))
#earth_label = ctk.CTkLabel(app, text="", image=earth_icon)
#earth_label.place(relx=0.15, rely=0.25)
#
##earth_image = Image.open(os.path.join("assets","earth icon 1.png"))  # Replace with actual path to your image
##earth_image = earth_image.resize((250, 250))
##earth_image = ImageTk.PhotoImage(earth_image)
##earth_label = ctk.CTkLabel(app, image=earth_image, text="")
##earth_label.image = earth_image
##earth_label.place(relx=0.15, rely=0.25)
#
#caption_label = ctk.CTkLabel(app, text="Connecting people around the world", font=("Arial", 20))
#caption_label.place(relx=0.1, rely=0.65)
#
## Buttons
#def login_button_clicked():
#    print("Login Button clicked!")
#
#def register_button_clicked():
#    print("Register Button clicked!")
#
#login_button = ctk.CTkButton(app, text="Log-in", command=login_button_clicked, width=150, height=40, corner_radius=10)
#login_button.place(relx=0.65, rely=0.25)
#
#register_button = ctk.CTkButton(app, text="Register", command=register_button_clicked, width=150, height=40, corner_radius=10, fg_color="#FF6347", hover_color="#FF9171")
#register_button.place(relx=0.65, rely=0.45)
#
## Chat Bubble Icon
#chat_bubble_icon_image = Image.open(fp=os.path.join("assets","conversation icon 1.png"))
#chat_bubble_icon = ctk.CTkImage(light_image=chat_bubble_icon_image, size=(100, 100))
#chat_bubble_label = ctk.CTkLabel(app, text="", image=chat_bubble_icon)
#chat_bubble_label.place(relx=0.65, rely=0.05)
#
##chat_bubble_image = Image.open(os.path.join("assets","conversation icon 1.png"))  # Replace with actual path to your chat bubble image
##chat_bubble_image = chat_bubble_image.resize((100, 100))
##chat_bubble_image = ImageTk.PhotoImage(chat_bubble_image)
##chat_bubble_label = ctk.CTkLabel(app, image=chat_bubble_image, text="")
##chat_bubble_label.image = chat_bubble_image
##chat_bubble_label.place(relx=0.65, rely=0.05)
#
#app.mainloop()


#-------------


#import customtkinter as ctk
#from PIL import Image, ImageTk
#import os
#
#
#app = ctk.CTk()
#app.geometry("700x450")
#app.title("Thread Vortex")
#
## Logo
#logo_icon_image = Image.open(fp=os.path.join("assets","Thread Vortex logo.png"))
#logo_icon = ctk.CTkImage(light_image=logo_icon_image, size=(150, 50))
#logo_label = ctk.CTkLabel(app, text="", image=logo_icon)
#logo_label.grid(row=0, column=0, padx=10, pady=10)
#
## Image & Caption
#earth_icon_image = Image.open(fp=os.path.join("assets","earth icon 1.png"))
#earth_icon = ctk.CTkImage(light_image=earth_icon_image, size=(250, 250))
#earth_label = ctk.CTkLabel(app, text="", image=earth_icon)
#earth_label.grid(row=1, column=0, padx=10, pady=10)
#
#caption_label = ctk.CTkLabel(app, text="Connecting people around the world", font=("Arial", 20))
#caption_label.grid(row=2, column=0, padx=10, pady=10)
#
## Buttons
#def login_button_clicked():
#    print("Login Button clicked!")
#
#def register_button_clicked():
#    print("Register Button clicked!")
#
#login_button = ctk.CTkButton(app, text="Log-in", command=login_button_clicked, width=150, height=40, corner_radius=10)
#login_button.grid(row=1, column=1, padx=10, pady=10)
#
#register_button = ctk.CTkButton(app, text="Register", command=register_button_clicked, width=150, height=40, corner_radius=10, fg_color="#FF6347", hover_color="#FF9171")
#register_button.grid(row=2, column=1, padx=10, pady=10)
#
## Chat Bubble Icon
#chat_bubble_icon_image = Image.open(fp=os.path.join("assets","conversation icon 1.png"))
#chat_bubble_icon = ctk.CTkImage(light_image=chat_bubble_icon_image, size=(100, 100))
#chat_bubble_label = ctk.CTkLabel(app, text="", image=chat_bubble_icon)
#chat_bubble_label.grid(row=0, column=1, padx=10, pady=10)
#
#app.mainloop()

#--------------

# light mode

import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os

#ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
#ctk.set_default_color_theme("green")  # Themes: "blue" (default), "green", "dark-blue"



print(f"{str(2).zfill(2)}:{str(5).zfill(2)}")



app = ctk.CTk()
app.geometry("800x600")
app.title("Thread Vortex")

# Top Frame
top_frame = ctk.CTkFrame(app, border_color="black", border_width=2)
top_frame.pack(side=tk.TOP, fill=tk.X, expand=True, padx=20, pady=20)

# Logo
logo_icon_image = Image.open(os.path.join("assets","Thread Vortex logo.png"))  # Replace with your logo path
logo_icon = ctk.CTkImage(light_image=logo_icon_image, size=(400, 246))
logo_label = ctk.CTkLabel(top_frame, image=logo_icon, text="")
logo_label.pack(pady=5)

credits_label = ctk.CTkLabel(top_frame, text="Created by Idan Barkin", font=("Roboto", 40))
credits_label.pack(pady=5)
# Left Frame
left_frame = ctk.CTkFrame(app, border_color="black", border_width=2)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

## Earth image
#earth_icon_image = Image.open(os.path.join("assets","earth icon 1.png"))  # Replace with your image path
#earth_icon = ctk.CTkImage(light_image=earth_icon_image, size=(250, 250))
#earth_label = ctk.CTkLabel(left_frame, image=earth_icon, text="")
#earth_label.pack(pady=20)

## Connecting people text
#connecting_label = ctk.CTkLabel(left_frame, text="Connecting people around the world", font=("Roboto", 16))
#connecting_label.pack(pady=10)

# Right Frame
right_frame = ctk.CTkFrame(app, border_color="black", border_width=2)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Chat icon
chat_icon_image = Image.open(os.path.join("assets","conversation icon 2.png"))  # Replace with your icon path
chat_photo = ctk.CTkImage(light_image=chat_icon_image, size=(100, 100))
chat_label = ctk.CTkLabel(left_frame, image=chat_photo, text="")
chat_label.pack(pady=20)

# Log-in button
def login_button_click():
    print("Log-in button clicked")  # Replace with your login action

login_button = ctk.CTkButton(left_frame, text="Log-in", command=login_button_click, width=120, height=32, font=("Roboto", 14))
login_button.pack(pady=10)

## New tag
#new_label = ctk.CTkLabel(right_frame, text="NEW", font=("Roboto", 16), fg_color="red", text_color="white")
#new_label.pack(pady=10)

new_icon_image = Image.open(os.path.join("assets","new icon 2.png"))  # Replace with your icon path
new_photo = ctk.CTkImage(light_image=new_icon_image, size=(100, 100))
new_label = ctk.CTkLabel(right_frame, image=new_photo, text="")
new_label.pack(pady=20)

# Register button
def register_button_click():
    print("Register button clicked")  # Replace with your register action

register_button = ctk.CTkButton(right_frame, text="Register", command=register_button_click, width=120, height=32, font=("Roboto", 14))
register_button.pack(pady=10)

app.mainloop()


# dark mode 

#import customtkinter as ctk
#import tkinter as tk
#from PIL import Image, ImageTk
#import os
#
#ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
#ctk.set_default_color_theme("green")  # Themes: "blue" (default), "green", "dark-blue"
#
#app = ctk.CTk()
#app.geometry("800x600")
#app.title("Thread Vortex")
#
## Logo
#logo_icon_image = Image.open(os.path.join("assets","Thread Vortex logo.png"))  # Replace with your logo path
#logo_icon = ctk.CTkImage(light_image=logo_icon_image, size=(400, 246))
#logo_label = ctk.CTkLabel(app, image=logo_icon, text="", fg_color="#EAF2F8")
#logo_label.pack(pady=20)
#
## Left Frame
#left_frame = ctk.CTkFrame(app, border_color="white", border_width=2)
#left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
#
### Earth image
##earth_icon_image = Image.open(os.path.join("assets","earth icon 1.png"))  # Replace with your image path
##earth_icon = ctk.CTkImage(light_image=earth_icon_image, size=(250, 250))
##earth_label = ctk.CTkLabel(left_frame, image=earth_icon, text="")
##earth_label.pack(pady=20)
#
### Connecting people text
##connecting_label = ctk.CTkLabel(left_frame, text="Connecting people around the world", font=("Roboto", 16))
##connecting_label.pack(pady=10)
#
## Right Frame
#right_frame = ctk.CTkFrame(app, border_color="white", border_width=2)
#right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
#
## Chat icon
#chat_icon_image = Image.open(os.path.join("assets","conversation icon 2.png"))  # Replace with your icon path
#chat_photo = ctk.CTkImage(light_image=chat_icon_image, size=(100, 100))
#chat_label = ctk.CTkLabel(left_frame, image=chat_photo, text="")
#chat_label.pack(pady=20)
#
## Log-in button
#def login_button_click():
#    print("Log-in button clicked")  # Replace with your login action
#
#login_button = ctk.CTkButton(left_frame, text="Log-in", command=login_button_click, width=120, height=32, font=("Roboto", 14))
#login_button.pack(pady=10)
#
### New tag
##new_label = ctk.CTkLabel(right_frame, text="NEW", font=("Roboto", 16), fg_color="red", text_color="white")
##new_label.pack(pady=10)
#
#new_icon_image = Image.open(os.path.join("assets","new icon 2.png"))  # Replace with your icon path
#new_photo = ctk.CTkImage(light_image=new_icon_image, size=(100, 100))
#new_label = ctk.CTkLabel(right_frame, image=new_photo, text="")
#new_label.pack(pady=20)
#
## Register button
#def register_button_click():
#    print("Register button clicked")  # Replace with your register action
#
#register_button = ctk.CTkButton(right_frame, text="Register", command=register_button_click, width=120, height=32, font=("Roboto", 14))
#register_button.pack(pady=10)
#
#app.mainloop()