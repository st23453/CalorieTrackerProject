import customtkinter as ctk

homepage = ctk.CTk()  # Creating homepage window
homepage.geometry("1280x750")
homepage.title('Homepage')

    #Homepage Frame
frame = ctk.CTkFrame(master=homepage, width=200, height=200, border_width=4)
frame.pack()

    # Homescreen widgets
    

homepage.mainloop()
