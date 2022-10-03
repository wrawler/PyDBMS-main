## Importing mysql connector
import mysql.connector
from mysql.connector import errorcode


## Creating connection object
hostname = input("\nPLEASE ENTER YOUR HOSTNAME (By default: localhost):" ) or "localhost"     #no actuall need to enter you username and passwd if you have default ones
username = input("PLEASE ENTER YOUR USERNAME(By default: root ):") or "root"
passwd = input("PLEASE ENTER YOUR USER PASSWORD:") or "no_input"

if passwd != "no_input":
    try:
        mydb = mysql.connector.connect(
            host = hostname,
            user = username,
            password = passwd,
    )

    except mysql.connector.ProgrammingError as ez:
        if errorcode.ER_ACCESS_DENIED_ERROR == ez.errno:
            print("\nAccess Denied: Kindly recheck your connection parameters..")
            quit()


elif passwd == "no_input":                     #if user does not enters password, program will just shut down
    print("NO PASSWORD ENTERED!! \nKINDLY RERUN THE PROGRAM")
    quit()

## Defining a cursor object
cursor_obj = mydb.cursor()


## Creating a database
def database_create():
    database_name = input("PLEASE ENTER THE NAME OF THE NEW DATABASE:")
    try:
        cursor_obj.execute("CREATE DATABASE {}".format(database_name))
    except mysql.connector.DatabaseError as e:
        if errorcode.ER_DB_CREATE_EXISTS == e.errno:
            print("\nERROR: {} database already exists..".format(database_name))
        else:
            print("Table created with no errors..")

## Showing created databases
def database_show():
    cursor_obj.execute("SHOW DATABASES")
    for x in cursor_obj:
        print(x)

## Using a database
def database_use():
    db_name = input("PLEASE ENTER THE NAME OF DATABASE TO USE:")
    try:
        cursor_obj.execute("use {}".format(db_name))
    except mysql.connector.DatabaseError as e:
        if errorcode.ER_BAD_DB_ERROR == e.errno:
            print("\nERROR: {} database does not exist".format(db_name))
## Drop a database
def database_drop():
    database_name = input("ENTER THE NAME OF THE DATABASE:")
    try:
        cursor_obj.execute('DROP DATABASE {}'.format(database_name))
    except mysql.connector.DatabaseError as e:
        if errorcode.ER_DB_DROP_EXISTS == e.errno:
            print("ERROR: {} database does not exist".format(db_name))

## To create a table
def table_creator():
    try:
        table_name = input("PLEASE ENTER THE NAME OF NEW TABLE:")

        print("\nKindly first create the initiating column for table, you would be given choice to create table with as much columns you want...")   
                            # first created a table with one column and added more columns showing that all the columns were made at time of table creations
        

        a = input("NAME FOR COLUMN 1:")
        t = input("DATATYPE OF COLUMN 1:")
        size = input("SIZE OF COLUMN 1:")
        choice1 = input("\nDO YOU WANT TO ADD CONSTRAINS TO THIS COLUMN ? y or n")    #asking if contrains are to be added

        if choice1 == "y":
            constrain = input("\nENTER THE DESIRED CONSTRAINS SEPERATED BY SPACES:")
            cursor_obj.execute("CREATE TABLE {} ({} {}({}) {})".format(table_name,a,t,size,constrain))  
                                  # we need to add column into table as needed by user to show we added all columns at one go :)
        elif choice1 == "n":
            cursor_obj.execute("CREATE TABLE {} ({} {}({}))".format(table_name,a,t,size))

        x = int(input("PLEASE ENTER THE NUMBER OF COLUMNS YOU WANT IN TABLE:"))          #determing the desired degree of table
        i = 1 
        while i < x:                                                  #loop to add columns to table
            a1 = input("NAME FOR COLUMN {}:".format(i+1))
            t1 = input("DATATYPE FOR COLUMN {}:".format(i+1))
            size1 = input("SIZE OF COLUMN {}:".format(i+1))
            choice1 = input("Do you want to add constrains to this column? y or n ")

            if choice1 == "y":
                constrain = input("ENTER THE DESIRED CONSTRAINS SEPERATED BY SPACES:\n")              #two different conditions for having or not having constrains 
                cursor_obj.execute("Alter table {} add column {} {}({}) {}".format(table_name,a1,t1,size1,constrain))
            elif choice1 == "n":
                cursor_obj.execute('Alter table {} add column {} {}({})'.format(table_name,a1,t1,size1))
            else:
                print("Invalid Selection, kindly rerun the program")
            i = i+1
    except mysql.connector.ProgrammingError as e:
        if errorcode.ER_CANT_CREATE_TABLE == e.errno:
            print("\nERROR: Can't create table, table already exists...")
        elif errorcode.ER_PARSE_ERROR == e.errno:
            print("\nERROR: kindly recheck your column creation parameters\n")

## To see created tables
def tables_show():
    cursor_obj.execute("SHOW TABLES")
    for x in cursor_obj:
        print(x)


## TO delete a table
def table_del():
    table_name = input("ENTER NAME OF THE TABLE:")
    
    cursor_obj.execute("DROP TABLE {} ".format(table_name))

## Creating a comitt option
def commit():

    choice_commit = input("DO YOU WANT TO SAVE THE CHANGES? \n y or n")

    if choice_commit == "y":
        mydb.commit()
        print("Changes saved")

    elif choice_commit == "n":
        print("Changes unsaved")

    else:
        print("Changes unsaved due to invalid selection")


## To input values to a table
def inputer():

    table_name = input("PLEASE ENTER THE NAME OF THE TABLE: ") or "no_input"

    if table_name != "no_input":
        cursor_obj.execute("select database() from dual")
        for i in cursor_obj:
            database_name = i[0]


        cursor_obj.execute("set @a  = (select count(*) as count from information_schema.columns where table_schema = '{}' and table_name = '{}') ".format(database_name,table_name))
        cursor_obj.execute("select @a")
        for i in cursor_obj:
            x = i
            degree = x[0]     #stored the number of columns in degree var


        choice = input("DO YOU WANT TO SEE THE TABLE STRUCTURE?: \n \n y for yes and n for no:")

        if choice == "y":
                    cursor_obj.execute("DESCRIBE {}".format(table_name))
                    for x in cursor_obj:
                        print(x)      #table structure shown to user for efficiency

        elif choice == "n":
            print("\nGREAT, YOU SEEM TO HAVE A NICE MEMORY")  

        else:
            print("\nINVALID SELECTION, CONTINUING WITHOUT SHOWING TABLE STRUCTURE")

        choice2 = int(input("\nENTER THE NUMBER OF RECORDS YOU WANT TO ENTER: "))    #determining the number of records to be entered 
        a = 0
        while a < choice2:                #loop for showing the record number and for adding multiple records at a time
            print("INPUTS FOR RECORD NO {}".format(a+1))
            i = 0
            list1 = []
            while i < degree:             #loop to show the input number and appending the inputs into a list
                x1 = input("ENTER INPUT NO.{}: \n ".format(i+1))
                list1.append(x1)
                i = i + 1

            try: 
                cursor_obj.execute("INSERT INTO {} VALUES{}".format(table_name,tuple(list1)))     #converting list into tuple to perform insert_into fucntion
            except mysql.connector.DataError as e:
                if errorcode.ER_TRUNCATED_WRONG_VALUE_FOR_FIELD == e.errno:
                    print("\nERROR: Kindly check the datatype of input..\n consider seeing the table structure prior inputting...")
            a = a + 1


    elif table_name == "no_input":
        print("\nTABLE NAME NOT ENTERED \nKINDLY RERUN THE PROGRAM")


## Function to display the whole content of the table
def print_table():
    table_name = input("ENTER THE NAME OF THE TABLE TO PRINT:") or "no_input"

    if table_name != "no_input":

        choice = input("WHAT PORTION OF TABLE WOULD YOU LIKE TO PRINT? : \n \n(a)WHOLE TABLE \n \n(b)A SPECIFIC COLUMN \n \n(c)A WHOLE RECORD REFFERING TO RECORD IN SPECIFIED COLUMN \n \n(d) STRUCTURE OF THE TABLE -->")

        if choice == 'a':
                cursor_obj.execute("select * from {}".format(table_name))
                for x in cursor_obj:
                    print(x)

        elif choice == 'b':
            x = input("PLEASE ENTER THE NAME OF COLUMN TO PRINT:")
            cursor_obj.execute("select {} from {}".format(x,table_name))
            for i in cursor_obj:
                print(i)

        elif choice == 'c':

            choice1 = input("WOULD YOU LIKE TO SEE THE WHOLE TABLE ONCE FOR SPECIFYING THE CONDITION? y or n -->")

            if choice1 == 'y':     
                print("\nTHE TABLE-->\n")                                    #asking if user wants to see the table structure
                                                           
                cursor_obj.execute("select * from {}".format(table_name))
                for i in cursor_obj:
                    print(i)

                print("THE STRUCTURE OF TABLE--")

                cursor_obj.execute("describe {}".format(table_name))
                for x in cursor_obj:
                    print(x)


            elif choice1 == 'n':
                print("FINE, YOU SEEM TO REMEMBER THE WHOLE TABLE")


            else:
                print("ERROR: Invalid Selection..")           
            x1 = input("NOW PLEASE ENTER THE NAME OF COLUMN TO REFER:")
            y1 = input("NOW PLEASE ENTER THE RECORD IN THAT COLUMN TO REFER:")
            cursor_obj.execute("select * from {} where {} = '{}'".format(table_name,x1,y1))
            for i in cursor_obj:
                print(i)


        elif choice == "d":
                cursor_obj.execute("describe {}".format(table_name))
                for x in cursor_obj:
                    print(x)


        else:
            print("ERROR: Invalid Selection..\n")


    elif table_name == "no_input":
        print("\nNO INPUT RECEIVED \nKINDLY RERUN THE PROGRAM")
    print("\nJUST SAYING, EMPTY TABLE WONT GIVE ANY OUTPUT")


## Adding column into the table
def column_add():
    table_name = input('Enter the table to add column to:')
    new_column = input("Enter the name of the new column:")
    data_type = input("Enter the data type of new column:")
    size = int(input("Enter the size of the new column:\n"))

    try:
        cursor_obj.execute('Alter table {} add column {} {}({})'.format(table_name,new_column,data_type,size))
    except mysql.connector.ProgrammingError as e:
        if errorcode.ER_PARSE_ERROR == e.errno:
            print("\nERROR: Kindly recheck your column parameters..")


# Deleting a column
def column_del():
    table_name = input("\nENTER THE NAME OF THE TABLE:")
    column_name = input("\nENTER THE COLUMN NAME TO DELETE: ")

    try:
        cursor_obj.execute("ALTER TABLE {} DROP COLUMN {}".format(table_name,column_name))
    except mysql.connector.ProgrammingError as e:
        if errorcode.ER_NO_SUCH_TABLE == e.errno:
            print("\nERROR: Table does not exist..")
            print("Kindly rerun the program..")
        if errorcode.ER_CANT_DROP_FIELD_OR_KEY == e.errno:
            print("ERROR: Can't delete column, column does not exist..")

# Modifying a column
def column_modify():
    try:    
        table_name = input("ENTER THE NAME OF THE TABLE:") or "no_input"
        column_new = input("ENTER THE NEW COLUMN NAME (ENTER THE CURRENT COLUMN NAME FOR NO CHANGES):") or "no_input"
        dat_new    = input("ENTER THE NEW DATATYPE FOR COLUMN (ENTER CURRENT DATAYPE FOR NO CHANGES):") or "no_input"
        size_new   = input("ENTER THE NEW SIZE FOR DATATYPE (ENTER THE CURRENT SIZE FOR NO CHANGES):")  or 'no_input'

        if table_name and column_new and dat_new and size_new != "no-input":
            cursor_obj.execute("ALTER TABLE {} MODIFY {} {}({})".format(table_name,column_new,dat_new,size_new))

        elif table_name or column_new or dat_new or size_new == "no-input":
            print("SOME INPUT SEEMS TO BE MISSING \nKINDLY RERUN THE PROGRAM")

    except mysql.connector.ProgrammingError as e:
        if errorcode.ER_PARSE_ERROR == e.errno:
            print("Kindly recheck your column parameters..")


## Defining a menu for performing tasks
def menu():
    choice = input("\nWHAT DO YOU WISH TO DO?: \n \n (1) DATABASE CREATION AND USAGE \n \n (2) DISPLAY AVAILABLE TABLES AND DATABASES \n \n (3) TABLE CREATION AND MODIFICATION \n \n (4) INPUT RECORDS TO A TABLE \n \n (5) PRINT A TABLE \n \n PLEASE ENTER ONLY THE OPTION AS PER CHOICE WITHOUT BRACKETS -->")

    if choice == '1':
        
        x1 = input("(a) CREATE A DATABASE \n \n(b) USE A DATABASE \n \n(c) DROP A DATABASE-->")

        if x1 == "a":
            database_create()

        elif x1 == "b":
            database_use() 
        elif x2 == "c":
            database_drop()


    elif choice == '2':
        x2 = input("(a) SHOW AVAILABLE DATABASES \n \n(b) SHOW AVAILABLE TABLES -->")
        if x2 == "a":
            database_show()

        elif x2 == "b":
            tables_show()


    elif choice == '3':
        x3 = input("(A) CREATE A TABLE \n \n(B) MANIPULATE A TABLE \n \n(C) DELETE A TABLE-->")
        if x3 == "a":
            table_creator()

        elif x3 == "b":
            y1 = input("(a) ADD AN ATTRIBUTE \n \n(b) DELETE AN ATTRIBUTE \n \n(c) MODIFY AN ATTRIBUTE -->")
            if y1 == "a":
                column_add()

            elif y1 == "b":
                column_del()

            elif y1 == "c":
                column_modify()
        elif x3 == "c":
            table_del()

    elif choice == '4':
        inputer()


    elif choice == '5':
        print_table()


    else:
        print("INVALID SELECTION")

## Initiating the program
print('Pydbms Beta 2.0 \nAUTHOR: ARASHDEEP SINGH \nWELCOME, THIS IS A DBMS BASED ON PYTHON CONNECTOR \nREQUIREMENTS: MySQL INSTALLED ALONG WITH PYTHON CONNECTOR COMPONENTS \nFor any furthur query ,CONTACT: mangoshake5888@gmail.com  ')

option = 'y'
while option == 'y':
    menu()

    option = input("\nDO YOU WANT TO CONTINUE? \n y or n: ")

    if option == 'n':
        print("\nFine, Have a nice day")

        quit()
