from tkinter import PhotoImage
from playsound import playsound

bg = PhotoImage(file="assets/bg.png")
canvas.create_image(0, 0, image=bg, anchor="nw")

playsound("Assets/select.wav")
