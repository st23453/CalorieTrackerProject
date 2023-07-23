import customtkinter as ctk
import tkinter as tk
import sqlite3

window = ctk.CTk()
window.title("Test")
window.iconbitmap("")
window.geometry("400x400")

# Database

# Create a database or connect to one
conn = sqlite3.connect("calorie_count.db")

# Create cursor
cursor = conn.cursor()

# Commit changes
conn.commit()

# Create table
cursor.execute("""CREATE TABLE addresses (
        first_name text,   
        last_name text,
        address text,
        city text,
        state text,
        zipcode interger
        )""")

# Close connection
conn.close()

window.mainloop()