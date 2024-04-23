from connection import Connection
from database_creation import Database_Creation_Admin
from admin_login import Admin_Login
from admin_portal_cataegory import Admin_Work
from admin_specific_product import Specific_Brand_Work_Admin
from admin_main_page import Admin_Main_Page






# craeting instances of class
connection=Connection()
database=Database_Creation_Admin()
admin_login=Admin_Login()
admin_portal=Admin_Work()
specific_brand=Specific_Brand_Work_Admin()
admin_main_page = Admin_Main_Page()

# making connections
connection.create_connection()
database.create_database()
database.create_table_for_cataegory()


# main function
def main():
    print("\n\t\tWelcome To Mobile Hub.")
    # loop to stuck
    while True:
        # display choice to admin
        print("\t1.Login As Mobile-Hub Admin.")
        print("\t2.Exit From Application.\n")
        
        # Taking choice by admin
        choice=input("Enter Your Choice in Mobile-Hub:").strip()

        # calling respective mehtods
        if choice=="1":
            admin_main_page.main_page_Admin()  # Call the main page method
        elif choice=="2":
            print("Mobile-Hub Is Exiting Now..\n")
            database.close_connection() # close the connection of database
            return
        # when wrong choice
        else:
            print("Invalid choice in Mobile-Hub.Please Seelect From Given Choice\n")

main()   # call main function
    