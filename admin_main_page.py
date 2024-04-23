from admin_specific_product import Specific_Brand_Work_Admin



    


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