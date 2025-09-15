from datetime import datetime
from task_manager_functions import user_auth, login_dict_function, new_user, \
new_pass, add_task_function, user_exit

#====Login Section====

# Handles log in with limited attempts
login_dict = login_dict_function()
login_user = user_auth(login_dict)

#====Menu Section====

while True:

    # Initializes list for later use
    add_task_list = []

    # Displays only if "admin" is stored in login_user
    if login_user == "admin":

        # Collects input to execute the associated if/elif/else statement
        menu = input("""Select one of the following options:
        r - register a user
        a - add task
        va - view all tasks
        vm - view my tasks
        vu - view user's tasks
        s - statistics             
        cu - change user
        e - exit
        : """).lower()

    # Displays if anyone other than "admin" is stored in login_user
    else:

        # Collects input to execute the associated if/elif/else statement
        menu = input("""Select one of the following options:
        a - add task
        va - view all tasks
        vm - view my tasks
        cu - change user
        e - exit
        : """).lower()

    # Handles registering a new user
    if menu == "r":

        # Only executes if "admin" is logged in
        if login_user == "admin":

            try:

                # Opens tasks.txt as "append+"
                with open("user.txt", "a+", encoding = "utf-8") as user_info:

                    # Collects inputs, ensures inputs match and checks if
                    # the user is already present to prevent duplicates
                    add_user = new_user()
                    add_pass = new_pass()
                    if add_user not in login_dict:

                        # Writes a new user to user.txt
                        user_info.write("\n"+add_user+", "+add_pass)

                        # Flushes memory to immediately update the text file
                        user_info.flush()
                        print("Registered New User\n")

                        # Updates login_dict with the new user
                        login_dict[add_user.lower()] = add_pass

                    # Executes if the user is already registered
                    else:
                        print("User Already Registered\n")

            # Handles ending the program if the file cannot be found
            except FileNotFoundError as error:
                print("File cannot be found.")
                user_exit()

            # Handles ending the program if a generic exception is detected
            except Exception as error:
                print("An unexpected error has occured.")
                user_exit()

        # Executes if anyone other than "admin" is stored in login_user
        else:
            print("Access Denied.\n" \
            "Admin Login Required.\n")

    # Handles registering a new task to a user
    elif menu == "a":

        try:

            # Opens tasks.txt as "append+"
            with open("tasks.txt", "a+", encoding = "utf-8") as task_info:
                while True:

                    # Collects input and checks if the user is valid
                    add_task_check = input("\nUsername: ").lower()

                    # Handles prematurely ending the program
                    if add_task_check == "e":
                        user_exit()

                    # Checks if the intended user is stored in login_dict
                    if add_task_check in login_dict:

                        # Collects inputs and writes a new task to tasks.txt
                        # in the correct format
                        add_task_list = add_task_function()
                        task_info.write("\n"
                                + add_task_check + ", "
                                + add_task_list[0] + ", "
                                + add_task_list[1] + ", "
                                + add_task_list[2] + ", "
                                # Writes the current date
                                + datetime.today().strftime("%d %B %Y")
                                + ", " + "No")
                                # This thread helped me understand this
                                # https://shorturl.at/hfdEl

                        # Flushes memory to immediately update the text file
                        task_info.flush()
                        print("\nNew Task Assigned.\n")
                        break

                    # Executes when the input username is invalid
                    print(f"Invalid Username: \"{add_task_check}\". \
                        Please Try again.\n")

        # Handles ending the program if the file cannot be found
        except FileNotFoundError as error:
            print("File cannot be found.")
            user_exit()

        # Handles ending the program if a generic exception is detected
        except Exception as error:
            print("An unexpected error has occured.")
            user_exit()

    # Handles viewing all tasks
    elif menu == "va":

        try:

            # Opens task.txt as "read"
            with open("tasks.txt", "r", encoding = "utf-8") as task_info:

                # Sets the file's pointer to the start
                task_info.seek(0)

                # Removes extra whitespaces and splits each line into a list
                # and prints it's components in the correct format
                for i in task_info:
                    task_entry = i.strip().split(", ")
                    print(f"\nTask:               {task_entry[1]} \
                            \nAssigned To:        {task_entry[0]} \
                            \nDate Assigned:      {task_entry[4]} \
                            \nDue Date:           {task_entry[3]} \
                            \nTask Complete?:     {task_entry[5]} \
                            \nTask Description: \n\n{task_entry[2]}\n ")

        # Handles ending the program if the file cannot be found
        except FileNotFoundError as error:
            print("File cannot be found.")
            user_exit()

        # Handles ending the program if a generic exception is detected
        except Exception as error:
            print("An unexpected error has occured.")
            user_exit()

    # Handles viewing the logged in user's tasks
    elif menu == "vm":
        try:
            # Opens task.txt as "read"
            with open("tasks.txt", "r", encoding = "utf-8") as task_info:

                # Updates to True if any tasks are assigned to the user
                found_tasks = False

                # Removes extra whitespaces and splits each line into a list
                # and prints it's components in the correct format
                for i in task_info:
                    task_entry = i.strip().split(", ")

                    # Repeats the code for "va" with a check to only print
                    # tasks assigned to the currently logged in user
                    if login_user == task_entry[0]:

                        print(f"\nTask:               {task_entry[1]} \
                                \nAssigned To:        {task_entry[0]} \
                                \nDate Assigned:      {task_entry[4]} \
                                \nDue Date:           {task_entry[3]} \
                                \nTask Complete?:     {task_entry[5]} \
                                \nTask Description: \n\n{task_entry[2]}\n ")

                        # Flags that this user has assigned tasks
                        found_tasks = True

                        # Flushes memory to immediately update the text file
                        task_info.flush()

                # Executes if found_tasks is still False
                if not found_tasks:
                    print("\nNo tasks assigned to user.\n")

        # Handles ending the program if the file cannot be found
        except FileNotFoundError as error:
            print("File cannot be found.")
            user_exit()

        # Handles ending the program if a generic exception is detected
        except Exception as error:
            print("An unexpected error has occured.")
            user_exit()

    elif menu == "vu":

         # Only executes if "admin" is logged in
        if login_user == "admin":

            try:
                # Opens task.txt as "read"
                with open("tasks.txt", "r", encoding = "utf-8") as task_info:

                    # Updates to True if any tasks are assigned to the user
                    found_tasks = False

                    # Collects input to check a particular user's tasks
                    view_user_tasks = input("\nUsername: ")

                    # Handles prematurely ending the program
                    if view_user_tasks == "e":
                        user_exit()

                    for i in task_info:
                        task_entry = i.strip().split(", ")

                    # Repeats the code for "va" and "vm" with a check to
                    # only print tasks assigned to the user stored in
                    # view_user_task
                        if view_user_tasks == task_entry[0]:

                            print(f"\nTask:               {task_entry[1]} \
                                    \nAssigned To:        {task_entry[0]} \
                                    \nDate Assigned:      {task_entry[4]} \
                                    \nDue Date:           {task_entry[3]} \
                                    \nTask Complete?:     {task_entry[5]} \
                                    \nTask Description: \n\n{task_entry[2]} \
                                    \n ")

                            # Flags that this user has assigned tasks
                            found_tasks = True

                            # Flushes memory to immediately update the text file
                            task_info.flush()

                    # Executes if found_tasks is still False
                    if not found_tasks:
                        print("\nNo tasks assigned to user.\n")

        # Handles ending the program if the file cannot be found
            except FileNotFoundError as error:
                print("File cannot be found.")
                user_exit()

        # Handles ending the program if a generic exception is detected
            except Exception as error:
                print("An unexpected error has occured.")
                user_exit()

        # Executes if anyone other than "admin" is stored in login_user
        else:
            print("Access Denied.\n" \
            "Admin Login Required.\n")    

    elif menu == "s":

        # Only executes if "admin" is logged in
        if login_user == "admin":

            try:

                # Opens both task.txt and user.txt as "read"
                with open("tasks.txt", "r", encoding = "utf-8") as task_info,\
                    open("user.txt", "r", encoding = "utf-8") as user_info:

                    # Sets the file's pointer to the start
                    task_info.seek(0)

                    # Sums each line in each file and prints them in the
                    # correct format
                    total_users = sum(1 for _ in user_info)
                    total_tasks = sum(1 for _ in task_info)

                    print(f"\nTotal Users: {total_users}")
                    print(f"Total Tasks: {total_tasks}\n")

            # Handles ending the program if the file cannot be found
            except FileNotFoundError as error:
                print("File cannot be found.")
                user_exit()

            # Handles ending the program if a generic exception is detected
            except Exception as error:
                print("An unexpected error has occured.")
                user_exit()

        # Executes if anyone other than "admin" is stored in login_user
        else:
            print("Access Denied.\n" \
            "Admin Login Required.\n")

    # Allows the user to change user mid-session using the same login logic
    elif menu == "cu":
        print("")
        login_dict = login_dict_function()
        login_user = user_auth(login_dict)

    # Handles ending the program
    elif menu == "e":
        user_exit()

    # Catches any invalid inputs
    else:
        print("Invalid input. Please try again")
