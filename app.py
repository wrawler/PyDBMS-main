#____________importing required modules_____

from tkinter import *
from tkinter import filedialog
import sys
import os
import atexit
from PIL import Image, ImageDraw, ImageTk
import mysql.connector
from mysql.connector import errorcode, errors

sys.stdout = open("/home/wrawler/vs_code/PyDBMS main/logs","a")

#______Function to connect to MySQL DB______



def connect():
    hostname = hostname_entry_box.get()
    username = username_entry_box.get()
    password = password_entry_box.get()
    dbname = database_name_entry_box.get()

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



#______exit window______

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

def newfile_window():
    new_window = Toplevel(root)
    new_window.geometry("1920x1080")
    new_window.title("PyDBMS")

    toolbar_frame_new = Frame(new_window,width=1920,height=60,bg="gray22").place(x=0,y=0,anchor="nw")
    output_frame_new = Frame(new_window,width=1440,height=1020,bg="gray16").place(x=480,y=60,anchor="nw")
    foo_frame_new = Frame(new_window,width=1920,height=30,bg="gray19").place(x=0,y=60,anchor="nw")
    querry_frame_new = Frame(new_window,width=480,height=1020,bg="gray20").place(x=0,y=0,anchor="nw")

    new_window.option_add('*tearOff', FALSE)
    my_menu_new = Menu(toolbar_frame_new,bg="gray30",fg="White",font=("Calibri",12),relief=RAISED)
    new_window.config(menu = my_menu_new)

    file_menu_new = Menu(my_menu_new)
    my_menu_new.add_cascade(label = "FILE",menu = file_menu_new)
    file_menu_new.add_command(label = "New",command = newfile_window)
    file_menu_new.add_command(label = "Open File",command = file_dialog_box)
    file_menu_new.add_command(label = "Save as")
    file_menu_new.add_command(label = "Save")
    file_menu_new.add_command(label = "Exit",command = quit)

    database_menu_new = Menu(my_menu_new)
    my_menu_new.add_cascade(label="DATABASE",menu = database_menu_new)
    database_menu_new.add_command(label = "Create")
    database_menu_new.add_command(label = "Use")
    database_menu_new.add_command(label = "Drop")

    table_menu_new = Menu(my_menu_new)
    my_menu_new.add_cascade(label="TABLE",menu=table_menu_new)
    table_menu_new.add_command(label= "Create")
    table_menu_new.add_command(label= "Modify")
    table_menu_new.add_command(label= "Drop")



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
login_window.grab_set()
login_window.geometry("550x250")
login_window.resizable(False,False)

hostname_entry_box = Entry(login_window,width=30,relief=RAISED,font=("Calibre",13))
username_entry_box = Entry(login_window,width=30,relief=RAISED,font=("Calibre",13))
password_entry_box = Entry(login_window,width=30,relief=RAISED,font=("Calibre",13),show = "*")
database_name_entry_box = Entry(login_window,width=30,relief=RAISED,font=("Calibre",13))

hostname_entry_box.place(x=200,y=20,anchor="nw")
username_entry_box.place(x=200,y=60,anchor="nw")
password_entry_box.place(x=200,y=100,anchor="nw")
database_name_entry_box.place(x=200,y=140,anchor="nw")

hostname_entry_label = Label(login_window,text="HOST:",font=("Arial",20)).place(x=10,y=20,anchor="nw")
username_entry_label = Label(login_window,text="USER",font=("Arial",20)).place(x=10,y=60,anchor="nw")
password_entry_label = Label(login_window,text="PASSWORD:",font=("Arial",20)).place(x=10,y=100,anchor="nw")
database_name_entry_label = Label(login_window,text="DATABASE:",font=("Arial",20)).place(x=10,y=140,anchor="nw")

connect_button = Button(login_window,text="Connect",font=("Arial",15),command=lambda:[connect(),login_window.destroy()]).place(x=150,y=200,anchor="nw")
cancel_button = Button(login_window,text="Cancel",font=("Arial",15),command=login_window.destroy).place(x=300,y=200,anchor="nw")



#______Creating a toolbar for root window_________

root.option_add('*tearOff', FALSE)
my_menu = Menu(toolbar_frame,bg="gray30",fg="White",font=("Calibri",12),relief=RAISED)
root.config(menu = my_menu)

file_menu = Menu(my_menu)
my_menu.add_cascade(label = "FILE",menu = file_menu)
file_menu.add_command(label = "New",command=newfile_window)
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
sys.stdout.close()