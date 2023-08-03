import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
import customtkinter as ctk
import sqlite3
import datetime

# Set customtkinter appearance mode and color theme
ctk.set_appearance_mode("system")  # Set light or dark mode
ctk.set_default_color_theme("green")  # Set the color theme

def get_current_date():
    current_date = datetime.date.today()
    return current_date.strftime("%B %d, %Y")

# Create the database connection function
def get_database_connection():
    return sqlite3.connect('database2.db')

# Create or connect to the SQLite3 database
with get_database_connection() as conn:
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

    # Add a table for food entries
    cursor.execute('''CREATE TABLE IF NOT EXISTS food_entries (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    food_name TEXT NOT NULL,
                    calories REAL NOT NULL,
                    serving TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')
    conn.commit()

# Global variable

foodpage = None
homepage = None
loginpage = None
historypage = None
homepage_info_label = None
user_entry = None
password_entry = None
info_label = None
calorie_intake = 0

def calculate_calorie_intake(weight_goal, current_weight):
    if weight_goal == "Lose Weight":
        return int(current_weight * 30) - 300
    elif weight_goal == "Gain Weight":
        return int(current_weight * 30) + 300
    elif weight_goal == "Maintain Weight":
        return int(current_weight * 30)

def login():
    global user_entry, password_entry, user_data
    written_username = user_entry.get()
    written_password = password_entry.get()

    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (written_username, written_password))
        user_data = cursor.fetchone()

    if user_data:
        homescreen_function()
    else:
        messagebox.showwarning(title="Error", message="Invalid Username Or Password")

def calculate_total_calories():
    global user_data

    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(calories) FROM food_entries WHERE user_id=?", (user_data[0],))
        total_calories = cursor.fetchone()

    return total_calories[0] if total_calories[0] else 0

def update_calories():
    total_calories = calculate_total_calories()
    current_date = get_current_date()
    info_label.configure(text=f"Today's date: {current_date}\nBase Goal: {calorie_intake} calories\nTotal Calories: {total_calories} calories")
    homepage_info_label.configure(text=f"Today's date: {current_date}\nBase Goal: {calorie_intake} calories\nTotal Calories: {total_calories} calories")


def historypage_function():
    global historypage, homepage, user_data

    if homepage:
        homepage.withdraw()

    historypage = ctk.CTk()
    historypage.geometry("800x450")
    historypage.title('History Page')
    historypage.maxsize(900, 600)
    historypage.configure(fg_color="#232635")

    historypage.mainloop()
####################################################################################################################################

def foodto_homepage():
    global foodpage, homepage
    if foodpage:
        foodpage.destroy()

    if homepage:  # If homepage is hidden, show it again
        homepage.deiconify()

def save_food_entry(food_name, calories, serving):
    global user_data

    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO food_entries (user_id, food_name, calories, serving) VALUES (?, ?, ?, ?)",
                       (user_data[0], food_name, calories, serving))
        conn.commit()

    update_calories()

def foodpage_function():
    global foodpage, homepage, homepage_info_label

    if homepage:
        homepage.withdraw()  # Hide the homepage

    foodpage = ctk.CTk()
    foodpage.geometry("800x450")
    foodpage.title('Food Page')
    foodpage.maxsize(900, 600)
    foodpage.configure(fg_color="#232635")
    

    # Main Frames  

    main1_frame = ctk.CTkFrame(master=foodpage, width=200, height=800, fg_color="transparent")
    main1_frame.pack(side = "left", fill = "both", expand = True) #left of the page

    menu2_frame = ctk.CTkFrame(master=foodpage, width=200, height=800,fg_color="transparent")
    menu2_frame.pack(side = "right", fill = "both", expand = True) #right of the page

    # Frames Inside the main frames

    progression_frame = ctk.CTkFrame(master=main1_frame, width=200, height=800, corner_radius=20,border_width=2)
    progression_frame.pack(padx = "10", pady = "20") #top of the page

    entry_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=250, corner_radius=20,border_width=2)
    entry_frame.pack(side= "top", padx = 10, pady = 15) #top of the page

    info_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=200, corner_radius=20,border_width=2)
    info_frame.pack(side = "bottom", padx = 10, pady = 20)  #bottom of the page

    # Widgets inside entry_frame
    
    # Label

    foodname_label = ctk.CTkLabel(master=entry_frame,text="Enter Name Of Food:")
    foodname_label.place(relx=0.3, rely=0.15)


    calorie1_label = ctk.CTkLabel(master=entry_frame,text="Enter Amount Of Calories")
    calorie1_label.place(relx=0.3, rely=0.35)


    serving1_label = ctk.CTkLabel(master=entry_frame,text="Serving:", )
    serving1_label.place(relx=0.3, rely=0.55)

    # Entry

    foodname_entry = ctk.CTkEntry(master= entry_frame, width=220, height=35, font=('Switzer', 14))
    foodname_entry.place(relx=0.75, rely=0.2, anchor=tk.CENTER)

    calorie1_entry = ctk.CTkEntry(master= entry_frame, width=220, height=35, font=('Switzer', 14))
    calorie1_entry.place(relx=0.75, rely=0.4, anchor=tk.CENTER)

    serving1_entry = ctk.CTkEntry(master= entry_frame, width=220, height=35, font=('Switzer', 14))
    serving1_entry.place(relx=0.75, rely=0.6, anchor=tk.CENTER)

    # Buttons

    enter_button = ctk.CTkButton(master=entry_frame, text="Enter",
                                corner_radius=6, fg_color="#FFC300", font=('Switzer', 14, 'bold'))
    enter_button.place(relx=0.75, rely=0.8, anchor=tk.CENTER)

#-----------------------------------------------------------------------------------------------------

    # Back button to return to homepage
    back_button = ctk.CTkButton(master=progression_frame, text="Back", command=foodto_homepage,
                                corner_radius=6, fg_color="#f46b41", font=('Switzer', 12, 'bold'))
    back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def save_entry():
        food_name = foodname_entry.get()
        calories = calorie1_entry.get()
        serving = serving1_entry.get()

        # Check if any required field is empty
        if not food_name or not calories or not serving:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        # Check if calories is a valid number
        try:
            calories = float(calories)
        except ValueError:
            messagebox.showerror("Error", "Calories must be a number.")
            return

        # Save the food entry to the database
        save_food_entry(food_name, calories, serving)
        update_calories()

        # Clear the entry fields after saving
        foodname_entry.delete(0, tk.END)
        calorie1_entry.delete(0, tk.END)
        serving1_entry.delete(0, tk.END)

#-----------------------------------------------------------------------------------------------------

         # Display the updated total calories in the info_frame
        total_calories = calculate_total_calories()
        info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Calories: {total_calories} calories")

        # Display the updated total calories in the homepage info_frame as well
        homepage_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Calories: {total_calories} calories")

    enter_button.configure(command=save_entry)

#-----------------------------------------------------------------------------------------------------

    # Create a label to display calorie information in the info_frame
    global info_label
    info_label = ctk.CTkLabel(master=info_frame, font=("Switzer", 14), anchor=tk.W)
    info_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Update the calorie information when the food page is created
    total_calories = calculate_total_calories()
    info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Calories: {total_calories} calories")

    # Update the info_label to refer to the global homepage_info_label
    info_label = homepage_info_label

    # Create a label to display the date in the info_frame
    date_label = ctk.CTkLabel(master=info_frame, font=("Switzer", 12), anchor=tk.W)
    date_label.place(relx=0.1, rely=0.2, anchor=tk.W)
    date_label.configure(text="Today's date:")

    # Create a label to display the actual date in big text
    date_value_label = ctk.CTkLabel(master=info_frame, font=("Switzer", 24), anchor=tk.W)
    date_value_label.place(relx=0.1, rely=0.4, anchor=tk.W)

    # Update the date label with the current date
    current_date = get_current_date()
    date_value_label.configure(text=current_date)

    foodpage.mainloop()

####################################################################################################################################

def homescreen_function():
    global user_data, homepage, info_label, calorie_intake, homepage_info_label

    def log_out():
        # Display a confirmation dialog box
        response = messagebox.askyesno("Confirmation", "Are you sure you want to log out?")

        if response:
            # If the user clicks "Yes," destroy the homepage window and create the login page again.
            homepage.destroy()
            create_loginpage()
        else:
            # If the user clicks "No," do nothing and remove the message.
            pass

    loginpage.destroy()  # Destroy current window and create a new one
    homepage = ctk.CTk()  # Creating homepage window
    homepage.geometry("1280x750")
    homepage.title('Homepage')
    homepage.maxsize(900, 600)
    homepage.configure(fg_color="#232635")

#-----------------------------------------------------------------------------------------------------

    #Homepage Frame

    #main frames  
    menu1_frame = ctk.CTkFrame(master=homepage, width=200, height=600, fg_color="transparent")
    menu1_frame.pack(side = "right", fill = "both", expand = True) #right of the page

    menu2_frame = ctk.CTkFrame(master=homepage, width=200, height=600,fg_color="transparent")
    menu2_frame.pack(side = "left", fill = "both", expand = True) #right of the page

    #frames inside the main frame 

    user_frame = ctk.CTkFrame(master=menu1_frame, width=200, height=600, corner_radius=20,border_width=2)
    user_frame.pack(padx = "10", pady = "20") #top of the page

    entry_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=250, corner_radius=20,border_width=2)
    entry_frame.pack(side= "top", padx = 10, pady = 20) #top of the page

    info_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=200, corner_radius=20,border_width=2)
    info_frame.pack(side = "bottom", padx = 10, pady = 20)  #bottom of the page

#-----------------------------------------------------------------------------------------------------

    # Inside info_frame

    # In the homescreen_function() add the following lines before entering the mainloop to update the homepage info_label
    homepage_info_label = ctk.CTkLabel(master=info_frame, font=("Switzer", 14), anchor=tk.W)
    homepage_info_label.place(relx=0.8, rely=0.3, anchor=tk.CENTER)
    homepage_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Calories: 0 calories")  # Initial value

    # Update the calorie information when the home page is created
    total_calories = calculate_total_calories()
    homepage_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Calories: {total_calories} calories")

    # Update the info_label to refer to the global homepage_info_label
    info_label = homepage_info_label

    # Calculate the recommended calorie intake based on the user's weight and weight goal
    calorie_intake = calculate_calorie_intake(user_data[5], user_data[4])
    info_label.configure(text=f"Base Goal: {calorie_intake} calories")

    # Create a label to display the date in the info_frame
    date_label = ctk.CTkLabel(master=info_frame, font=("Switzer", 12), anchor=tk.CENTER)
    date_label.place(relx=0.3, rely=0.4, anchor=tk.CENTER)
    date_label.configure(text="Today's date:")

    # Create a label to display the actual date in big text
    date_value_label = ctk.CTkLabel(master=info_frame, font=("Switzer", 24), anchor=tk.CENTER)
    date_value_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

    # Update the date label with the current date
    current_date = get_current_date()
    date_value_label.configure(text=current_date)

#-----------------------------------------------------------------------------------------------------

    # Inside entry_frame

    food_button = ctk.CTkButton(master= entry_frame, text="Food", command=foodpage_function)
    food_button.place(relx=0.2,rely=0.5,anchor="center")

    #buttons inside the user_frame

    # Create the log out button on the homepage
    logout_button = ctk.CTkButton(master=user_frame, text="Log Out", command=log_out,
                                  corner_radius=6, fg_color="#f46b41", font=('Switzer', 12, 'bold'))
    logout_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    history_button = ctk.CTkButton(master=user_frame, text="History", command=historypage_function,
                                  corner_radius=6, fg_color="#282434", font=('Switzer', 12, 'bold'))
    history_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)


    homepage.mainloop()

def signup_function():
    global user_entry, password_entry

    def go_back():
        signup.destroy()
        create_loginpage()

####################################################################################################################################


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

    def save_signup():
        # Get the input values from the entries
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        age = age_entry.get().strip()
        current_weight = current_weight_entry.get().strip()
        weight_goal = weight_goal_var.get()



        # Check if any required field is empty or contains only whitespace
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
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            return

        # Calculate the recommended calorie intake based on the weight goal and current weight
        calorie_intake = calculate_calorie_intake(weight_goal, current_weight)

        # Insert the new user into the database
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, age, current_weight, weight_goal) VALUES (?, ?, ?, ?, ?)",
                        (username, password, age, current_weight, weight_goal))
            conn.commit()

        # Show a success message
        messagebox.showinfo("Success", "Account created successfully!")

        # Optionally, you can navigate the user back to the login page after successful signup
        go_back()

    save_button = ctk.CTkButton(master=signup, text="Sign Up", command=save_signup,
                                corner_radius=6, fg_color="#FFC300", font=('Switzer', 12, 'bold'))
    save_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    
    # Associate validation functions with age and current_weight entries
    age_entry.configure(validate="key", validatecommand=(validate_age_input, "%S"))
    current_weight_entry.configure(validate="key", validatecommand=(validate_current_weight_input, "%S"))

    signup.mainloop()

#-----------------------------------------------------------------------------------------------------

def validate_age_input(char):
    return char.isdigit() or char == ""

def validate_current_weight_input(char):
    return char.isdigit() or char == "." or char == ""

#-----------------------------------------------------------------------------------------------------

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


    loginpage.mainloop()

#-----------------------------------------------------------------------------------------------------

# Create Login page
create_loginpage()

#-----------------------------------------------------------------------------------------------------

# Close the database connection when the program exits
conn.close()
