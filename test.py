from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.geometry('500x500')
label = Label(window, text="TEST123",bg='yellow', fg='red',font=('Helvetica 35 bold'))
label.pack(side=TOP)

def function1():
    window2 = Tk()
    window2.geometry('500x500')
    
    def entryfunc():
        global entry1
        entry1 = StringVar()

        label1 = Label(window2, text="Please tell us your name: ",bg='white', fg='black',font=('Helvetica 15 bold'))
        label1.pack()
        entry = Entry(window2, textvariable = entry1, show='*')
        entry.pack()
        return entry1

    label2 = Label(window2)
    label2.pack()

    def show_frame():  
        imgtk = ImageTk.PhotoImage(file="C:/Users/Ryan's Laptop/Desktop/Coding/Projects/Waste Segregation/logo.png")
        label2.configure(image=imgtk)
        label2.after(10, show_frame)

    show_frame()

    entry1 = entryfunc()

    window2.mainloop()


but1=Button(window,padx=5,pady=5,width=20,bg='green',fg='red',command=function1,text='Open New Window',font=('helvetica 15'))
but1.place(x=200,y=400)


window.mainloop()