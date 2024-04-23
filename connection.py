
# importing mysql connector and database password user from server details.py file

import mysql.connector
from config import db_host,db_password,db_user


# creating a  class for server connection
class Connection:
    def __init__(self):
        self.cursor=None       # makig instances for further use in any class
        self.connection=None
      
    # making method for making connection
    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password
            )
            self.cursor = self.connection.cursor()  # Assign cursor object to self.cursor
     
        except mysql.connector.Error as e:
            print("\nYou must update config.py file for access the system.\n")
            exit()
   
    # mehtod for closing connection
    def close_connection(self):
        # Close database connection
        try:
            if self.connection.is_connected():
                self.cursor.close()        # close the connection
                self.connection.close()
                print("Connection to MySQL database closed.")
        except mysql.connector.Error as e:
            print(f"Error closing connection: {e}")