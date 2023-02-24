from tkinter import *
from tkinter import filedialog
import os
import atexit
from PIL import Image, ImageDraw, ImageTk
import mysql.connector
from mysql.connector import errorcode

#__________Creating a window to connect to mysql database_________
def connect():
    hostname = e1.get()
    username = e2.get()
    password = e3.get()
    dbname = e4.get()

    print(hostname,username,password,dbname,"lol")

    try:
        global conn
        conn = mysql.connector.connect(
            host = "{}".format(hostname),
            user = "{}".format(username),
            passwd = "{}".format(password),
            database = "{}".format(dbname)
        )

        print("Connection established..")

    except mysql.connector.DatabaseError as ez3:
        if ez3.errno == 2005:
            print("\nNo host present named",'"',hostname,'"',"\nKindly rerun the program")


    except mysql.connector.InterfaceError as ez2:
        if ez2.errno == 2003:
            print("\n>>ERROR: Kindly recheck your connection parameters\n\t\tIf you think parameters are correct, check if mysql service is enabled...\n")

    except mysql.connector.ProgrammingError as ez:
        if errorcode.ER_ACCESS_DENIED_ERROR == ez.errno:
            print("\n>>Access Denied: Kindly recheck your connection parameters..")

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

#______login screen___________

login_window = Toplevel(root)
login_window.title('Login')
login_window.transient(root)
login_window.geometry("550x250")
login_window.resizable(False,False)

e1 = Entry(login_window,width=30,relief=RAISED,font=("Calibre",13))
e3 = Entry(login_window,width=30,relief=RAISED,font=("Calibre",13),show="*")
e4 = Entry(login_window,width=30,relief=RAISED,font=("Calibre",13))
e2 = Entry(login_window,width=30,relief=RAISED,font=("Calibre",13))

e1.place(x=200,y=20,anchor="nw")
e2.place(x=200,y=60,anchor="nw")
e3.place(x=200,y=100,anchor="nw")
e4.place(x=200,y=140,anchor="nw")

l1 = Label(login_window,text="HOST:",font=("Arial",20)).place(x=10,y=20,anchor="nw")
l2 = Label(login_window,text="USER",font=("Arial",20)).place(x=10,y=60,anchor="nw")
l3 = Label(login_window,text="PASSWORD:",font=("Arial",20)).place(x=10,y=100,anchor="nw")
l4 = Label(login_window,text="DATABASE:",font=("Arial",20)).place(x=10,y=140,anchor="nw")


connect_button = Button(login_window,text="Connect",font=("Arial",15),command=lambda:[connect(),login_window.destroy()]).place(x=150,y=200,anchor="nw")
cancel_button = Button(login_window,text="Cancel",font=("Arial",15),command=login_window.destroy).place(x=300,y=200,anchor="nw")

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
atexit.register(conn.close)