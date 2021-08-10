from Hash import Hash 
from Salt import Salt
from MySQLConnection import Database
from Password import Password

#This method obtains the salt stored in the database for the especified user
'''fetchData contains the result set, which is returned in form of a tuple'''
def obtainSalt(dbObj, username):
    fetchData = dbObj.SQLExecute(f'SELECT salt FROM users WHERE username = \'{username}\'')
    #if fetchData has a result set, then salt equals the value in the result set
    if fetchData != None:
        salt = fetchData[0]
        return salt
    #else if no result set available, then return empty string
    else:
        return ""

#This method calls a function to generate a salt
def saltFunction():
    saltObj = Salt()
    salt = saltObj.saltingFunction()
    return salt

#This method call a function to hash the password
def hashPassword(password, salt):
    #create object from class hash
    hashObj = Hash(password)
    #obtains hashed password
    password = hashObj.hashFunction(salt)
    return password

#This method validates credentials of users 
'''Checks if username and password provided matches the records in the database.
'''
def validate_credentials(username, password, dbObj):
    #existingUser is initialized to a result set, if there is no result set then the user was not found in the database
    existingUser = dbObj.SQLExecute(f'SELECT username FROM users WHERE username = \'{username}\' and passwordHash = \'{password}\'')
    if existingUser != None:
        print("Credentials accepted")
    else:
        while existingUser == None:
            print("The credentials given appear to be incorrect. Please enter your credentials below")
            username = input("Username:")
            password = input("Password:")
            print()
            salt = obtainSalt(dbObj, username)
            #salt is converted from hex() to its original value
            salt = bytes.fromhex(salt)
            password = hashPassword(password, salt)
            existingUser = dbObj.SQLExecute(f'SELECT username FROM users WHERE username = \'{username}\' and passwordHash = \'{password}\'')
        print("Credentials accepted")

#This method creates a new user
def createAccount(username, password, dbObj, salt, valid, passObj):
    #checkUsername is initialized to a result set, if there is no result set then the user was not found in the database
    checkUsername = dbObj.SQLExecute(f'SELECT username FROM users WHERE username = \'{username}\'')

    #if checkUsername == None, then there isn't a user with the give username
    #if valid = 0, password meets requirements
    if valid == 0 and checkUsername == None:
            dbObj.SQLExecute(f'INSERT INTO users (username, passwordHash, salt) VALUES (\'{username}\', \'{password}\', \'{salt}\')')
            dbObj.SQLCommit()
            print("Account was created")
    else:
        passTest = False
        while passTest == False:
            if checkUsername != None:
                print("\nUsername already taken.")
            elif valid != 0:
                print("Password does not meet the requirements.")
            print("Enter a new username and password:")
            print("Password Requirements:\n"
            + "-Must be at least 8 characters long\n"
            + "-Must contain at least 1 special character('_','@','$')\n"
            + "-Must have at least 1 uppercase letter\n"
            + "-Must contain at least 1 number (0-9)")
            username = input("Username:")
            password = input("Password:")
            print("")
            valid = passObj.validatePassword(password)
            salt = saltFunction()
            password = hashPassword(password, salt)
            #salt is turned into hexadecimal value, and returned as a string
            salt = salt.hex()
            checkUsername = dbObj.SQLExecute(f'SELECT username FROM users WHERE username = \'{username}\'')
            if valid == 0:
                if checkUsername == None:
                    passTest = True

        dbObj.SQLExecute(f'INSERT INTO users (username, passwordHash, salt) VALUES (\'{username}\', \'{password}\', \'{salt}\')')
        dbObj.SQLCommit()
        print("Account was created")

#This method checks that user selects correct options
def checkOptions(option):
        accepted = False
        while accepted == False: #check that user chooses option 1, 2 or 3
            try:
                if option == 1 or option == 2 or option == 3 or option == 4:
                    accepted = True
                    continue
                print("\nEntered option is not available. Please choose one of the options: Enter 1 to login, 2 to create an account, 3 to delete account, or 4 to change password")
                option = int(input("Enter your option: "))
                print("")
            except ValueError:
                continue
        return option

#This method deletes an account
def deleteAccount(username, dbObj):
    dbObj.SQLExecute(f'DELETE FROM users WHERE username = \'{username}\'')
    dbObj.SQLCommit()
    return dbObj.cursor.rowcount

def changePassword(username, newPassword, dbObj):
    dbObj.SQLExecute(f'UPDATE users SET passwordHash = \'{newPassword}\' WHERE username = \'{username}\'')
    dbObj.SQLCommit()
    return dbObj.cursor.rowcount

#create a database object
dbObj = Database()

option = ""
#if user input is other than int() throw exception
try:
    print("Welcome user. Please choose one of the following options: Enter 1 to login, 2 to create an account, 3 to delete account, or 4 to change password")
    option = int(input("Enter your option: "))
    print("")
    option = checkOptions(option)
except ValueError:
    option = checkOptions(option)
    

if option == 1: #login option
    print("Please enter your login credentials below")
    username = input("Username:")
    password = input("Password:")
    print("")
    salt = obtainSalt(dbObj, username)
    #salt is converted from hex() to its original value
    salt = bytes.fromhex(salt)
    password = hashPassword(password, salt)
    validate_credentials(username, password, dbObj)

elif option == 2: #create account option
    print("Let's create your account. Fill out the form below to complete your account.")
    print("Password Requirements:\n"
    + "-Must be at least 8 characters long\n"
    + "-Must contain at least 1 special character('_','@','$')\n"
    + "-Must have at least 1 uppercase letter\n"
    + "-Must contain at least 1 number (0-9)")
    username = input("Username:")
    password = input("Password:")
    print("")
    passObj = Password()
    valid = passObj.validatePassword(password)
    salt = saltFunction()
    password = hashPassword(password, salt)
    #salt is turned into hexadecimal value, and returned as a string
    salt = salt.hex()
    createAccount(username, password, dbObj, salt, valid, passObj)

elif option == 3: #delete account  
    print("To delete your account, please enter your credentials below")
    username = input("Username:")
    password = input("Password:")
    salt = obtainSalt(dbObj, username)
    #salt is converted from hex() to its original value
    salt = bytes.fromhex(salt)
    password = hashPassword(password, salt)
    validate_credentials(username, password, dbObj)
    deleted = deleteAccount(username, dbObj)
    if deleted == 1:
        print("Account has been deleted")

elif option == 4: #change password
    print("To change your password, please enter your login credentials below")
    username = input("Username:")
    password = input("Password:")
    print("")
    salt = obtainSalt(dbObj, username)
    #salt is converted from hex() to its original value
    salt = bytes.fromhex(salt)
    password = hashPassword(password, salt)
    validate_credentials(username, password, dbObj)

    valid = 1
    passObj = Password()
    while valid != 0:
        print("Password Requirements:\n"
        + "-Must be at least 8 characters long\n"
        + "-Must contain at least 1 special character('_','@','$')\n"
        + "-Must have at least 1 uppercase letter\n"
        + "-Must contain at least 1 number (0-9)")
        print("")
        newPassword = input("Enter new password:")
        print("")
        valid = passObj.validatePassword(newPassword)
        if valid != 0:
            print("Password doesn't meet requirements")
    newPassword = hashPassword(newPassword, salt)
    changed = changePassword(username, newPassword, dbObj)
    if changed == 1:
        print("Password has been changed")