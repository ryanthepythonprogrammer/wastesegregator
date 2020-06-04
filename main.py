from PIL import Image as IMG_TOOL
from PIL import ImageTk
import tkinter as tk
from tkinter import *
import cv2
import os
from selenium import webdriver
import threading
import tensorflow as tf
from time import sleep, strftime
from prog_backend import frame_loader

model = tf.keras.models.load_model("C:/Users/Ryan's Laptop/Desktop/Coding/Projects/Waste Segregation/models/new_ft.model")



def web_open():
    chromedriver_path = "C:/Users/Ryan's Laptop/Desktop/chromedriver.exe"
    webber = webdriver.Chrome(executable_path=chromedriver_path)
    sleep(2)
    webber.get('https://www.getwaste.info/')
    sleep(3)

def detection():
    
    root2=Toplevel(root)
    root2.geometry('450x800')
    # root2.bind('<escape>', lambda e: root2.quit())
    fra = Frame(root2, relief=RIDGE, borderwidth=2)
    fra.pack(fill=BOTH,expand=1)
    root2.title('Camera')
    fra.config(background='white')
    label = Label(fra, text="Camera",bg='#91ffa6',font=('Helvetica 35 bold'))
    label.pack(side=TOP)
    but2 = Button(fra,padx=5,pady=5,width=20,bg='#ffefab',fg='green',relief=GROOVE,text='More Info',command=web_open,font=('helvetica 15'))
    but2.place(x=100,y=650)
    model = tf.keras.models.load_model("C:/Users/Ryan's Laptop/Desktop/Coding/Projects/Waste Segregation/models/new_ft.model")
    lmain = tk.Label(root2)
    lmain.place(x=25, y=150)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

    
    def show_frame():
        _, frame = cap.read()

        n_prediction, bin_prediction = frame_loader(frame, model)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(frame, bin_prediction, (0, 35), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0))
        cv2.putText(frame, n_prediction, (0, 275), cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0))
        img = IMG_TOOL.fromarray(frame)
        imgtk = ImageTk.PhotoImage(img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)
    
    show_frame()
    root2.mainloop()



root=Tk()
root.geometry('450x800')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
root.title('Waste Segregator')
frame.config(background='white')
label = Label(frame, text="SegreCAM",bg='#91ffa6',font=('Helvetica 35 bold'))
label.pack(side=TOP)
filename = PhotoImage(file="C:/Users/Ryan's Laptop/Desktop/Coding/Projects/Waste Segregation/logo.png")
background_label = Label(frame,image=filename)
background_label.pack(side=TOP)


but1=Button(frame,padx=5,pady=5,width=20,bg='#ffefab',fg='green',relief=GROOVE,command=detection,text='Open Segregator',font=('helvetica 15'))
but1.place(x=100,y=550)

but2 = Button(frame,padx=5,pady=5,width=20,bg='#ffefab',fg='green',relief=GROOVE,text='More Info',command=web_open,font=('helvetica 15'))
but2.place(x=100,y=650)

root.mainloop()
