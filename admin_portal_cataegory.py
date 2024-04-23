import mysql.connector
from admin_login import Admin_Login



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
            query="SELECT * FROM cataegory"
            self.cursor.execute(query)
            data=self.cursor.fetchall()
            return data
        except mysql.connector.Error as e:
            print(f"Error in fetching data {e}")
    
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

        
    