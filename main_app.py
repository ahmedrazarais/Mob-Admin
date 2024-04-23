
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
            print("\nYou must update sever_details.py file for access the system.\n")
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

# class for admin login
class Admin_Login(Database_Creation_Admin):
    def __init__(self):
        self.admin_username = "admin"    # Admin username
        self.admin_password = "admin123"   # admin password
        super().__init__()
        # Admin login


    def admin_login(self):
        # Ask the user for the username and password
        while True:
            username = input("Enter Admin Username (enter 0 to back): ")
            if username == "0":
                return
            # Check if the username is correct
            if username == self.admin_username:
                break
            else:
                print("Incorrect Username")
                print()
        # when username is correct then ask for password
        while True:
                password = input("Enter Admin Password (enter 0 to back): ")
                if password == "0":
                    return
                
                # Check if the password is correct
                if password == self.admin_password:
                    print("Login Successful!!")
                    print()
                    return "login"
                else:
                    print("Incorrect Password")
                    print()
        
# class for cataegory adding by admin
class Admin_Work(Admin_Login):
    def __init__(self):
        self.brand_table=""
        super().__init__()
    
    
    # mehtod to fetch data from cataegory table
    def fetch_data_from_cataegory_table(self):
        try:
         
            self.create_connection()
            self.cursor.execute(f"USE {self.database}")
            
            self.cursor.execute("SELECT * FROM cataegory")
            data = self.cursor.fetchall()
         
            self.connection.commit()
            return data
        except mysql.connector.Error as e:
            print(f"Error in fetching data: {e}")
             


    
    # mehtod to insert id and cataegory in cataegory input
    def insert_brand_in_table(self,id,brand):
        try:
            self.create_connection()
            self.cursor.execute(f"USE {self.database}")
            query="INSERT INTO cataegory (id,brand) VALUES (%s,%s)"
            self.cursor.execute(query,(id,brand))
            self.connection.commit()
            print(f"\nCongratulations Brand name {brand} With Id {id} Added Successfully.\n")
        except mysql.connector.Error as e:
            print(f"Error In inserting data {e}")
    
    # asking for id from admin
    def id_input_from_admin(self):
        # calling this to fetch dara from cataegory table
        brand_data=self.fetch_data_from_cataegory_table()
        while True:
            try:
                id_input=int(input("Enter Brand Id To Assign (enter 0 to go back):"))

                # idf want to go back
                if id_input==0:
                    return
                
            
                # if less than zero
                if id_input<0:
                    print("Id must not be exceed from four nonnegative digits\n")
                    continue
                
                # checking brand id nmust be unique
                if brand_data:
                    id_exist=any(id_[0]==id_input for id_ in brand_data)
                    if id_exist:
                        print("This id already assign to another brand name.Select another\n")
                        continue

                # when getting all valid input then return for further use
                print("Brand-Id Assign Successfully.\n") 
                return id_input
            # if not in digits
            except ValueError:
                print("Please Enter in digit.Id must be in digit.\n")


    # mehtod to take brand name input
    def brand_name_input(self):
        #  # calling this to fetch dara from cataegory table
        brand_data=self.fetch_data_from_cataegory_table()
        while True:
            brand_name=input("Enter Brand Name to Added To Mobile-Hub (enter 0 to back):").strip().lower()
            # if he want bto go back
            if brand_name=="0":
                return
            # checking cataegory name must not be repeate because we make table of ctaaegory name
            if brand_data:
                brand_name_exist=any(brand==brand_name for _,brand in brand_data)
                if brand_name_exist:
                    print("This brand is already in your Mobile-Hub.Select another.\n")
                    continue # if name matches

            # if gettig no input
            if not brand_name:
                print("Brand Name is complusory to set.\n")
                continue
            
            # return when valid input
            print("Brand-Name Added Successfully.\n")
            return brand_name


    # mehtod to process id and brand name
    def adding_cataegory_process(self):
        # calling respective mehtods and check that each mehtod give input then write in tbale
        id=self.id_input_from_admin()
        if id:
            brand=self.brand_name_input()
            if brand:
                # call insert table mehtod to write in table
                self.insert_brand_in_table(id,brand)
                print("wait Going To Previous Options\n")        
            # when not get input
            else:
                print("Getting no brand-name..Going To previous menu.\n")
        # when not get input
        else:
            print("Getting no id..Going To previous menu.\n")
        
    

    # mehtod to display all brand name along with ids
    def display_brands_to_admin(self):
        # calling this to fetch data
        brand_details=self.fetch_data_from_cataegory_table()
        # check must be any cataegory added
        if brand_details:
            print("\n\t\tMobiles Cataegories Details")
            print("-"*60)
            print("Brand-Id\t\tBrand-Name")
            # iterate over 2d data
            for id,brand in brand_details:
                print(f"{id}\t\t\t{brand}")
            print()
        # if no cataegfory added yet
        else:
            print("\nMobile-hub is Empty at This Moment Nothing to Display.")
            print("come back later.\n")
    

    # mehtod to write delete query
    def delete_query_for_brand_deletion(self,id_input):
        try:
           self.create_connection()
           self.cursor.execute(f"USE {self.database}")
           query=("DELETE FROM cataegory WHERE id=%s")
           self.cursor.execute(query,(id_input,))
           print("\nBrand With That Id Is Deleted Successfully.\n")
           self.connection.commit() # commit the change
        
        except mysql.connector.Error as e:
            print(f"Error in deletion: {e}")

    # delete any brand details
    def delete_brand_from_table(self):
        # calling this mehtod to fetch data
        brand_details=self.fetch_data_from_cataegory_table()
        if brand_details:
              while True:
                # display cataegories to admin
                self.display_brands_to_admin()
                try:
                    id_input=int(input("Enter Brand Id To Delete (enter 0 to go back):"))
                    if id_input==0:
                        print("Going Back From Delete Option.\n")
                        return
                    found=False
                    for id,_ in brand_details:
                        if id_input==id:
                            found=True
                    # check if id orf roww matches so delete the row/cataegorey
                    if found:
                        self.delete_query_for_brand_deletion(id_input)
                        print("For More Details Visit Display Option.\n")
                        return
                    # if not id found
                    if not found:
                        print("Brand-Id Not Found please Enter Correct id foir deletion\n")
                # if not get in digits
                except ValueError:
                    print("Please Enter in digit.Brand-Id is in digits\n")
        # if database isd empty/no cataegory added indication
        else:
            print("\nMobile-hub is Empty at This Moment Can't Delete Anything at this moment.\n")

        
    

        


    
    
# making class for admin to work on specific product
class Specific_Brand_Work_Admin(Admin_Work):
    def __init__(self):
        self.brand_table=""    # initial take it empty later assign with table name 
        super().__init__()

    #mehtod to create table to hold mobiles details
    def create_table_for_mobile(self):
        try:
            self.create_connection()
            self.cursor.execute(f"USE {self.database}")
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.brand_table} (
                id INT PRIMARY KEY,
                name VARCHAR(50),
                price INT NOT NULL,
                quantity INT
                )""")
            self.connection.commit()
        # getting error
        except mysql.connector.Error as e:
            print(f"Error on line 292 as {e}")

    # make mehtod to insert in mobile table
    def insert_in_mobile_table(self,id,name,price,quantity):
        try:
            self.cursor.execute(f"USE {self.database}")
            # write querey to insert data
            query=f"INSERT INTO {self.brand_table} (id,name,price,quantity) VALUES (%s,%s,%s,%s)"
            self.cursor.execute(query,(id,name,price,quantity))
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error in inserting data in table {e}")

    # fetching data from mobile data
    def fetch_data_from_mobile_table(self):
        try:
            self.create_connection()
            self.cursor.execute(f"USE {self.database}")
            query=f"SELECT * FROM {self.brand_table}"
            self.cursor.execute(query)
            data=self.cursor.fetchall()
            return data # return 2d data 
        except mysql.connector.Error as e:
            print(f"Error in fetching data {e}")

      # asking for id from admin
    def id_from_admin(self):
        # calling fetch data mehtod to fetch data
        brand_data=self.fetch_data_from_mobile_table()
        while True:
            try:
                id_input=int(input("Enter Brand Id To Assign (enter 0 to go back):"))
               
                # if he want to go back
                if id_input==0:
                    return
                
            
                # if id getting less than zero
                if id_input<0:
                    print("Id must not be exceed from four nonnegative digits\n")
                    continue
                
                # check existence that id must not repeat primary key
                if brand_data:

                    id_exist=any(id_[0]==id_input for id_ in brand_data)
                    if id_exist:
                        print("This id already assign to another brand name.Select another\n")
                        continue
                # if all valid input return id
                print("Mobile-Id Assign Successfully.\n") 
                return id_input
        
            except ValueError:
                print("Please Enter in digit.Id must be in digit.\n")


    
    # Method to take mobile name input
    def mobile_name_input(self):
        while True:
            mobile_name = input(f"\nEnter Mobile Name To add in {self.brand_table} cataegory (enter 0 to go back): ").strip()
            if mobile_name == "0":
                return None  # Return None if user wants to go back

            # Check if mobile name is not empty and contains at least one alphabet
            if mobile_name and any(char.isalpha() for char in mobile_name):
                return mobile_name
            else:
                print("Mobile Name is mandatory and should contain at least one alphabet.")
    
    # Method to take price input
    def price_input(self):
        while True:
            price_str = input("\nEnter Price for the mobile (enter 0 to go back): ").strip()
            if price_str == "0":
                return None  # Return None if user wants to go back
            
            # Check if input is a valid integer
            try:
                price = int(price_str)
                if price >= 0:
                    return price
                else:
                    print("Price should be a non-negative integer.")
            except ValueError:
                print("Invalid input. Please enter a valid price.")
    

    # Method to take quantity input
    def quantity_input(self):
        while True:
            quantity_str = input("\nEnter Quantity for the mobile (enter 0 to go back): ").strip()
            if quantity_str == "0":
                return None  # Return None if user wants to go back
            
            # Check if input is a valid integer
            try:
                quantity = int(quantity_str)
                if quantity >= 0:
                    return quantity
                else:
                    print("Quantity should be a non-negative integer.")
            except ValueError:
                print("Invalid input. Please enter a valid quantity.")
    
    # main adding mobile process
    def add_mobile_in_cataegory(self):
       # calling respective mehtods check that if getting nput then proceed further

        id=self.id_from_admin()
        if id:
            name=self.mobile_name_input()
            if name:
                price=self.price_input()
                if price: # check every mehtod return something if not then break
                    quantity=self.quantity_input()
                    if quantity:
                        # when get all input then call insert data mehtod to insert data
                        self.insert_in_mobile_table(id,name,price,quantity)
                        print(f"Mobile Added Successfully In {self.brand_table} Cataegory")
                        print("For More Details visit Display mobiles option.\n")
                        return
                    # when go back
                    else:
                        print("Going Back To previous menu.\n")
                # when go back
                else:
                    print("Going Back To previous menu.\n")
            else:
                print("Going Back To previous menu.\n")
        else:
            print("Going Back To previous menu.\n")

    # mehtod to display all mobile phones
    def display_mobile_to_admin(self):
        # calling this to check data 
        brand_details=self.fetch_data_from_mobile_table()

        # check if data or not in mobile table
        if brand_details:
            # if data then print it
            print(f"\n\t\t{self.brand_table} Mobile-Phones Details")
            print("-"*100)
            print("Mobile-Id\t\tMobile-Name\t\t\tPrice\t\tQuantity")
            for id,brand,price,quantity in brand_details:
                print(f"{id}\t\t\t{brand}\t\t\t{price}\t\t{quantity}")
            print()
        # if not getting data printthe message
        else:
            print("\nMobile-hub is Empty at This Moment Nothing to Display.")
            print("come back later.\n")    
    
    # mehtod to delete mobile from cataegory
     # mehtod to write delete query
    def delete_query_for_mobile_deletion(self,id_input):
        try:
           self.create_connection()
           self.cursor.execute(f"USE {self.database}")
           query=(f"DELETE FROM {self.brand_table} WHERE id=%s")
           self.cursor.execute(query,(id_input,))
           print(f"\nMobile With That Id Is Deleted Successfully From {self.brand_table} Cataegory.\n")
           self.connection.commit()

        except mysql.connector.Error as e:
            print(f"Error in deletion: {e}")

    def delete_mobile_from_table(self):
        # calling mehtofd to check data
        brand_details = self.fetch_data_from_mobile_table()
        # if data then ask for id to delte that data
        if brand_details:
            while True:
                self.display_mobile_to_admin()
                try:
                    # asking for id
                    id_input = input("Enter Mobile Id To Delete (enter 0 to go back):").strip()

                    # if want to go back
                    if id_input == "0":
                        print("Going Back From Delete Option.\n")
                        return
                    
                    if id_input.isdigit():  # Check if input consists only of digits
                        id_input = int(id_input)
                        found = False
                        # check for id in table
                        for id in brand_details:
                            if id[0]==id_input:
                                found = True
                                break
                        # if id found then call delete query
                        if found:
                            self.delete_query_for_mobile_deletion(id_input)
                            print("Mobile With That Id Is Deleted Successfully.\n")
                            return
                        # if id not found
                        else:
                            print("Mobile-Id Not Found. Please Enter Correct id for deletion.\n")
                    # if not getting in digits
                    else:
                        print("Please Enter a valid digit for Mobile-Id.\n")
                # if bnot getting in digits
                except ValueError:
                    print("Please Enter a valid digit for Mobile-Id.\n")
        # when database is empty/no mobile in cataegory
        else:
            print("\nMobile-hub is Empty at This Moment Can't Delete Anything at this moment.\n")

        # Method to update mobile name
    def update_name(self, id, name):
        try:        # use try except to avoid conflicts
            self.create_connection()
            self.cursor.execute(f"USE {self.database}")
            query = f"UPDATE {self.brand_table} SET name=%s WHERE id=%s"
            self.cursor.execute(query, (name, id))
            self.connection.commit()    # commit the change
            print("Update has been made successfully.")
        except mysql.connector.Error as e:
            print(f"Error as {e}")

    # Method to update mobile price
    def update_price(self, id, price):
        try:
            self.create_connection()
            self.cursor.execute(f"USE {self.database}")
            query = f"UPDATE {self.brand_table} SET price=%s WHERE id=%s"
            self.cursor.execute(query, (price, id))
            self.connection.commit()
            print("Update has been made successfully.")
        except mysql.connector.Error as e:
            print(f"Error as {e}")

    # Method to update mobile quantity
    def update_quantity(self, id, quantity):
        try:
            self.create_connection()
            self.cursor.execute(f"USE {self.database}")
            query = f"UPDATE {self.brand_table} SET quantity=%s WHERE id=%s"
            self.cursor.execute(query, (quantity, id))
            self.connection.commit()
            print("Update has been made successfully.")
        except mysql.connector.Error as e:
            print(f"Error as {e}")

    # Method to update mobile details
    def update_mobile_details(self):
        # call the fetch one to check data
        data = self.fetch_data_from_mobile_table()
        # if data /mean mobile in data
        if data:
            while True:
                self.display_mobile_to_admin()
                #ask for id to stuck in loop
                try:
                    id_input = int(input("Enter Mobile Id To Update (enter 0 to go back):"))
                    # if want to go back
                    if id_input == 0:
                        print("Going Back From Update Option.\n")
                        return
                    found = False
                    # iterate over data to find key
                    for id in data:
                        if id[0] == id_input:
                            found = True
                    break
                # if not get in diogits
                except ValueError:
                    print("Please Enter In Digits.\n")
            # if id found stuck him in loop till hewant to back
            if found:
                print("\t\tWelcome in update area")
                while True:
                    # display update options
                    print("\t1.Update Mobile Name.")
                    print("\t2.Update Mobile Price.")
                    print("\t3.Update Mobile Quantity.")
                    print("\t4.Exit From Update Area.\n\n")

                    # asking update chopice
                    update_choice = input("Enter Your Choice You want to update:")

                    # calling update choice
                    if update_choice == "1":
                        name=self.mobile_name_input()
                        if name:   # check must have input
                            self.update_name(id_input,name)
                            self.display_mobile_to_admin()

                    # calling respective mehtod ob desired choice
                    elif update_choice == "2":
                        price = self.price_input()  
                        if price:
                            self.update_price(id_input, price)
                            self.display_mobile_to_admin()

                    elif update_choice == "3":
                        quantity = self.quantity_input() 
                        if quantity:
                            self.update_quantity(id_input, quantity)
                            self.display_mobile_to_admin()

                    # if he want to go back from update
                    elif update_choice == "4":
                        print("Back From Update Area..\n")
                        return
                    # if invlaid choice in update
                    else:
                        print("Invalid Update Choice. Please Select From Given Choice\n")
            # if no data/no mobile added yet in cataeogory
            else:
                print(f"{self.brand_table} Category is empty at this moment. Can't Update Anything At this moment.\n")

    # main page for specif_products_operations
    def specifc_product_operation(self):
        # calling the fetch data mehtod to check whether the cataegories are not
        data=self.fetch_data_from_cataegory_table()
        if data:
            while True:
                try:
                    self.display_brands_to_admin()
                    id_input=int(input("Enter Brand-Id You Want to perform operations (enter 0 to back):"))
                    #if wantb to go back
                    if id_input==0:
                        print('Going Back To previous Menu..\n')
                        return
                    # initial it as false
                    id_found=False
                    # iterate to check id
                    for id,brand in data:
                        if id==id_input:
                            self.brand_table=brand
                            id_found=True
                    break
                # if getting wrong input
                except ValueError:
                    print("Please Enter In Digits e.g=1,2\n")

            # apply loop when id found
            while True:
                    if id_found:
                        self.create_table_for_mobile() # craeting tables for mobiles
                        # display options
                        print(f"\t\tWelcome in {self.brand_table} Brand-Cataegory")
                        print(f"\t1.Add Mobiles To {self.brand_table} Cataegory.")
                        print(f"\t2.View Mobiles From {self.brand_table} Cataegory.")
                        print(f"\t3.Delete Mobiles From {self.brand_table} Cataegory.")
                        print(f"\t4.Update Mobile Details In {self.brand_table} Cataegory.")
                        print("\t5.Back To main Portal\n\n")

                        #choice 
                        option=input(f"Enter Your Option What you want to do in {self.brand_table} cataegory: ").strip()
                        if option=="1":
                            self.add_mobile_in_cataegory()
                        elif option=="2":
                            self.display_mobile_to_admin()
                        elif option=="3":
                            self.delete_mobile_from_table()
                        elif option=="4":
                            self.update_mobile_details()
                        elif option=="5":
                            print("Back To Administation Portal.\n")
                            return
                        else:
                            print("Invalid Choice Please Select From Given choices.\n")

                    # invalid choice
                    else:
                        print("Invalid Brand-Id No Id found.\n")
                        break

        # when no data/no mobile added yet
        else:
            print("Mobile-Hub Is empty.You Not Add Any cataegory yet.can't Access this option\n")
    

    
    
        

    


# class for main page of admin
class Admin_Main_Page(Specific_Brand_Work_Admin):
    def __init__(self):
        super().__init__()

    
    # mehtod to display main page
    def main_page_Admin(self):
        #call admin login function from parenmt class to check that he must login to get all operations
        login_check=self.admin_login()
        if login_check:
            # when admin login succesfull
            while True:
                # display him options
                print("\n\t\tWelcome To Administaration Portal.\n")
                print("\t1.View All Mobile Cataegories You added.")
                print("\t2.Add Mobile Cataegory To Mobile-Hub.")
                print("\t3.Delete Any Cataegory From Mobile-Hub.")
                print("\t4.Perform Operations On specific cataegory.")
                print("\t5.Exit From Administration portal.\n\n")
                # taking choice by admin
                admin_choice=input("Dear Admin Please Enter Your Choice:").strip()

                # calling respective mehtods now
                if admin_choice=="1":
                    self.display_brands_to_admin()
                elif admin_choice=="2":
                    self.adding_cataegory_process()
                elif admin_choice=="3":
                    self.delete_brand_from_table()
                elif admin_choice=="4":
                    self.specifc_product_operation()
                # if he want to exit
                elif admin_choice=="5":
                    print("\nExiting From Administration Area..")
                    print("See You Soon.")
                    return
                # when invalid choice
                else:
                    print("\nInvalid choice.Please Enter Valid Choice\n")
        # when login attempt fail
        else:
            print("Admin Login Attempt Failed.Must Login To Perform Operations.")
            
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
    
