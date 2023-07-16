import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("system")  # Set light or dark mode
ctk.set_default_color_theme("green")  # Set the color theme

username = "user"
password = "123"

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
    homepage = ctk.CTk()  # Creating homepage window
   
    homepage.geometry("850x500")
    homepage.title('Homepage')
    homepage.maxsize(900, 600)
    homepage.configure(fg_color="#232635")

    #Homepage Frame

    #main frames  
    menu1_frame = ctk.CTkFrame(master=homepage, width=200, height=800, fg_color="transparent")
    menu1_frame.pack(side = "right", fill = "both", expand = True) #right of the page

    menu2_frame = ctk.CTkFrame(master=homepage, width=200, height=800,fg_color="transparent")
    menu2_frame.pack(side = "left", fill = "both", expand = True) #right of the page

    #frames inside the main frame 

    user_frame = ctk.CTkFrame(master=menu1_frame, width=200, height=800, corner_radius=20)
    user_frame.pack(padx = "10", pady = "20") #top of the page

    entry_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=250, corner_radius=20)
    entry_frame.pack(side= "top", padx = 10, pady = 20) #top of the page

    info_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=200, corner_radius=20)
    info_frame.pack(side = "bottom", padx = 10, pady = 20)  #bottom of the page

    #buttons inside entry_frame

    homepage.mainloop()

def signup_function():
    loginpage.destroy()  # Destroy current window and create a new one
    signup = ctk.CTk()  # Creating signup window
    signup.geometry("850x500")
    signup.title('Sign Up')

    # Signup widgets
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
