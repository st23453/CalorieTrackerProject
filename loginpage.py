import tkinter as tk
import customtkinter
from PIL import ImageTk

customtkinter.set_appearance_mode("system")  # Set light or dark mode
customtkinter.set_default_color_theme("dark-blue")  # Set the color theme

app = customtkinter.CTk()  # Creating customtkinter window
app.geometry("750x500")
app.title("Login")
app.maxsize(900, 600)

def login_function():
    app.destroy()  # Destroy current window and create a new one
    w = customtkinter.CTk()  
    w.geometry("1280x750")
    w.title('Homepage')
    label = customtkinter.CTkLabel(master=w, text="Home Page", font=('Century Gothic',60))
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    w.mainloop()


label1 = customtkinter.CTkLabel(master=app, text="Welcome to", font=('Switzer', 28, 'bold'))
label1.place(relx=0.5, rely=0.24, anchor=tk.CENTER)

label2 = customtkinter.CTkLabel(master=app, text="Calorie Tracker", font=('Switzer', 42, 'bold'))
label2.place(relx=0.5, rely=0.32, anchor=tk.CENTER)

user_entry = customtkinter.CTkEntry(master=app, width=220, placeholder_text='Username or Email', font=('Switzer',16))
user_entry.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

password_entry = customtkinter.CTkEntry(master=app, width=220, placeholder_text='Password', show="⚫", font=("Switzer", 16))
password_entry.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

login_button = customtkinter.CTkButton(master=app, width=220, text="Login", command=login_function, corner_radius=6, fg_color= "#FFC300", font=('Switzer', 16, 'bold'))
login_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

app.mainloop()
