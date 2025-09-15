import sys

def user_exit():
    """Handles prematurely exiting the program
    """
    print("\nGoodbye!")
    return sys.exit()

def login_dict_function():
    """Handles populating the login dictionary
    """
    try:
        with open("user.txt", "r", encoding = "utf-8") as user_info:

            login_dict = {}

            # Populates login_dict with each user stored in users.txt
            for line in user_info:
                username, password = map(str.strip, line.split(", "))
                login_dict[username.lower()] = password
            # Returns the populated login dict
            return login_dict

    # Handles ending the program if the file cannot be found
    except FileNotFoundError as error:
        print("File cannot be found.")
        print(error)
        sys.exit()
    # Handles ending the program if a generic exception is detected
    except Exception as error:
        print("An unexpected error has occured.")
        print(error)
        sys.exit()

def user_auth(login_dict):
    """Handles log in logic
    """
    # Stores the remaining login attempts
    attempts = 3

    # Returns login_user when both inputs match their relevant tuple
    while attempts > 0:
        login_user = input("Please enter your username: ").lower()
        login_pass = input("Please enter your password: ")

        if login_user in login_dict and \
            login_pass == login_dict[login_user]:
            print("Access Granted!\n")
            return login_user

        # Negatively increments attempts variable if login is incorrect
        else:
            attempts -= 1
            print(f"Access Denied! {attempts} attempts remaining.\n")

    # Exits the program if all attempts are exhausted
    print("Too many failed attempts. Exiting.")
    sys.exit()

def new_user():
    """Handles inputting and verifying a new username.
    """
    add_user = input("\nInput New Username: ").lower()

    # Allows the user to prematurely exit
    if add_user == "e":
        print("\nGoodbye!")
        sys.exit()

    add_user2 = input("Please Confirm Username: ").lower()

    # Allows the user to prematurely exit
    if add_user2 == "e":
        print("\nGoodbye!")
        sys.exit()

    # Returns add_user if both inputs match
    if add_user == add_user2:
        return add_user
    # Recurs the function if inputs don't match
    print("\nUsername does not match, please try again.")
    return new_user()

def new_pass():
    """Handles inputting and verifying a new username.
    """
    add_pass = input("\nInput New Password: ")

    # Allows the user to prematurely exit
    if add_pass == "e":
        print("\nGoodbye!")
        sys.exit()

    add_pass2 = input("Please Confirm Password: ")

    # Allows the user to prematurely exit
    if add_pass2 == "e":
        print("\nGoodbye!")
        sys.exit()

    # Returns add_pass if both inputs match
    if add_pass == add_pass2:
        return add_pass
    # Recurs the function if inputs don't match
    print("\nPassword does not match, please try again.")
    return new_pass()

def add_task_function():
    """Handles inputting and assigning a task to a user.
    """
    # Collects inputs and returns add_task_list
    add_task_title = input("Task Title: ")
    add_description = input("Task Description: ")
    add_due = input("Task Due Date (Eg. 12 October 2022): ")
    add_task_list = [add_task_title, add_description, add_due]

    return add_task_list
