import tkinter
import customtkinter
from PIL import ImageTk, Image

customtkinter.set_appearance_mode("system)") #can set light or dark
customtkinter.set_default_color_theme("dark-blue")# themes: blue, green, dark-blue, 

app=customtkinter.CTk() #creating customtkinter window
app.geometry("700x500")
app.title("Login")



app.mainloop()