import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
import customtkinter as ctk
import sqlite3
import bcrypt

# Set customtkinter appearance mode and color theme
ctk.set_appearance_mode("system")  # Set light or dark mode
ctk.set_default_color_theme("green")  # Set the color theme

# Create or connect to the SQLite3 database
conn = sqlite3.connect('projectcalorietracker.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    age INTEGER,
                    current_weight REAL,
                    weight_goal TEXT
                )''')
conn.commit()


# Global variable for the pages
loginpage = None
homepage = None
foodpage = None

# Global variables for user_entry and password_entry
user_entry = None
password_entry = None

# Global variable for user_data
user_data = None

# Global variables to store calorie information
calories_consumed = 0
info_label = None



def calculate_calorie_intake(weight_goal, current_weight):
    try:
        current_weight = float(current_weight)
    except ValueError:
        # Handle the case where current_weight is not a valid number
        return 0
    
    if weight_goal == "Lose Weight":
        return int(current_weight * 30) - 300
    elif weight_goal == "Gain Weight":
        return int(current_weight * 30) + 300
    elif weight_goal == "Maintain Weight":
        return int(current_weight * 30)
    
    # Function to update the info_label text with the updated total calories
def update_info_label():
    global calories_consumed, info_label
    calorie_intake = calculate_calorie_intake(user_data[5], user_data[4])
    total_calories = calorie_intake + calories_consumed
    
    # Check if the info_label exists before configuring it
    if info_label:
        info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Consumed: {total_calories} calories")

def create_info_label():
    global user_data, info_label

    # Calculate the recommended calorie intake based on the user's weight and weight goal
    calorie_intake = calculate_calorie_intake(user_data[5], user_data[4])

    info_label = ctk.CTkLabel(master=info_frame, font=("Switzer", 14), anchor=tk.W)
    info_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    info_label.configure(text=f"Base Goal: {calorie_intake} calories")
 


def login():
    global user_data, user_entry, password_entry

    written_username = user_entry.get()
    written_password = password_entry.get()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (written_username, written_password))
    user_data = cursor.fetchone()
    
    if user_data:
        return user_data
    else:
        messagebox.showwarning(title="Error", message="Invalid Username Or Password")
        return None

def food_function():
    global calories_consumed, info_label, info_frame

    if homepage:
        homepage.destroy()
    
    print("Creating foodpage...")
    foodpage = ctk.CTk()
    foodpage.geometry("800x450")
    foodpage.title('Food Page')
    foodpage.maxsize(900, 600)
    foodpage.configure(fg_color="#232635")

    print("Inside food_function")
    print("homepage:", homepage)


    update_info_label()

    # Entry
    def on_calorie_entry_change(*args):
        global calories_consumed
        try:
            calories_consumed = sum(int(calorie.get()) for calorie in calorie_entries)
        except ValueError:
            pass
        update_info_label()

    # Create StringVar and associate it with the CTkEntry widget
    calorie_var = tk.StringVar()
    calorie1_entry = ctk.CTkEntry(master=entry2_frame, width=220, height=35, font=('Switzer', 14), fg_color="#e0dcdc", text_color="black", textvariable=calorie_var)
    calorie1_entry.place(relx=0.75, rely=0.4, anchor=tk.CENTER)



    # Create a list to store calorie entries for recalculation
    calorie_entries = []

    # Function to handle enter_button click event
    def on_enter_button_click():
        global calories_consumed
        try:
            # Get the calorie entry and add it to calories_consumed
            calories_consumed += int(calorie1_entry.get())
            # Update info_label on both pages
            update_info_label()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid calorie amount.")
        # Save the calorie entry in the database (You can add your database saving code here)

    # Register the on_calorie_entry_change function with the StringVar
    calorie_var.trace_add("write", on_calorie_entry_change)


    # Main Frames  

    main1_frame = ctk.CTkFrame(master=foodpage, width=200, height=800, fg_color="transparent")
    main1_frame.pack(side = "left", fill = "both", expand = True) #right of the page

    menu2_frame = ctk.CTkFrame(master=foodpage, width=200, height=800,fg_color="transparent")
    menu2_frame.pack(side = "right", fill = "both", expand = True) #right of the page

    # Frames Inside the main frames

    progression_frame = ctk.CTkFrame(master=main1_frame, width=200, height=800, corner_radius=20,border_width=2)
    progression_frame.pack(padx = "10", pady = "20") #top of the page

    entry2_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=250, corner_radius=20,border_width=2)
    entry2_frame.pack(side= "top", padx = 10, pady = 15) #top of the page

    info_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=200, corner_radius=20,border_width=2)
    info_frame.pack(side = "bottom", padx = 10, pady = 20)  #bottom of the page

    # Label

    foodname_label = ctk.CTkLabel(master=entry2_frame,text="Enter Name Of Food:")
    foodname_label.place(relx=0.3, rely=0.15)


    calorie1_label = ctk.CTkLabel(master=entry2_frame,text="Enter Amount Of Calories")
    calorie1_label.place(relx=0.3, rely=0.35)


    serving1_label = ctk.CTkLabel(master=entry2_frame,text="Serving:", )
    serving1_label.place(relx=0.3, rely=0.55)

    # Entry

    foodname_entry = ctk.CTkEntry(master= entry2_frame, width=220, height=35, font=('Switzer', 14))
    foodname_entry.place(relx=0.75, rely=0.2, anchor=tk.CENTER)

    calorie1_entry = ctk.CTkEntry(master= entry2_frame, width=220, height=35, font=('Switzer', 14))
    calorie1_entry.place(relx=0.75, rely=0.4, anchor=tk.CENTER)

    serving1_entry = ctk.CTkEntry(master= entry2_frame, width=220, height=35, font=('Switzer', 14))
    serving1_entry.place(relx=0.75, rely=0.6, anchor=tk.CENTER)

    # Buttons

    enter_button = ctk.CTkButton(master=entry2_frame, text="Enter", command=on_enter_button_click,
                                 corner_radius=6, fg_color="#FFC300", font=('Switzer', 14, 'bold'))
    enter_button.place(relx=0.75, rely=0.8, anchor=tk.CENTER)

    # Associate on_calorie_entry_change with the entry
    calorie1_entry.trace_add("write", on_calorie_entry_change)

    create_info_label()


    foodpage.mainloop()
  


def homescreen_function():
    global user_data, homepage, info_label, info_frame


    loginpage.destroy()   # Destroy current windFow and create a new one
    
    homepage = ctk.CTk()
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

    entry1_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=250, corner_radius=20,border_width=2)
    entry1_frame.pack(side= "top", padx = 10, pady = 20) #top of the page

    info_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=200, corner_radius=20,border_width=2)
    info_frame.pack(side = "bottom", padx = 10, pady = 20)  #bottom of the page

    # inside info_frame
    
    # Display user information in the info_frame
    info_label = ctk.CTkLabel(master=info_frame, font=("Switzer", 14), anchor=tk.W)
    info_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Calculate the recommended calorie intake based on the user's weight and weight goal
    calorie_intake = calculate_calorie_intake(user_data[5], user_data[4])
    info_label.configure(text=f"Base Goal: {calorie_intake} calories")

    #buttons inside entry_frame

    food_button = ctk.CTkButton(master= entry1_frame, text="Food", command=food_function)
    food_button.place(relx=0.2,rely=0.5,anchor="center")
    
    homepage.mainloop()



def signup_function():
    global loginpage, user_entry, password_entry

    def go_back():
        signup.destroy()
        create_loginpage()



    loginpage.destroy()  # Destroy current window and create a new one
    
    signup = ctk.CTk()  # Creating signup window
    signup.geometry("850x500")
    signup.title('Sign Up')

    # Back Button
    back_button = ctk.CTkButton(master=signup, width=100, text="Back", command=go_back,
                                corner_radius=6, fg_color="#f46b41", font=('Switzer', 12, 'bold'))
    back_button.place(relx=0.1, rely=0.9, anchor=tk.CENTER)  # Back Button


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

    # Customizing the OptionMenu appearance using ctk.CTkOptionMenu
    weight_goal_var = tk.StringVar()
    weight_goal_var.set("Select")
    weight_goal_options = ["Lose Weight", "Gain Weight", "Maintain Weight"]
    weight_goal_combobox = Combobox(master=signup, width=23, height=35, textvariable=weight_goal_var, values=weight_goal_options,
                                    font=('Switzer', 14), state="readonly")
    weight_goal_combobox.place(relx=0.6, rely=0.7, anchor=tk.CENTER)


    def save_signup(username, password, age, current_weight, weight_goal):

        global calorie_intake
        
        # Get the input values from the entries
        username = username_entry.get()
        password = password_entry.get()
        age = age_entry.get()
        current_weight = current_weight_entry.get()
        weight_goal = weight_goal_var.get()

        
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Store the hashed password in the database
        cursor.execute("INSERT INTO users (username, password, age, current_weight, weight_goal) VALUES (?, ?, ?, ?, ?)",
                    (username, hashed_password, age, current_weight, weight_goal))
        conn.commit()

        # Check if any required field is empty
        if not username or not password or not age or not current_weight or not weight_goal:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        # Check if age is an integer
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be an integer.")
            return

        # Check if current weight is a valid number
        try:
            current_weight = float(current_weight)
        except ValueError:
            messagebox.showerror("Error", "Current weight must be a number.")
            return
        
        # Check if weight goal is selected
        if weight_goal == "Select":
            messagebox.showwarning("Error", "Please select a weight goal.")
            return

        # Check if the username already exists in the database
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Error", "Username already taken. Please choose a different username.")
            return

        # Calculate the recommended calorie intake based on the weight goal and current weight
        calorie_intake = calculate_calorie_intake(weight_goal, current_weight)

        cursor.execute("INSERT INTO users (username, password, age, current_weight, weight_goal) VALUES (?, ?, ?, ?, ?)",
                    (username, password, age, current_weight, weight_goal))
        conn.commit()
        messagebox.showinfo("Success", "Signup successful! You can now log in.")
        go_back()  # Go back to the login page after successful signup

    save_button = ctk.CTkButton(master=signup, text="Sign Up", command=save_signup,
                                    corner_radius=6, fg_color="#FFC300", font=('Switzer', 12, 'bold'))
    save_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        
    # Associate validation functions with age and current_weight entries
    age_entry.configure(validate="key", validatecommand=(validate_age_input, "%S"))
    current_weight_entry.configure(validate="key", validatecommand=(validate_current_weight_input, "%S"))

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Store the hashed password in the database using a parameterized query
    cursor.execute("INSERT INTO users (username, password, age, current_weight, weight_goal) VALUES (?, ?, ?, ?, ?)",
                (username, hashed_password, age, current_weight, weight_goal))
    conn.commit()

    

    signup.mainloop()

    


def validate_age_input(char):
    return char.isdigit() or char == ""

def validate_current_weight_input(char):
    return char.isdigit() or char == "." or char == ""


def create_loginpage():
    global loginpage, user_entry, password_entry

    loginpage = ctk.CTk()
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
                                  show="●", font=("Switzer", 16), fg_color="#e0dcdc", text_color="black")
    password_entry.place(relx=0.5, rely=0.54, anchor=tk.CENTER) # Password entry

    # Buttons
    login_button = ctk.CTkButton(master=frame, width=220, height=35, text="Login", command=login,
                                 corner_radius=6, fg_color="#FFC300", border_spacing=10,
                                 font=('Switzer', 18, 'bold'))
    login_button.place(relx=0.5, rely=0.63, anchor=tk.CENTER) # Login button

    signup_button = ctk.CTkButton(master=frame, width=220, text="Sign Up For Free", command=signup_function,
                                  corner_radius=6, fg_color="transparent", font=('Switzer', 12, 'bold'))
    signup_button.place(relx=0.5, rely=0.72, anchor=tk.CENTER) # Signup Button

    
def on_login_button_click():
    global user_data, user_entry, password_entry

    # Get the input values from the entries
    username = user_entry.get()
    password = password_entry.get()

    # Call the login function to authenticate the user
    user_data = login(username, password)

    # If login is successful, proceed to the homescreen
    if user_data:
        homescreen_function(user_data)


    loginpage.mainloop()


# Create Login page
create_loginpage()


# Close the database connection when the program exits
conn.close()
