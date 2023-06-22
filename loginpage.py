import tkinter as tk
import customtkinter
from PIL import ImageTk

customtkinter.set_appearance_mode("system")  # Set light or dark mode
customtkinter.set_default_color_theme("dark-blue")  # Set the color theme

app = customtkinter.CTk()  # Creating customtkinter window
app.geometry("750x500")
app.title("Login")

def login_function():
    app.destroy()            # destroy current window and creating new one 
    w = customtkinter.CTk()  
    w.geometry("1280x720")
    w.title('Welcome')
    l1=customtkinter.CTkLabel(master=w, text="Home Page",font=('Century Gothic',60))
    l1.place(relx=0.5, rely=0.5,  anchor=tk.CENTER)
    w.mainloop()

user_entry = customtkinter.CTkEntry(master=app, width=220, placeholder_text='Username or Email')
user_entry.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

password_entry = customtkinter.CTkEntry(master=app, width=220, placeholder_text='Password', show="⚫")
password_entry.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

login_button = customtkinter.CTkButton(master=app, width=220, text="Login", command=login_function, corner_radius=6)
login_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

app.mainloop()
