# Module Imports
import mariadb
import sys
import json
import os
class Database:
     
     def __init__(self):
          with open('/home/pi/Documents/Python Projects/Completed Login App/Json File/Database.json') as jFile:
               data = json.load(jFile) #load data into users dictionary
               databaseCredentials = data['database'] 
          # Connect to MariaDB Platform
          try:
               self.connection = mariadb.connect(
               user = databaseCredentials['username'],
               password = databaseCredentials['password'],
               host = databaseCredentials['host'],
               database = databaseCredentials['database']
          )
          except mariadb.Error as e:
               print(f"Error connecting to MariaDB Platform: {e}")
               sys.exit(1)
          # Get Cursor
          self.cursor = self.connection.cursor()
     
     #This method executes a query
     '''Try block executes the for loop to check if the query return a result set.
     If it doesn't return a result set, then an exception is thrown to prevent an error.'''
     def SQLExecute(self, query):
          x = None
          self.cursor.execute(query)
          try:
               for x in self.cursor:
                    return x
          except mariadb.Error as b:
               return x
               
     #Tis method commits changes to the database
     def SQLCommit(self):
          self.connection.commit()

     
          
     