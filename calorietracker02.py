import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sqlite3

# Set customtkinter appearance mode and color theme
ctk.set_appearance_mode("system")  # Set light or dark mode
ctk.set_default_color_theme("green")  # Set the color theme

# Create or connect to the SQLite3 database
conn = sqlite3.connect('userinformation.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    age INTEGER,
                    current_weight REAL,
                    weight_goal REAL
                )''')
conn.commit()

# Global variables for user_entry and password_entry
user_entry = None
password_entry = None

class FoodPage(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.label = ctk.CTkLabel(self, text="Food Page")
        self.label.pack(padx=20, pady=20)

def login():
    global user_entry, password_entry
    written_username = user_entry.get()
    written_password = password_entry.get()
    
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (written_username, written_password))
    user_data = cursor.fetchone()
    
    if user_data:
        homescreen_function()
    else:
        messagebox.showwarning(title="Error", message="Invalid Username Or Password")

def homescreen_function():
    loginpage.destroy()  # Destroy current window and create a new one
    homepage = ctk.CTk()  # Creating homepage window
    homepage.geometry("1280x750")
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

    user_frame = ctk.CTkFrame(master=menu1_frame, width=200, height=800, corner_radius=20,border_width=2)
    user_frame.pack(padx = "10", pady = "20") #top of the page

    entry_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=250, corner_radius=20,border_width=2)
    entry_frame.pack(side= "top", padx = 10, pady = 20) #top of the page

    info_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=200, corner_radius=20,border_width=2)
    info_frame.pack(side = "bottom", padx = 10, pady = 20)  #bottom of the page

    #buttons inside entry_frame

    food_button = ctk.CTkButton(master= entry_frame, command=open_foodwindow)
    food_button.place(relx=0.5,rely=0.5,anchor="center")
    
    homepage.mainloop()

def open_foodwindow():
    global food_window
    if not food_window or not food_window.winfo_exists():
        food_window = FoodPage()
    else:
        food_window.focus()

def signup_function():
    global user_entry, password_entry
    loginpage.destroy()  # Destroy current window and create a new one
    signup = ctk.CTk()  # Creating signup window
    signup.geometry("850x500")
    signup.title('Sign Up')

    label = ctk.CTkLabel(master=signup, text="Sign Up Page", font=('Century Gothic', 60))
    label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    username_label = ctk.CTkLabel(master=signup, text="Username:", font=('Switzer', 14))
    username_label.place(relx=0.3, rely=0.3, anchor=tk.CENTER)
    username_entry = ctk.CTkEntry(master=signup, width=220, height=35, font=('Switzer', 14), fg_color="#e0dcdc", text_color="black")
    username_entry.place(relx=0.6, rely=0.3, anchor=tk.CENTER)

    password_label = ctk.CTkLabel(master=signup, text="Password:", font=('Switzer', 14))
    password_label.place(relx=0.3, rely=0.4, anchor=tk.CENTER)
    password_entry = ctk.CTkEntry(master=signup, width=220, height=35, font=('Switzer', 14), fg_color="#e0dcdc", text_color="black")
    password_entry.place(relx=0.6, rely=0.4, anchor=tk.CENTER)

    age_label = ctk.CTkLabel(master=signup, text="Age:", font=('Switzer', 14))
    age_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
    age_entry = ctk.CTkEntry(master=signup, width=220, height=35, font=('Switzer', 14), fg_color="#e0dcdc", text_color="black")
    age_entry.place(relx=0.6, rely=0.5, anchor=tk.CENTER)

    current_weight_label = ctk.CTkLabel(master=signup, text="Current Weight:", font=('Switzer', 14))
    current_weight_label.place(relx=0.3, rely=0.6, anchor=tk.CENTER)
    current_weight_entry = ctk.CTkEntry(master=signup, width=220, height=35, font=('Switzer', 14), fg_color="#e0dcdc", text_color="black")
    current_weight_entry.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

    weight_goal_label = ctk.CTkLabel(master=signup, text="Weight Goal:", font=('Switzer', 14))
    weight_goal_label.place(relx=0.3, rely=0.7, anchor=tk.CENTER)
    weight_goal_entry = ctk.CTkEntry(master=signup, width=220, height=35, font=('Switzer', 14), fg_color="#e0dcdc", text_color="black")
    weight_goal_entry.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

    def save_signup():
        # Save the signup data to the database
        username = username_entry.get()
        password = password_entry.get()
        age = age_entry.get()
        current_weight = current_weight_entry.get()
        weight_goal = weight_goal_entry.get()

        cursor.execute("INSERT INTO users (username, password, age, current_weight, weight_goal) VALUES (?, ?, ?, ?, ?)",
                       (username, password, age, current_weight, weight_goal))
        conn.commit()

        # Close the signup window and go back to the login page
        signup.destroy()
        create_loginpage()

    save_button = ctk.CTkButton(master=signup, text="Sign Up", command=save_signup,
                                corner_radius=6, fg_color="#FFC300", font=('Switzer', 12, 'bold'))
    save_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    signup.mainloop()
    pass

def create_loginpage():
    global loginpage, user_entry, password_entry
    loginpage = ctk.CTk()  # Creating ctk window
    loginpage.geometry("750x500")
    loginpage.title("Login")
    loginpage.maxsize(900, 600)
    loginpage.configure(fg_color="#232635")

    # Login Frame
    frame = ctk.CTkFrame(master=loginpage, corner_radius=20, fg_color="#232635")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Labels
    label1 = ctk.CTkLabel(master=frame, text="Welcome To The Best", font=('Switzer', 28, 'bold'))
    label1.place(relx=0.5, rely=0.26, anchor=tk.CENTER)

    label2 = ctk.CTkLabel(master=frame, text="Calorie Tracker", font=('Switzer', 42, 'bold'))
    label2.place(relx=0.5, rely=0.34, anchor=tk.CENTER)

    # Info Entry 
    user_entry = ctk.CTkEntry(master=frame, width=220, height=35, placeholder_text='Username or Email',
                              font=('Switzer', 16), fg_color="#e0dcdc", text_color="black") 
    user_entry.place(relx=0.5, rely=0.46, anchor=tk.CENTER) # Username entry

    password_entry = ctk.CTkEntry(master=frame, width=220, height=35, placeholder_text='Password',
                                  show="⚫", font=("Switzer", 16), fg_color="#e0dcdc", text_color="black")
    password_entry.place(relx=0.5, rely=0.54, anchor=tk.CENTER) # Password entry

    # Buttons
    login_button = ctk.CTkButton(master=frame, width=220, height=35, text="Login", command=login,
                                 corner_radius=6, fg_color="#FFC300", border_spacing=10,
                                 font=('Switzer', 18, 'bold'))
    login_button.place(relx=0.5, rely=0.63, anchor=tk.CENTER) # Login button

    signup_button = ctk.CTkButton(master=frame, width=220, text="Sign Up For Free", command=signup_function,
                                  corner_radius=6, fg_color="transparent", font=('Switzer', 12, 'bold'))
    signup_button.place(relx=0.5, rely=0.72, anchor=tk.CENTER) # Signup Button
 
    loginpage.mainloop()

# Create Login page
create_loginpage()

# Close the database connection when the program exits
conn.close()