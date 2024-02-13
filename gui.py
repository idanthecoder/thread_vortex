import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Thread Vortex")
window.geometry("800x600")

# Create a frame for the header
header_frame = tk.Frame(window, bg="#222222", height=50)
header_frame.pack(fill=tk.X)

# Create a label for the site name
site_name_label = tk.Label(header_frame, text="Thread Vortex", fg="white", font=("Arial", 24), bg="#222222")
site_name_label.place(x=350, y=5)

# Create a frame for the popular topics
popular_frame = tk.Frame(window, bg="#F5F5F5", height=500)
popular_frame.pack(side=tk.LEFT, fill=tk.Y)

# Add some popular topics
topics = ["Valheim", "Genshin Impact", "Minecraft", "Pokimane", "Halo Infinite", "Call of Duty: Warzone", "Path of Exile"]
for i, topic in enumerate(topics):
    topic_button = tk.Button(popular_frame, text=topic, font=("Arial", 18), bg="#DDDDDD", width=15, height=3, anchor="center")
    topic_button.place(x=20, y=50 + i * 60)

# Create a frame for the right side
right_frame = tk.Frame(window, bg="#F5F5F5", height=500)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Add some content to the right frame
content_label = tk.Label(right_frame, text="What name-brand item will you always buy?", font=("Arial", 18), bg="#F5F5F5")
content_label.place(x=20, y=20)

# Add some upvotes and comments
upvotes_label = tk.Label(right_frame, text="6.1K ↑", font=("Arial", 14), bg="#F5F5F5")
upvotes_label.place(x=520, y=20)
comments_label = tk.Label(right_frame, text="300 ➡", font=("Arial", 14), bg="#F5F5F5")
comments_label.place(x=620, y=20)

# Start the tkinter main loop
window.mainloop()