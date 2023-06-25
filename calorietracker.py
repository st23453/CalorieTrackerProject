import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("system")  # Set light or dark mode
ctk.set_default_color_theme("green")  # Set the color theme

username = "monkey"
password = "lol123"

def login():
    written_username = user_entry.get()
    written_password = password_entry.get()

    if written_username == username and written_password == password:
        homescreen_function()
    else:
        messagebox.showwarning(title="Error", message="Invalid Username Or Password")

def homescreen_function():
    loginpage.destroy()  # Destroy current window and create a new one
    homepage = ctk.CTk()  # Creating homepage window
    homepage.geometry("1280x750")
    homepage.title('Homepage')

    # Homescreen widgets
    

    homepage.mainloop()

def signup_function():
    loginpage.destroy()  # Destroy current window and create a new one
    signup = ctk.CTk()  # Creating signup window
    signup.geometry("1280x750")
    signup.title('Sign Up')

    # Homescreen widgets
    label = ctk.CTkLabel(master=signup, text="Sign Up Page", font=('Century Gothic', 60))
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    signup.mainloop()

loginpage = ctk.CTk()  # Creating ctk window
loginpage.geometry("750x500")
loginpage.title("Login")
loginpage.maxsize(900, 600)
loginpage.configure(fg_color="#232635")

frame = ctk.CTkFrame(master=loginpage, corner_radius=20, fg_color="#232635")
frame.pack(pady=20, padx=20, fill="both", expand=True)

label1 = ctk.CTkLabel(master=frame, text="Welcome To The Best", font=('Switzer', 28, 'bold'))
label1.place(relx=0.5, rely=0.26, anchor=tk.CENTER)

label2 = ctk.CTkLabel(master=frame, text="Calorie Tracker", font=('Switzer', 42, 'bold'))
label2.place(relx=0.5, rely=0.34, anchor=tk.CENTER)

user_entry = ctk.CTkEntry(master=frame, width=220, height=35, placeholder_text='Username or Email',
                          font=('Switzer', 16), fg_color="#e0dcdc", text_color="black")
user_entry.place(relx=0.5, rely=0.46, anchor=tk.CENTER)

password_entry = ctk.CTkEntry(master=frame, width=220, height=35, placeholder_text='Password',
                              show="⚫", font=("Switzer", 16), fg_color="#e0dcdc", text_color="black")
password_entry.place(relx=0.5, rely=0.54, anchor=tk.CENTER)

login_button = ctk.CTkButton(master=frame, width=220, height=35, text="Login", command=login,
                             corner_radius=6, fg_color="#FFC300", border_spacing=10,
                             font=('Switzer', 18, 'bold'))
login_button.place(relx=0.5, rely=0.63, anchor=tk.CENTER)

signup_button = ctk.CTkButton(master=frame, width=220, text="Sign Up For Free", command=signup_function,
                              corner_radius=6, fg_color="transparent", font=('Switzer', 12, 'bold'))
signup_button.place(relx=0.5, rely=0.72, anchor=tk.CENTER)

loginpage.mainloop()
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("system")  # Set light or dark mode
ctk.set_default_color_theme("green")  # Set the color theme

username = "monkey"
password = "lol123"

def login():
    written_username = user_entry.get()
    written_password = password_entry.get()

    if written_username == username and written_password == password:
        homescreen_function()
    else:
        messagebox.showwarning(title="Error", message="Incorrect username or password")

def homescreen_function():
    loginpage.destroy()  # Destroy current window and create a new one
    homepage = ctk.CTk()  # Creating homepage window
    homepage.geometry("1280x750")
    homepage.title('Homepage')

    def button_pressed():
        print("Button pressed")

    # Homescreen widgets
    label = ctk.CTkLabel(master=homepage, text="Home Page", font=('Century Gothic', 60))
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    button = ctk.CTkButton(master=homepage, text="Monkey", command=button_pressed)
    button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    homepage.mainloop()

def signup_function():
    loginpage.destroy()  # Destroy current window and create a new one
    signup = ctk.CTk()  # Creating signup window
    signup.geometry("1280x750")
    signup.title('Sign Up')

    # Homescreen widgets
    label = ctk.CTkLabel(master=signup, text="Sign Up Page", font=('Century Gothic', 60))
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    signup.mainloop()

loginpage = ctk.CTk()  # Creating ctk window
loginpage.geometry("750x500")
loginpage.title("Login")
loginpage.maxsize(900, 600)
loginpage.configure(fg_color="#232635")

frame = ctk.CTkFrame(master=loginpage, corner_radius=20, fg_color="#232635")
frame.pack(pady=20, padx=20, fill="both", expand=True)

label1 = ctk.CTkLabel(master=frame, text="Welcome To The Best", font=('Switzer', 28, 'bold'))
label1.place(relx=0.5, rely=0.26, anchor=tk.CENTER)

label2 = ctk.CTkLabel(master=frame, text="Calorie Tracker", font=('Switzer', 42, 'bold'))
label2.place(relx=0.5, rely=0.34, anchor=tk.CENTER)

user_entry = ctk.CTkEntry(master=frame, width=220, height=35, placeholder_text='Username or Email',
                          font=('Switzer', 16), fg_color="#e0dcdc", text_color="black")
user_entry.place(relx=0.5, rely=0.46, anchor=tk.CENTER)

password_entry = ctk.CTkEntry(master=frame, width=220, height=35, placeholder_text='Password',
                              show="⚫", font=("Switzer", 16), fg_color="#e0dcdc", text_color="black")
password_entry.place(relx=0.5, rely=0.54, anchor=tk.CENTER)

login_button = ctk.CTkButton(master=frame, width=220, height=35, text="Login", command=login,
                             corner_radius=6, fg_color="#FFC300", border_spacing=10,
                             font=('Switzer', 18, 'bold'))
login_button.place(relx=0.5, rely=0.63, anchor=tk.CENTER)

signup_button = ctk.CTkButton(master=frame, width=220, text="Sign Up For Free", command=signup_function,
                              corner_radius=6, fg_color="transparent", font=('Switzer', 12, 'bold'))
signup_button.place(relx=0.5, rely=0.72, anchor=tk.CENTER)

loginpage.mainloop()