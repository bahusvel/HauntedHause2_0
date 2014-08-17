__author__ = 'denislavrov'

import sqlite3

DATABASE = 'test.db'


def createtable(filename=''):  # function called to insert a table into a new database
    conn = sqlite3.connect(filename)  # opening/connecting to a database just like a file
    conn.execute('''CREATE TABLE SAVE
       (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
       SAVENAME TEXT    NOT NULL,
       INV_TNAME TEXT     NOT NULL,
       LOC_TNAME TEXT  NOT NULL
       );
       ''')
    conn.close()


def createdb(filename=''):  # this function actually creates a physical file, for database to be stored in
    if filename == '':  # since some functions may be used just to reuse code they have keys to avoid user input
        while (len(filename) == 0) or (filename[len(filename) - 3:len(filename)] != '.db'):
            # check that input is not emtpy and ends with .db
            filename = input("Please enter a filename that ends with '.db': ")
    try:  # check if database exists by trying to open it for reading
        open(filename, mode='r')  # if file exists the following code is not run and jump to 'except:' is made.
        while 1:  # if database does exist ask user if he would like to switch to it
            useri = input("This database already exists. Would you like to switch to it? [Y,N]: ").lower()
            if useri == 'y':
                switchdb(filename=filename)  # invoke function to switch
                break
            elif useri == 'n':  # if user chooses not to switch send him back recursively,by calling this function again
                createdb()
                break
    except IOError:  # if file does not exist, then create it, create the table in it and switch to it.
        open(filename, mode='a').close()  # a quick way to create an empty file in one line.
        createtable(filename=filename)
        switchdb(filename=filename)


def switchdb(filename=''):  # a function to switch databases
    while 1:
        if filename == '':  # check for a preset key as usual if not set ask user for input
            filename = input("Please input a valid existing database name: ")
        try:  # try to open database for reading just to check that the file is there
            file = open(filename, mode='r')
        except IOError:
            print("Error switching the database.")
        else:  # no exception raised everything is fine, set that database to current database and reset current user
            global DATABASE
            DATABASE = filename
            file.close()
            break


def insertuser(username):  # little function to insert a new user into the database
    conn = sqlite3.connect(DATABASE)
    inv_tname = 'inv_' + username
    loc_tname = 'loc_' + username
    conn.execute("INSERT INTO SAVE (SAVENAME, INV_TNAME, LOC_TNAME) \
    VALUES ('%s','%s','%s')" % (username, inv_tname, loc_tname))
    conn.commit()
    conn.execute('''CREATE TABLE %s
       (ITEM_ID INTEGER  NOT NULL
       );
       ''' % inv_tname)

    conn.execute('''CREATE TABLE %s
       (LOC_ID INTEGER  NOT NULL
       );
       ''' % loc_tname)

    conn.close()


def save(inventory, visitedLocations):
    savename = input('Please input a savename: ')
    if savename != '' and not userexists(savename):
        insertuser(savename)
        conn = sqlite3.connect(DATABASE)
        for inv in inventory:
            conn.execute("INSERT INTO %s (ITEM_ID) \
    VALUES (%d)" % (get_inv_tname(savename), inv))
            conn.commit()

        for loc in visitedLocations:
            conn.execute("INSERT INTO %s (LOC_ID) \
    VALUES (%d)" % (get_loc_tname(savename), loc))
            conn.commit()
        conn.close()
    else:
        print('That save name is either invalid or already exists')


def checkdb(db, create=False):  # helper function to check if database exists
    # could be expanded to check data inside database
    try:
        open(db, mode='r').close()
        return True
    except IOError:
        print("Database %s does not exist, please create one." % db)
        if create:
            createdb()
        else:
            return False


def readusers():  # read the users in from the database
    conn = sqlite3.connect(DATABASE)
    rows = conn.execute("SELECT SAVENAME FROM SAVE")
    lrows = list([x[0] for x in rows])
    conn.close()
    return lrows


def readinv(savename):  # read the users in from the database
    conn = sqlite3.connect(DATABASE)
    rows = conn.execute("SELECT ITEM_ID FROM %s" % ('inv_' + savename))
    lrows = list([x[0] for x in rows])
    conn.close()
    return lrows


def readloc(savename):  # read the users in from the database
    conn = sqlite3.connect(DATABASE)
    rows = conn.execute("SELECT LOC_ID FROM %s" % ('loc_' + savename))
    lrows = list([x[0] for x in rows])
    conn.close()
    return lrows


def rmuser(username=''):  # function to remove a user
    global cUser
    if username == '':
        username = input("Please enter username to remove: ")
    conn = sqlite3.connect(DATABASE)
    conn.execute("DELETE FROM SAVE WHERE SAVENAME='%s'" % username)
    conn.commit()  # must commit when making changes
    conn.close()
    if username == cUser:  # if current user is the user being deleted set current user to no one
        cUser = ''
    return username


def getid(username):  # helper function to getid of user by username
    conn = sqlite3.connect(DATABASE)
    uid = list(conn.execute("SELECT ID FROM SAVE WHERE SAVENAME='%s'" % username))[0][0]
    conn.close()
    return uid


def get_inv_tname(username):  # helper function to getid of user by username
    conn = sqlite3.connect(DATABASE)
    uid = list(conn.execute("SELECT INV_TNAME FROM SAVE WHERE SAVENAME='%s'" % username))[0][0]
    conn.close()
    return uid


def get_loc_tname(username):  # helper function to getid of user by username
    conn = sqlite3.connect(DATABASE)
    uid = list(conn.execute("SELECT LOC_TNAME FROM SAVE WHERE SAVENAME='%s'" % username))[0][0]
    conn.close()
    return uid


def userexists(username):  # helper function to check if the user exists
    conn = sqlite3.connect(DATABASE)
    rows = list(conn.execute("SELECT SAVENAME FROM SAVE WHERE SAVENAME='%s'" % username))
    conn.close()
    return rows.__contains__((username,))