from database_creation import Database_Creation_Admin


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