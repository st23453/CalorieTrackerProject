import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
import customtkinter as ctk
import sqlite3
import datetime

# Set customtkinter appearance mode and color theme
ctk.set_appearance_mode("system")  # Set light or dark mode
ctk.set_default_color_theme("green")  # Set the color theme

# Get the current date

def get_current_date():
    current_date = datetime.date.today()
    return current_date.strftime("%B %d, %Y")

# Datebase

# Create the database connection function
def get_database_connection():
    return sqlite3.connect('database4.db')

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
                    date DATE NOT NULL,  -- Change the type to TEXT or DATE based on your needs
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')
    
# Add a table for water entries
    cursor.execute('''CREATE TABLE IF NOT EXISTS water_entries (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    liquid_name TEXT NOT NULL,
                    amount_ml REAL NOT NULL,
                    date DATE NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')

    conn.commit()

    conn.commit()
########################################################################################################################

# Global variable

foodpage = None
homepage = None
waterpage = None
loginpage = None
historypage = None
homepage_info_label = None
water_info_label = None
food_info_label = None
user_entry = None
password_entry = None
info_label = None
calorie_intake = 0

def login():
    global user_entry, password_entry, user_data
    written_username = user_entry.get()
    written_password = password_entry.get()

    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (written_username, written_password))
        user_data = cursor.fetchone()

    if user_data:
        homepage_function()
    else:
        messagebox.showwarning(title="Error", message="Invalid Username Or Password")

def calculate_calorie_intake(weight_goal, current_weight):
    if weight_goal == "Lose Weight":
        return int(current_weight * 30) - 300
    elif weight_goal == "Gain Weight":
        return int(current_weight * 30) + 300
    elif weight_goal == "Maintain Weight":
        return int(current_weight * 30)

def calculate_total_calories():
    global user_data

    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(calories) FROM food_entries WHERE user_id=?", (user_data[0],))
        total_calories = cursor.fetchone()

    return total_calories[0] if total_calories[0] else 0

def update_calories():
    global user_data

    with get_database_connection() as conn:
        cursor = conn.cursor()
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        cursor.execute("SELECT SUM(calories) FROM food_entries WHERE user_id=? AND date=?", (user_data[0], current_date))
        total_calories = cursor.fetchone()

    homepage_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Calories: {total_calories[0]} calories")

def update_weight_if_needed():
    global user_data, calorie_intake

    total_calories = calculate_total_calories()

    if total_calories >= calorie_intake:
        weight_goal = user_data[5]

        if weight_goal == "Gain Weight":
            new_weight = user_data[4] + 0.1
        elif weight_goal == "Lose Weight":
            new_weight = user_data[4] - 0.1
        else:
            return

        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET current_weight=? WHERE id=?", (new_weight, user_data[0]))
            conn.commit()

        user_data = (*user_data[:4], new_weight, user_data[5])

        update_homepage_calories()

def update_homepage_calories():
    global homepage_info_label, user_data

    total_calories = calculate_total_calories()

    homepage_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Calories: {total_calories} calories")

def save_food_entry(food_name, calories, serving):
    global user_data

    current_date = datetime.date.today().strftime("%Y-%m-%d")

    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO food_entries (user_id, food_name, calories, serving, date) VALUES (?, ?, ?, ?, ?)",
                       (user_data[0], food_name, calories, serving, current_date))
        conn.commit()

    update_calories()

def save_water_entry(liquid_name, amount_ml):
    global user_data

    current_date = datetime.date.today().strftime("%Y-%m-%d")

    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO water_entries (user_id, liquid_name, amount_ml, date) VALUES (?, ?, ?, ?)",
                       (user_data[0], liquid_name, amount_ml, current_date))
        conn.commit()

    update_water_intake()

def update_water_intake():
    global user_data

    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount_ml) FROM water_entries WHERE user_id=?", (user_data[0],))
        total_water_ml = cursor.fetchone()

    total_water_consumed = total_water_ml[0] if total_water_ml[0] else 0

    homepage_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Water Consumed: {total_water_consumed} mL")

    if foodpage:
        food_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Water Consumed: {total_water_consumed} mL")

    if waterpage:
        water_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Water Consumed: {total_water_consumed} mL")

def populate_tree(tree):
    tree.delete(*tree.get_children())

    with get_database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT date, calories FROM food_entries WHERE user_id=?", (user_data[0],))
        entries = cursor.fetchall()

        for entry in entries:
            date, calories = entry
            cursor.execute("SELECT current_weight FROM users WHERE id=?", (user_data[0],))
            current_weight = cursor.fetchone()[0]
            tree.insert("", "end", values=(date, calories, current_weight))

def historyto_homepage():
    global historypage, homepage
    if historypage:
        historypage.destroy()

    if homepage:
        homepage.deiconify()

def historypage_function():
    global historypage, homepage, user_data

    if homepage:
        homepage.withdraw()

    historypage = ctk.CTk()
    historypage.geometry("800x450")
    historypage.title('History Page')
    historypage.maxsize(900, 600)
    historypage.configure(fg_color="#232635")

    back_button = ctk.CTkButton(master=historypage, text="Back", command=historyto_homepage,
                                corner_radius=6, fg_color="#f46b41", font=('Roboto', 12, 'bold'))
    back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    tree = ttk.Treeview(historypage, columns=("Date", "Calories", "Weight"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Calories", text="Calories")
    tree.heading("Weight", text="Weight")

    tree.place(relx=0.5, rely=0.45, anchor=tk.CENTER, relwidth=0.8, relheight=0.6)
    tree.column("Date", width=150)
    tree.column("Calories", width=150)
    tree.column("Weight", width=150)

    populate_tree(tree)

    historypage.mainloop()

def foodto_homepage():
    global foodpage, homepage
    if foodpage:
        foodpage.destroy()

    update_homepage_calories()

    if homepage:
        homepage.deiconify()



def foodpage_function():
    global foodpage, homepage, homepage_info_label

    if homepage:
        homepage.withdraw()

    foodpage = ctk.CTk()
    foodpage.geometry("800x450")
    foodpage.title('Food Page')
    foodpage.maxsize(900, 600)
    foodpage.configure(fg_color="#232635")

    main1_frame = ctk.CTkFrame(master=foodpage, width=200, height=800, fg_color="transparent")
    main1_frame.pack(side="left", fill="both", expand=True)

    menu2_frame = ctk.CTkFrame(master=foodpage, width=200, height=800, fg_color="transparent")
    menu2_frame.pack(side="right", fill="both", expand=True)

    foodinfo_frame = ctk.CTkFrame(master=main1_frame, width=200, height=800, corner_radius=20, border_width=2)
    foodinfo_frame.pack(padx="10", pady="20")

    entry_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=250, corner_radius=20, border_width=2)
    entry_frame.pack(side="top", padx=10, pady=15)

    info_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=200, corner_radius=20, border_width=2)
    info_frame.pack(side="bottom", padx=10, pady=20)

    foodname_label = ctk.CTkLabel(master=entry_frame, text="Enter Name Of Food:")
    foodname_label.place(relx=0.3, rely=0.15)

    calorie1_label = ctk.CTkLabel(master=entry_frame, text="Enter Amount Of Calories")
    calorie1_label.place(relx=0.3, rely=0.35)

    serving1_label = ctk.CTkLabel(master=entry_frame, text="Serving:")
    serving1_label.place(relx=0.3, rely=0.55)

    foodname_entry = ctk.CTkEntry(master=entry_frame, width=220, height=35, font=('Roboto', 14))
    foodname_entry.place(relx=0.75, rely=0.2, anchor=tk.CENTER)

    calorie1_entry = ctk.CTkEntry(master=entry_frame, width=220, height=35, font=('Roboto', 14))
    calorie1_entry.place(relx=0.75, rely=0.4, anchor=tk.CENTER)

    serving1_entry = ctk.CTkEntry(master=entry_frame, width=220, height=35, font=('Roboto', 14))
    serving1_entry.place(relx=0.75, rely=0.6, anchor=tk.CENTER)

    def save_entry():
        food_name = foodname_entry.get()
        calories = calorie1_entry.get()
        serving = serving1_entry.get()

        if not food_name or not calories or not serving:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        try:
            calories = float(calories)
        except ValueError:
            messagebox.showerror("Error", "Calories must be a number.")
            return

        save_food_entry(food_name, calories, serving)
        update_calories()

        foodname_entry.delete(0, tk.END)
        calorie1_entry.delete(0, tk.END)
        serving1_entry.delete(0, tk.END)

        update_homepage_calories()
        update_weight_if_needed()

    enter_button = ctk.CTkButton(master=entry_frame, text="Enter",
                                corner_radius=6, fg_color="#FFC300", font=('Roboto', 14, 'bold'))
    enter_button.place(relx=0.75, rely=0.8, anchor=tk.CENTER)

    enter_button.configure(command=save_entry)

    username_label = ctk.CTkLabel(master=foodinfo_frame, text=f"{user_data[1]}", font=("Roboto", 16))
    username_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    back_button = ctk.CTkButton(master=foodinfo_frame, text="Back", command=foodto_homepage,
                                corner_radius=6, fg_color="#f46b41", font=('Roboto', 12, 'bold'))
    back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    food_info_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 14), anchor=tk.W)
    food_info_label.place(relx=0.7, rely=0.5, anchor=tk.CENTER)

    total_calories = calculate_total_calories()
    food_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Calories: {total_calories} calories")

    food_info_label = homepage_info_label

    date_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 12), anchor=tk.W)
    date_label.place(relx=0.1, rely=0.2, anchor=tk.W)
    date_label.configure(text="Today's date:")

    date_value_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 24), anchor=tk.W)
    date_value_label.place(relx=0.1, rely=0.4, anchor=tk.W)

    current_date = get_current_date()
    date_value_label.configure(text=current_date)

    foodpage.mainloop()

def waterto_homepage():
    global waterpage, homepage
    if waterpage:
        waterpage.destroy()
    
    update_homepage_calories()

    if homepage:
        homepage.deiconify()

def waterpage_function():
    global waterpage, homepage, homepage_info_label

    if homepage:
        homepage.withdraw()

    waterpage = ctk.CTk()
    waterpage.geometry("800x450")
    waterpage.title('Water Page')
    waterpage.maxsize(900, 600)
    waterpage.configure(fg_color="#232635")

    main1_frame = ctk.CTkFrame(master=waterpage, width=200, height=800, fg_color="transparent")
    main1_frame.pack(side="left", fill="both", expand=True)

    menu2_frame = ctk.CTkFrame(master=waterpage, width=200, height=800, fg_color="transparent")
    menu2_frame.pack(side="right", fill="both", expand=True)

    waterinfo_frame = ctk.CTkFrame(master=main1_frame, width=200, height=800, corner_radius=20, border_width=2)
    waterinfo_frame.pack(padx="10", pady="20")

    entry_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=250, corner_radius=20, border_width=2)
    entry_frame.pack(side="top", padx=10, pady=15)

    info_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=200, corner_radius=20, border_width=2)
    info_frame.pack(side="bottom", padx=10, pady=20)

    watername_label = ctk.CTkLabel(master=entry_frame, text="Enter Name Of Liquid:")
    watername_label.place(relx=0.3, rely=0.15)

    amount_label = ctk.CTkLabel(master=entry_frame, text="Enter Amount (mL)")
    amount_label.place(relx=0.3, rely=0.35)

    water_info_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 14), anchor=tk.W)
    water_info_label.place(relx=0.8, rely=0.3, anchor=tk.CENTER)

    update_water_intake()

    watername_entry = ctk.CTkEntry(master=entry_frame, width=220, height=35, font=('Roboto', 14))
    watername_entry.place(relx=0.75, rely=0.2, anchor=tk.CENTER)

    amount_entry = ctk.CTkEntry(master=entry_frame, width=220, height=35, font=('Roboto', 14))
    amount_entry.place(relx=0.75, rely=0.4, anchor=tk.CENTER)

    enter_button = ctk.CTkButton(master=entry_frame, text="Enter", corner_radius=6, fg_color="#6d9eeb", font=('Roboto', 14, 'bold'))
    enter_button.place(relx=0.75, rely=0.8, anchor=tk.CENTER)
    enter_button.configure(command=save_water)

    username_label = ctk.CTkLabel(master=waterinfo_frame, text=f"{user_data[1]}", font=("Roboto", 16))
    username_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    back_button = ctk.CTkButton(master=waterinfo_frame, text="Back", command=waterto_homepage, corner_radius=6, fg_color="#f46b41", font=('Roboto', 12, 'bold'))
    back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    water_info_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 14), anchor=tk.W)
    water_info_label.place(relx=0.8, rely=0.3, anchor=tk.CENTER)

    food_info_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 14), anchor=tk.W)
    food_info_label.place(relx=0.8, rely=0.5, anchor=tk.CENTER)

    date_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 12), anchor=tk.W)
    date_label.place(relx=0.1, rely=0.2, anchor=tk.W)
    date_label.configure(text="Today's date:")

    date_value_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 24), anchor=tk.W)
    date_value_label.place(relx=0.1, rely=0.4, anchor=tk.W)

    current_date = get_current_date()
    date_value_label.configure(text=current_date)

    def save_water():
        liquid_name = watername_entry.get()
        amount_ml = amount_entry.get()

        if not liquid_name or not amount_ml:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        try:
            amount_ml = float(amount_ml)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        save_water_entry(liquid_name, amount_ml)

        watername_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)

        update_water_intake()

    waterpage.mainloop()

def homepage_function():
    global user_data, homepage, info_label, calorie_intake, homepage_info_label

    def log_out():
        response = messagebox.askyesno("Confirmation", "Are you sure you want to log out?")

        if response:
            homepage.destroy()
            create_loginpage()

    loginpage.destroy()
    homepage = ctk.CTk()
    homepage.geometry("800x500")
    homepage.title('Homepage')
    homepage.maxsize(900, 600)
    homepage.configure(fg_color="#232635")

    menu1_frame = ctk.CTkFrame(master=homepage, width=200, height=600, fg_color="transparent")
    menu1_frame.pack(side="right", fill="both", expand=True)

    menu2_frame = ctk.CTkFrame(master=homepage, width=200, height=600, fg_color="transparent")
    menu2_frame.pack(side="left", fill="both", expand=True)

    user_frame = ctk.CTkFrame(master=menu1_frame, width=200, height=600, corner_radius=20, border_width=2)
    user_frame.pack(padx="10", pady="20")

    entry_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=250, corner_radius=20, border_width=2)
    entry_frame.pack(side="top", padx=10, pady=20)

    info_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=200, corner_radius=20, border_width=2)
    info_frame.pack(side="bottom", padx=10, pady=20)

    homepage_info_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 14), anchor=tk.W)
    homepage_info_label.place(relx=0.8, rely=0.3, anchor=tk.CENTER)
    homepage_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Calories: 0 calories\nTotal Water Consumed: 0 mL")

    update_water_intake()

    total_calories = calculate_total_calories()
    homepage_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Calories: {total_calories} calories")

    calorie_intake = calculate_calorie_intake(user_data[5], user_data[4])
    homepage_info_label.configure(text=f"Base Goal: {calorie_intake} calories\nTotal Calories: {total_calories} calories")

    date_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 12), anchor=tk.CENTER)
    date_label.place(relx=0.3, rely=0.35, anchor=tk.CENTER)
    date_label.configure(text="Today's date:")

    date_value_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 24), anchor=tk.CENTER)
    date_value_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

    current_date = get_current_date()
    date_value_label.configure(text=current_date)

    select_label = ctk.CTkLabel(master=entry_frame, text="SELECT WHAT TO ENTER", font=("Roboto", 24, "bold"))
    select_label.place(relx=0.5, rely=0.15, anchor="center")

    consumed_label = ctk.CTkLabel(master=entry_frame, text="CONSUMED", font=("Roboto", 18, "bold"))
    consumed_label.place(relx=0.25, rely=0.3, anchor="center")
    
    burned_label = ctk.CTkLabel(master=entry_frame, text="BURNED", font=("Roboto", 18, "bold"))
    burned_label.place(relx=0.75, rely=0.3, anchor="center")

    food_button = ctk.CTkButton(master=entry_frame, text="FOOD", font=("Roboto", 24, "bold"), command=foodpage_function, fg_color="#f1c232", width=210, height=50)
    food_button.place(relx=0.25, rely=0.5, anchor="center")

    water_button = ctk.CTkButton(master=entry_frame, text="WATER", font=("Roboto", 24, "bold"), command=waterpage_function, fg_color="#6d9eeb", width=210, height=50)
    water_button.place(relx=0.25, rely=0.8, anchor="center")

    cardiovascular_button = ctk.CTkButton(master=entry_frame, text="CARDIOVASCULAR", font=("Roboto", 24, "bold"), fg_color="#6aa84f", width=210, height=50)
    cardiovascular_button.place(relx=0.75, rely=0.5, anchor="center")

    strength_button = ctk.CTkButton(master=entry_frame, text="STRENGTH TRAINING", font=("Roboto", 24, "bold"), fg_color="#cc0000", width=200, height=50)
    strength_button.place(relx=0.75, rely=0.8, anchor="center")

    username_label = ctk.CTkLabel(master=user_frame, text=f"{user_data[1]}", font=("Roboto", 24, "bold"))
    username_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    logout_button = ctk.CTkButton(master=user_frame, text="LOG OUT", command=log_out,
                                  corner_radius=6, fg_color="#f46b41", font=('Roboto', 24, 'bold'), width=160, height=60)
    logout_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    history_button = ctk.CTkButton(master=user_frame, text="HISTORY", command=historypage_function,
                                  corner_radius=6, fg_color="#282434", font=('Roboto', 24, 'bold'), width=160, height=60)
    history_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    diary_button = ctk.CTkButton(master=user_frame, text="FOOD DIARY",
                                  corner_radius=6, fg_color="#282434", font=('Roboto', 24, 'bold'), width=160, height=60)
    diary_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    workout_button = ctk.CTkButton(master=user_frame, text="WORKOUT PLAN",
                                  corner_radius=6, fg_color="#282434", font=('Roboto', 24, 'bold'), width=160, height=60)
    workout_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    homepage.mainloop()

def signup_function():
    global user_entry, password_entry

    def go_back():
        signup.destroy()
        create_loginpage()

    loginpage.destroy()
    signup = ctk.CTk()
    signup.geometry("850x500")
    signup.title('Sign Up')

    back_button = ctk.CTkButton(master=signup, width=100, text="Back", command=go_back,
                                corner_radius=6, fg_color="#f46b41", font=('Roboto', 12, 'bold'))
    back_button.place(relx=0.1, rely=0.9, anchor=tk.CENTER)

    label = ctk.CTkLabel(master=signup, text="Sign Up Page", font=('Century Gothic', 60))
    label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    username_label = ctk.CTkLabel(master=signup, text="Username:", font=('Roboto', 14))
    username_label.place(relx=0.3, rely=0.3, anchor=tk.CENTER)
    username_entry = ctk.CTkEntry(master=signup, width=220, height=35, font=('Roboto', 14), fg_color="#e0dcdc", text_color="black")
    username_entry.place(relx=0.6, rely=0.3, anchor=tk.CENTER)

    password_label = ctk.CTkLabel(master=signup, text="Password:", font=('Roboto', 14))
    password_label.place(relx=0.3, rely=0.4, anchor=tk.CENTER)
    password_entry = ctk.CTkEntry(master=signup, width=220, height=35, font=('Roboto', 14), fg_color="#e0dcdc", text_color="black")
    password_entry.place(relx=0.6, rely=0.4, anchor=tk.CENTER)

    age_label = ctk.CTkLabel(master=signup, text="Age:", font=('Roboto', 14))
    age_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
    age_entry = ctk.CTkEntry(master=signup, width=220, height=35, font=('Roboto', 14), fg_color="#e0dcdc", text_color="black")
    age_entry.place(relx=0.6, rely=0.5, anchor=tk.CENTER)

    current_weight_label = ctk.CTkLabel(master=signup, text="Current Weight:", font=('Roboto', 14))
    current_weight_label.place(relx=0.3, rely=0.6, anchor=tk.CENTER)
    current_weight_entry = ctk.CTkEntry(master=signup, width=220, height=35, font=('Roboto', 14), fg_color="#e0dcdc", text_color="black")
    current_weight_entry.place(relx=0.6, rely=0.6, anchor=tk.CENTER)

    weight_goal_label = ctk.CTkLabel(master=signup, text="Weight Goal:", font=('Roboto', 14))
    weight_goal_label.place(relx=0.3, rely=0.7, anchor=tk.CENTER)

    weight_goal_var = tk.StringVar()
    weight_goal_var.set("Select")
    weight_goal_options = ["Lose Weight", "Gain Weight", "Maintain Weight"]
    weight_goal_combobox = Combobox(master=signup, width=23, height=35, textvariable=weight_goal_var, values=weight_goal_options,
                                    font=('Roboto', 14), state="readonly")
    weight_goal_combobox.place(relx=0.6, rely=0.7, anchor=tk.CENTER)

    def save_signup():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        age = age_entry.get().strip()
        current_weight = current_weight_entry.get().strip()
        weight_goal = weight_goal_var.get()

        if not username or not password or not age or not current_weight or not weight_goal:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be an integer.")
            return

        try:
            current_weight = float(current_weight)
        except ValueError:
            messagebox.showerror("Error", "Current weight must be a number.")
            return

        if weight_goal == "Select":
            messagebox.showwarning("Error", "Please select a weight goal.")
            return

        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            return

        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, age, current_weight, weight_goal) VALUES (?, ?, ?, ?, ?)",
                        (username, password, age, current_weight, weight_goal))
            conn.commit()

        messagebox.showinfo("Success", "Account created successfully!")
        go_back()

    save_button = ctk.CTkButton(master=signup, text="Sign Up", command=save_signup,
                                corner_radius=6, fg_color="#FFC300", font=('Roboto', 12, 'bold'))
    save_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    age_entry.configure(validate="key", validatecommand=(validate_age_input, "%S"))
    current_weight_entry.configure(validate="key", validatecommand=(validate_current_weight_input, "%S"))

    signup.mainloop()

def validate_age_input(char):
    return char.isdigit() or char == ""

def validate_current_weight_input(char):
    return char.isdigit() or char == "." or char == ""

def create_loginpage():
    global loginpage, user_entry, password_entry

    loginpage = ctk.CTk()
    loginpage.geometry("600x400")
    loginpage.title("Login")
    loginpage.maxsize(900, 600)
    loginpage.configure(fg_color="#232635")

    loginframe = ctk.CTkFrame(master=loginpage, corner_radius=20, fg_color="#232635")
    loginframe.pack(pady=20, padx=20, fill="both", expand=True)

    label1 = ctk.CTkLabel(master=loginframe, text="Welcome To The Best", font=('Roboto', 28, 'bold'))
    label1.place(relx=0.5, rely=0.23, anchor=tk.CENTER)

    label2 = ctk.CTkLabel(master=loginframe, text="Calorie Tracker", font=('Roboto', 42, 'bold'))
    label2.place(relx=0.5, rely=0.33, anchor=tk.CENTER)

    user_entry = ctk.CTkEntry(master=loginframe, width=220, height=35, placeholder_text='Username or Email',
                              font=('Roboto', 16), fg_color="#e0dcdc", text_color="black") 
    user_entry.place(relx=0.5, rely=0.46, anchor=tk.CENTER)

    password_entry = ctk.CTkEntry(master=loginframe, width=220, height=35, placeholder_text='Password',
                                  show="●", font=("Roboto", 16), fg_color="#e0dcdc", text_color="black")
    password_entry.place(relx=0.5, rely=0.56, anchor=tk.CENTER)

    login_button = ctk.CTkButton(master=loginframe, width=220, height=35, text="Login", command=login,
                                 corner_radius=6, fg_color="#FFC300", border_spacing=10,
                                 font=('Roboto', 18, 'bold'))
    login_button.place(relx=0.5, rely=0.68, anchor=tk.CENTER)

    signup_button = ctk.CTkButton(master=loginframe, width=220, text="Sign Up For Free", command=signup_function,
                                  corner_radius=6, fg_color="transparent", font=('Roboto', 12, 'bold'))
    signup_button.place(relx=0.5, rely=0.78, anchor=tk.CENTER)

    loginpage.mainloop()

#-----------------------------------------------------------------------------------------------------

# Create Login page
create_loginpage()

#-----------------------------------------------------------------------------------------------------

# Close the database connection when the program exits
conn.close()

