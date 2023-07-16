import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("system")  # Set light or dark mode
ctk.set_default_color_theme("green")  # Set the color theme

username = "user"
password = "123"

def login():
    new_username = "username_entry.get"()
    new_password = "password_entry.get"()
    if new_username == username and new_password == password:
        homescreen_function()
    else:
        messagebox.showwarning(title="Error", message="Invalid Username Or Password")

def homescreen_function():
    homepage = ctk.CTk()  # Creating homepage window
    homepage.geometry("850x500")
    homepage.title('Homepage')
    homepage.maxsize(900, 600)
    homepage.configure(fg_color="#232635")

    # Homepage widgets
    label = ctk.CTkLabel(master=homepage, text="Welcome to Calorie Tracker", font=('Century Gothic', 24))
    label.pack(pady=20)

    # Additional widgets and functionality for the homepage
    # ...

    homepage.mainloop()

def signup_function():
    def signup():
        new_username = username_entry.get()
        new_password = password_entry.get()
        new_age = age_entry.get()
        new_weight = weight_entry.get()

        # Save the user information or perform any required actions
        # Here, I'm just displaying the entered values as an example
        messagebox.showinfo(title="Signup Successful",
                            message=f"Username: {new_username}\n"
                                    f"Password: {new_password}\n"
                                    f"Age: {new_age}\n"
                                    f"Weight: {new_weight}")

        signup_page.destroy()
        login_page.deiconify()

    def show_signup_page():
        login_page.withdraw()  # Hide the login page
        signup_page.deiconify()  # Show the signup page

    def show_login_page():
        signup_page.withdraw()  # Hide the signup page
        login_page.deiconify()  # Show the login page

    login_page = ctk.CTk()  # Creating login window
    login_page.geometry("400x300")
    login_page.title('Login')

    # Login widgets
    label1 = ctk.CTkLabel(master=login_page, text="Username:")
    label1.pack()
    user_entry = ctk.CTkEntry(master=login_page, width=220, height=35, placeholder_text='Username',
                              font=('Switzer', 16), fg_color="#e0dcdc", text_color="black")
    user_entry.pack()

    label2 = ctk.CTkLabel(master=login_page, text="Password:")
    label2.pack()
    password_entry = ctk.CTkEntry(master=login_page, width=220, height=35, placeholder_text='Password',
                                  show="⚫", font=('Switzer', 16), fg_color="#e0dcdc", text_color="black")
    password_entry.pack()

    login_button = ctk.CTkButton(master=login_page, width=220, height=35, text="Login", command=login,
                                 corner_radius=6, fg_color="#FFC300", border_spacing=10,
                                 font=('Switzer', 18, 'bold'))
    login_button.pack(pady=10)

    signup_button = ctk.CTkButton(master=login_page, width=220, text="Sign Up", command=show_signup_page,
                                  corner_radius=6, fg_color="transparent", font=('Switzer', 12, 'bold'))
    signup_button.pack()

    signup_page = ctk.CTk()  # Creating signup window
    signup_page.geometry("400x300")
    signup_page.title('Signup')

    # Signup widgets
    label3 = ctk.CTkLabel(master=signup_page, text="Username:")
    label3.pack()
    username_entry = ctk.CTkEntry(master=signup_page, width=220, height=35, placeholder_text='Username',
                                  font=('Switzer', 16), fg_color="#e0dcdc", text_color="black")
    username_entry.pack()

    label4 = ctk.CTkLabel(master=signup_page, text="Password:")
    label4.pack()
    password_entry = ctk.CTkEntry(master=signup_page, width=220, height=35, placeholder_text='Password',
                                  show="⚫", font=('Switzer', 16), fg_color="#e0dcdc", text_color="black")
    password_entry.pack()

    label5 = ctk.CTkLabel(master=signup_page, text="Age:")
    label5.pack()
    age_entry = ctk.CTkEntry(master=signup_page, width=220, height=35, placeholder_text='Age',
                             font=('Switzer', 16), fg_color="#e0dcdc", text_color="black")
    age_entry.pack()

    label6 = ctk.CTkLabel(master=signup_page, text="Weight:")
    label6.pack()
    weight_entry = ctk.CTkEntry(master=signup_page, width=220, height=35, placeholder_text='Weight',
                                font=('Switzer', 16), fg_color="#e0dcdc", text_color="black")
    weight_entry.pack()

    signup_button = ctk.CTkButton(master=signup_page, width=220, text="Sign Up", command=signup,
                                  corner_radius=6, fg_color="#FFC300", border_spacing=10,
                                  font=('Switzer', 18, 'bold'))
    signup_button.pack(pady=10)

    back_button = ctk.CTkButton(master=signup_page, width=220, text="Back", command=show_login_page,
                                corner_radius=6, fg_color="transparent", font=('Switzer', 12, 'bold'))
    back_button.pack()

    signup_page.withdraw()  # Hide the signup page initially

    login_page.mainloop()

signup_function()
