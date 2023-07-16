import tkinter as tk
import customtkinter as ctk


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
