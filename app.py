from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageDraw, ImageTk

def connector_window():
    top1 = Toplevel(root)
    top1.transient(root)
    top1.geometry("550x300")
    top1.title("Connect")
    top1.resizable(False,False)

    e1 = Entry(top1,width=30,relief=RAISED,font=("Calibre",13)).grid(row=0,column=2,pady=10,ipadx=0)
    e2 = Entry(top1,width=30,relief=RAISED,font=("Calibre",13)).grid(row=1,column=2,pady=10,ipadx=0)
    e3 = Entry(top1,width=30,relief=RAISED,font=("Calibre",13),show="*").grid(row=2,column=2,pady=10,ipadx=0)
    e4 = Entry(top1,width=30,relief=RAISED,font=("Calibre",13)).grid(row=3,column=2,pady=10,ipadx=0)

    l1 = Label(top1,text="HOST:",font=("Arial",20)).grid(row=0,column=0,pady=10,ipadx=0)
    l2 = Label(top1,text="USER",font=("Arial",20)).grid(row=1,column=0,pady=10,ipadx=0)
    l3 = Label(top1,text="PASSWORD:",font=("Arial",20)).grid(row=2,column=0,pady=10,ipadx=0)
    l4 = Label(top1,text="DATABASE:",font=("Arial",20)).grid(row=3,column=0,pady=10,ipadx=0)

    connect_button = Button(top1,text="Connect",font=("Arial",15),command=top1.destroy).grid(row=4,column=0,pady=20)
    cancel_button = Button(top1,text="Cancel",font=("Arial",15),command=top1.destroy).grid(row=4,column=1,pady=20)

def quit():
    top2 = Toplevel(root)
    top2.geometry("150x80")
    top2.title("Exit")
    exit_label = Label(top2,text="Exit?",font = ("Arial",15))
    exit_label.place(x=0,y=0)

    no = Button(top2,text="cancel",font = ("Arial",13),command = top2.destroy,relief=RAISED).place(relx=0,rely=0.5)
    yes = Button(top2,text="ok",font = ("Arial",13),width = 5,command = root.quit,relief=RAISED).place(relx=0.5,rely=0.5)

    top2.transient(root) 
    top2.resizable(False,False) 

def file_dialog_box():
    root.filename = filedialog.askopenfilename(initialdir = "/",title="Select A File",filetypes = (("Database file","*.db"),("All Files","*.*")))

#root window
root = Tk()
root.geometry("1920x1080")
root.title("PyDBMS")

toolbar_frame = Frame(root,width=1920,height=60,bg="gray22").place(x=0,y=0,anchor="nw")
output_frame = Frame(root,width=1440,height=1020,bg="gray16").place(x=480,y=60,anchor="nw")
foo_frame = Frame(root,width=1920,height=30,bg="gray19").place(x=0,y=60,anchor="nw")
querry_frame = Frame(root,width=480,height=1020,bg="gray20").place(x=0,y=0,anchor="nw")

#toolbar
conn_button = Button(toolbar_frame,padx=2,text="CONNECT",font = ("Arial",12),command = connector_window,bg="gray27",fg="white",highlightthickness = 0,relief=RAISED).pack(anchor="nw")

root.option_add('*tearOff', FALSE)
my_menu = Menu(toolbar_frame,bg="gray30",fg="White",font=("Calibri",12),relief=RAISED)
root.config(menu = my_menu)

file_menu = Menu(my_menu)
my_menu.add_cascade(label = "FILE",menu = file_menu)
file_menu.add_command(label = "New")
file_menu.add_command(label = "Open File",command = file_dialog_box)
file_menu.add_command(label = "Save as")
file_menu.add_command(label = "Save")
file_menu.add_command(label = "Exit",command = quit)

database_menu = Menu(my_menu)
my_menu.add_cascade(label="DATABASE",menu = database_menu)
database_menu.add_command(label = "Create")
database_menu.add_command(label = "Use")
database_menu.add_command(label = "Drop")

table_menu = Menu(my_menu)
my_menu.add_cascade(label="TABLE",menu=table_menu)
table_menu.add_command(label= "Create")
table_menu.add_command(label= "Modify")
table_menu.add_command(label= "Drop")

#initiate
root.mainloop()
