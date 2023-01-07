from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageDraw, ImageTk
import mysql.connector
from mysql.connector import errorcode

#_________Creating a function to connect to mysql database
mydb = None

def connect(a,b,c,d):
    global mydb
    try:
        mydb = mysql.connector.connect(
            host = "{}".format(a),
            user = "{}".format(b),
            password = "{}".format(c),
            database = "{}".format(d)
        )

        if mydb.is_connected():
            conn_status_yes = ImageTk.PhotoImage(Image.open("tick.png"))
            conn_status_label.config(image=conn_status_yes,highlightthickness=0,borderwidth=0)
            conn_status_label.image=conn_status_yes

        else:
            pass
            
    except mysql.connector.DatabaseError as ez3:
        if ez3.errno == 2005:
            print("\nNo host present named",'"',a,'"',"\nKindly rerun the program")

    except mysql.connector.ProgrammingError as ez:
        if errorcode.ER_ACCESS_DENIED_ERROR == ez.errno:
            print("\n>>Access Denied: Kindly recheck your connection parameters..")

    except mysql.connector.InterfaceError as ez2:
        if ez2.errno == 2003:
            print("\n>>ERROR: Kindly recheck your connection parameters\n\t\tIf you think parameters are correct, check if mysql service is enabled...\n")


#__________Creating a window to connect to mysql database_________


def connector_window():
    top1 = Toplevel(root)
    top1.transient(root)
    top1.geometry("550x250")
    top1.title("Connect")
    top1.resizable(False,False)

    e1 = Entry(top1,width=30,relief=RAISED,font=("Calibre",13))
    e2 = Entry(top1,width=30,relief=RAISED,font=("Calibre",13))
    e3 = Entry(top1,width=30,relief=RAISED,font=("Calibre",13),show="*")
    e4 = Entry(top1,width=30,relief=RAISED,font=("Calibre",13))

    e1.place(x=200,y=20,anchor="nw")
    e2.place(x=200,y=60,anchor="nw")
    e3.place(x=200,y=100,anchor="nw")
    e4.place(x=200,y=140,anchor="nw")

    l1 = Label(top1,text="HOST:",font=("Arial",20)).place(x=10,y=20,anchor="nw")
    l2 = Label(top1,text="USER",font=("Arial",20)).place(x=10,y=60,anchor="nw")
    l3 = Label(top1,text="PASSWORD:",font=("Arial",20)).place(x=10,y=100,anchor="nw")
    l4 = Label(top1,text="DATABASE:",font=("Arial",20)).place(x=10,y=140,anchor="nw")

    hostname = e1.get()
    username = e2.get()
    passwd = e3.get()
    dbname = e4.get()

    connect_button = Button(top1,text="Connect",font=("Arial",15),command=lambda:[connect(hostname,username,passwd,dbname),top1.destroy()]).place(x=150,y=200,anchor="nw")
    cancel_button = Button(top1,text="Cancel",font=("Arial",15),command=top1.destroy).place(x=300,y=200,anchor="nw")

    hide_image = ImageTk.PhotoImage(file="tick.png")
    hide_image_label = Label(image=hide_image)
    pass_button = Button(top1,image = hide_image).place(x=150,y=100,anchor="nw")
    hide_image_label.image = hide_image

def quit():
    top2 = Toplevel(root)
    top2.geometry("150x80")
    top2.title("Exit")
    exit_label = Label(top2,text="Exit?",font = ("Arial",15))
    exit_label.place(x=0,y=0)

    no = Button(top2,text="cancel",font = ("Arial",13),command = top2.destroy,relief=RAISED).place(relx=0,rely=0.5)
    yes = Button(top2,text="ok",font = ("Arial",13),width = 5,command = lambda:[mydb.close(),root.quit()],relief=RAISED).place(relx=0.5,rely=0.5)

    top2.transient(root) 
    top2.resizable(False,False) 


#___________Creating a window to open a file from desired directory________

def file_dialog_box():
    root.filename = filedialog.askopenfilename(initialdir = "/",title="Select A File",filetypes = (("Database file","*.db"),("All Files","*.*")))


#_________Creating a new window similar to root window to create a new file_____________


def newfileframe():
    top3 = Toplevel(root)
    top3.geometry("1920x1080")
    top3.title("PyDBMS")

    toolbar_frame2 = Frame(top3,width=1920,height=60,bg="gray22").place(x=0,y=0,anchor="nw")
    output_frame2 = Frame(top3,width=1440,height=1020,bg="gray16").place(x=480,y=60,anchor="nw")
    foo_frame2 = Frame(top3,width=1920,height=30,bg="gray19").place(x=0,y=60,anchor="nw")
    querry_frame2 = Frame(top3,width=480,height=1020,bg="gray20").place(x=0,y=0,anchor="nw")

    conn_button2 = Button(top3,padx=2,text="CONNECT",font = ("Arial",12),command = connector_window,bg="gray27",fg="white",highlightthickness = 0,relief=RAISED).pack(anchor="nw")

    top3.option_add('*tearOff', FALSE)
    my_menu2 = Menu(toolbar_frame2,bg="gray30",fg="White",font=("Calibri",12),relief=RAISED)
    top3.config(menu = my_menu2)

    file_menu = Menu(my_menu2)
    my_menu2.add_cascade(label = "FILE",menu = file_menu)
    file_menu.add_command(label = "New",command=newfileframe)
    file_menu.add_command(label = "Open File",command = file_dialog_box)
    file_menu.add_command(label = "Save as")
    file_menu.add_command(label = "Save")
    file_menu.add_command(label = "Exit",command = quit)

    database_menu = Menu(my_menu)
    my_menu2.add_cascade(label="DATABASE",menu = database_menu)
    database_menu.add_command(label = "Create")
    database_menu.add_command(label = "Use")
    database_menu.add_command(label = "Drop")

    table_menu = Menu(my_menu)
    my_menu2.add_cascade(label="TABLE",menu=table_menu)
    table_menu.add_command(label= "Create")
    table_menu.add_command(label= "Modify")
    table_menu.add_command(label= "Drop")

#______Defining the root window__________

root = Tk()
root.geometry("1920x1080")
root.title("PyDBMS")

toolbar_frame = Frame(root,width=1920,height=60,bg="gray22").place(x=0,y=0,anchor="nw")
output_frame = Frame(root,width=1440,height=1020,bg="gray16").place(x=480,y=60,anchor="nw")
foo_frame = Frame(root,width=1920,height=30,bg="gray19").place(x=0,y=60,anchor="nw")
querry_frame = Frame(root,width=480,height=1020,bg="gray20").place(x=0,y=0,anchor="nw")

conn_button = Button(toolbar_frame,padx=2,text="CONNECT",font = ("Arial",12),command = connector_window,bg="gray27",fg="white",highlightthickness = 0,relief=RAISED).pack(anchor="nw")

conn_label = Label(text="CONNECTION STATUS",fg="white",bg="gray22")
conn_label.place(x=1755,y=5,anchor="nw")

global conn_status_label
conn_status_no = ImageTk.PhotoImage(Image.open("cross.png"))
conn_status_label = Label(image=conn_status_no,highlightthickness=0,borderwidth=0)
conn_status_label.place(x=1890,y=5,anchor="nw")

#______Creating a toolbar for root window_________


root.option_add('*tearOff', FALSE)
my_menu = Menu(toolbar_frame,bg="gray30",fg="White",font=("Calibri",12),relief=RAISED)
root.config(menu = my_menu)

file_menu = Menu(my_menu)
my_menu.add_cascade(label = "FILE",menu = file_menu)
file_menu.add_command(label = "New",command=newfileframe)
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


#____main_____

root.mainloop()