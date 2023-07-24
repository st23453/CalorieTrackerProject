import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
import customtkinter as ctk
import sqlite3


foodpage = ctk.CTk()  # Creating foodpage window
foodpage.geometry("800x450")
foodpage.title('Food Page')
foodpage.maxsize(900, 600)
foodpage.configure(fg_color="#232635")


# Main Frames  

main1_frame = ctk.CTkFrame(master=foodpage, width=200, height=800, fg_color="transparent")
main1_frame.pack(side = "left", fill = "both", expand = True) #right of the page

menu2_frame = ctk.CTkFrame(master=foodpage, width=200, height=800,fg_color="transparent")
menu2_frame.pack(side = "right", fill = "both", expand = True) #right of the page

# Frames Inside the main frames

progression_frame = ctk.CTkFrame(master=main1_frame, width=200, height=800, corner_radius=20,border_width=2)
progression_frame.pack(padx = "10", pady = "20") #top of the page

entry_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=250, corner_radius=20,border_width=2)
entry_frame.pack(side= "top", padx = 10, pady = 15) #top of the page

info_frame = ctk.CTkFrame(master=menu2_frame, width=600, height=200, corner_radius=20,border_width=2)
info_frame.pack(side = "bottom", padx = 10, pady = 20)  #bottom of the page

# Label

foodname_label = ctk.CTkLabel(master=entry_frame,text="Enter Name Of Food:")
foodname_label.place(relx=0.3, rely=0.14)


calorie1_label = ctk.CTkLabel(master=entry_frame,text="Enter Amount Of Calories")
calorie1_label.place(relx=0.3, rely=0.45)


serving1_label = ctk.CTkLabel(master=entry_frame,text="Serving:")
serving1_label.place(relx=0.3, rely=0.75)

# Entry

foodname_entry = ctk.CTkEntry(master= entry_frame, width=220, height=35, font=('Switzer', 14))
foodname_entry.place(relx=0.75, rely=0.2, anchor=tk.CENTER)

calorie1_entry = ctk.CTkEntry(master= entry_frame, width=220, height=35, font=('Switzer', 14))
calorie1_entry.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

serving1_entry = ctk.CTkEntry(master= entry_frame, width=220, height=35, font=('Switzer', 14))
serving1_entry.place(relx=0.75, rely=0.8, anchor=tk.CENTER)

foodpage.mainloop()
