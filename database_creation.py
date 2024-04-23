from connection import Connection
import mysql.connector
# making a class for database creation and for table creation for holding accountsdetails
# inherits with connection class
class Database_Creation_Admin(Connection):
    def __init__(self):
        super().__init__()
        self.database="mobile"

    # making amehtod to create dabase name mobile
    def create_database(self):
        try:
            self.create_connection()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")

    # mehtod to create table for cataegories  that add by admin
    def create_table_for_cataegory(self):
        try:
            self.cursor.execute(f"USE {self.database} ")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS cataegory( 
                                id INT PRIMARY KEY,
                                brand VARCHAR (50))""")
         
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")