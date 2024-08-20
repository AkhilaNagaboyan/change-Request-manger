
import json
import datetime
from getpass import getpass

class ChangeRequest:
    def _init_(self, id, description, status='Pending'):
        self.id = id
        self.description = description
        self.status = status

class ChangeRequestManager:
    def _init_(self):
        self.change_requests = []
        self.users ={"deepa":"6143","admin":"Admin@123"}
        Users=self.users# Inbuilt usernames and passwords
        self.logged_in_user = None
        self.load_change_requests()

    def authenticate_admin(self, username, password):
        if username == 'admin' and self.users.get(username) == password:
            self.logged_in_user = username
            return True
        return False

    def authenticate_user(self, username, password):
        if username in self.users and self.users[username] == password:
            self.logged_in_user = username
            return True
        return False

    def add_change_request(self, description):
        if not self.logged_in_user:
            print("Authentication required. Please log in.")
            return
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        change_request_id = len(self.change_requests) + 1
        change_request = ChangeRequest(change_request_id, description)
        self.change_requests.append(change_request)
        print(f"Change Request #{change_request.id} added successfully by {self.logged_in_user}.")
        self.save_change_requests()

    def view_change_requests(self):
        if not self.logged_in_user:
            print("Authentication required. Please log in.")
            return

        if not self.change_requests:
            print("No change requests found.")
        else:
            print("\nChange Requests:")
            for change_request in self.change_requests:
                print(f"ID: {change_request.id}, Description: {change_request.description}, Status: {change_request.status}")

    def update_change_request_status(self, change_request_id, new_status):
        if not self.logged_in_user:
            print("Authentication required. Please log in.")
            return

        if self.logged_in_user != 'admin':
            print("Only admin can update the status.")
            return

        for change_request in self.change_requests:
            if change_request.id == change_request_id:
                change_request.status = new_status
                print(f"Change Request #{change_request.id} status updated to {change_request.status} by {self.logged_in_user}.")
                self.save_change_requests()
                return
        print(f"Change Request #{change_request_id} not found.")

    def delete_change_request(self, change_request_id):
        if not self.logged_in_user:
            print("Authentication required. Please log in.")
            return

        for change_request in self.change_requests:
            if change_request.id == change_request_id:
                self.change_requests.remove(change_request)
                f1=open("deleted_history","a+")
                f1.write("\n")
                com=((change_request.description)+" deleted by the user "+self.logged_in_user)
                f1.write(com)
                print(f"Change Request #{change_request_id} deleted successfully by {self.logged_in_user}.")
                self.save_change_requests()
                return
        print(f"Change Request #{change_request_id} not found.")

    def save_change_requests(self):
        with open('change_requests.json', 'w') as file:
            json.dump([vars(cr) for cr in self.change_requests], file)

    def load_change_requests(self):
        try:
            with open('change_requests.json', 'r') as file:
                data = json.load(file)
                self.change_requests = [ChangeRequest(cr['id'], cr['description'], cr['status']) for cr in data]
                print()
        except FileNotFoundError:
            # File not found, no previous data
            pass
    def New_user(self):
        self.new_name=input("Enter the name of new user to add:")
        self.new_pass=input("Enter the password of the user")
        self.new_user={self.new_name:self.new_pass}
        self.users.update(self.new_user)

# Example usage
if __name__ == "__main__":
    change_request_manager = ChangeRequestManager()
    while True:
        print("\nChange Request Manager Menu:")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")

        choice_login = input("Enter your choice (1/2/3): ")

        if choice_login == '1':
            admin_username = input("Enter admin username: ")
            admin_password = getpass("Enter admin password: ")
            if change_request_manager.authenticate_admin(admin_username, admin_password):
                print(f"Admin {admin_username} logged in.")
                while True:
                    print("\nAdmin Menu:")
                    print("1. View Change Requests")
                    print("2. Update Change Request Status")
                    print("3. view deleted history")
                    print("4. Add new user")
                    print("5. Logout\n")
                    admin_choice = input("Enter your choice (1/2/3/4/5): ")

                    if admin_choice == '1':
                        change_request_manager.view_change_requests()
                    elif admin_choice == '2':
                        change_request_manager.view_change_requests()
                        change_request_id = int(input("Enter change request ID to update status: "))
                        new_status = input("Enter new status: ")
                        change_request_manager.update_change_request_status(change_request_id, new_status)
                    elif admin_choice=='3':
                        f2=open("deleted_history","r")
                        con=f2.read()
                        print(con)
                        f2.close()
                    elif admin_choice == '4':
                        change_request_manager.New_user()
                    elif admin_choice == '5':
                        print("Logging out admin. Goodbye!")
                        break
                    else:
                        print("Invalid choice. Please enter a valid option.")
            else:
                print("Invalid admin credentials.")
        elif choice_login == '2':
            user_username = input("Enter user username: ")
            user_password = getpass("Enter user password: ")
            if change_request_manager.authenticate_user(user_username, user_password):
                print(f"User {user_username} logged in.")
                while True:
                    print("\nUser Menu:")
                    print("1. Add Change Request")
                    print("2. View Change Requests")
                    print("3. Delete Change Request")
                    print("4. Logout")
                    user_choice = input("Enter your choice (1/2/3/4): ")

                    if user_choice == '1':
                        description = input("Enter change request description: ")
                        change_request_manager.add_change_request(description)
                    elif user_choice == '2':
                        change_request_manager.view_change_requests()
                    elif user_choice == '3':
                        change_request_manager.view_change_requests()
                        change_request_id = int(input("Enter change request ID to delete: "))
                        change_request_manager.delete_change_request(change_request_id)

                    elif user_choice == '4':
                        print("Logging out user. Goodbye!")
                        break
                    else:
                        print("Invalid choice. Please enter a valid option.")
            else:
                 print("Invalid user credentials.")
        elif choice_login == '3':
            print("Exiting Change Request Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")