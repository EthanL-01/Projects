import sqlite3
from datetime import datetime

#######################
# Database Connection #
#######################

def db_connect():
    '''
    Returns the database connection
    '''

    try:
        db = sqlite3.connect("trackerapp.db")

        print("Connected to database: tracker_app.db")
        return db
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def database_creation(db):
    '''
    Creates the required database tables
    '''

    cursor = db.cursor()

    # Enforces foreign keys across tables
    try:
        cursor.execute("PRAGMA foreign_keys = ON;")
        print("Foreign Key enforcement enabled.")

    except sqlite3.Error as e:
        print(f"Error encountered enabling foreign key enforcement: {e}")
        cursor.close()
        return False

    # List to simplify looping through database creation
    table_creation = [

        '''
        CREATE TABLE IF NOT EXISTS workout_categories
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        ''',

        '''
        CREATE TABLE IF NOT EXISTS workout_exercises
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        muscle_group TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES workout_categories(id) ON DELETE CASCADE
        );
        ''',

        '''
        CREATE TABLE IF NOT EXISTS workout_routines
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
        );
        ''',

        '''
        CREATE TABLE IF NOT EXISTS workout_routine_exercises
        (
        routine_id INTEGER NOT NULL,
        exercise_id INTEGER NOT NULL,
        sets INTEGER NOT NULL,
        reps INTEGER NOT NULL,
        order_in_routine INTEGER,
        PRIMARY KEY (routine_id, exercise_id),
        FOREIGN KEY (routine_id) REFERENCES workout_routines(id) ON DELETE CASCADE,
        FOREIGN KEY (exercise_id) REFERENCES workout_exercises(id) ON DELETE CASCADE
        );
        ''',


        '''
        CREATE TABLE IF NOT EXISTS workout_goal_categories
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
        );
        ''',

        '''
        CREATE TABLE IF NOT EXISTS workout_goals
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        target_value REAL NOT NULL,
        goal_category_id INTEGER NOT NULL,
        is_achieved INTEGER DEFAULT 0,
        FOREIGN KEY (goal_category_id) REFERENCES workout_goal_categories(id) ON DELETE CASCADE
        );
        ''',

        '''
        CREATE TABLE IF NOT EXISTS workout_logs
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        routine_id INTEGER NOT NULL,
        date_completed TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
        duration_minutes INTEGER,
        notes TEXT,
        FOREIGN KEY (routine_id) REFERENCES workout_routines(id) ON DELETE CASCADE
        );
        ''',
    ]

    try:
        # Loops through each database during creation
        for sql_command in table_creation:
            cursor.execute(sql_command)

        print("All tables created successfully.")

        db.commit()
        print("Database creation successful.")
        return True

    except sqlite3.Error as e:
        print(f"Error during database initialization: {e}")
        print("Error: Database creation aborted.")
        db.rollback()
        return False

    finally:
        cursor.close()

#####################
#        Menu       #
#####################

def menu_function():
    '''
    Returns the main runtime menu
    '''

    print("\n--- Menu ---\n"
        "\n1. Workout category options"
        "\n2. Exercise options"
        "\n3. Workout routine options"
        "\n4. Goals Options"
        "\n5. View Exercise Progress"
        "\n6. View Progress towards Fitness Goals"
        "\n0. Quit\n")

    while True:
        try:
            menu_input = int(input("Select: ").strip())
            if 0<= menu_input <= 6 or 999:
                return int(menu_input)
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def workout_category_submenu(db):
    '''
    Returns the workout category sub menu
    '''

    while True:
        print("\n--- Workout Category Menu ---\n"
        "\n1. Add a new workout category"
        "\n2. Update a workout category"
        "\n3. Delete a workout category"
        "\n4. View all workout categories"
        "\n0. Back to main menu\n")

        # Takes user input to perform the correct function
        try:
            choice = int(input("Select an option: ").strip())

            if choice == 1:
                add_workout_category(db)
            elif choice == 2:
                update_workout_category(db)
            elif choice == 3:
                delete_workout_category(db)
            elif choice == 4:
                view_workout_categories(db)
            elif choice == 0:
                break
            else:
                print("Invalid option. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

def workout_exercise_submenu(db):
    '''
    Returns the workout exercise sub menu
    '''

    while True:
        print("\n--- Exercise Menu ---\n"
        "\n1. Add a new exercise"
        "\n2. Delete an exercise by category"
        "\n3. View exercises"
        "\n4. View exercises by category"
        "\n0. Back to main menu\n")

        # Takes user input to perform the correct function
        try:
            choice = int(input("Select an option: ").strip())

            if choice == 1:
                add_workout_exercise(db)
            elif choice == 2:
                delete_workout_exercise_by_category(db)
            elif choice == 3:
                view_workout_exercises(db)
            elif choice == 4:
                view_workout_exercises_by_category(db)
            elif choice == 0:
                break
            else:
                print("Invalid option. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

def workout_routine_submenu(db):
    '''
    Returns the workout routine sub menu
    '''

    while True:
        print("\n--- Workout Routine Menu ---\n"
        "\n1. Add a new workout routine"
        "\n2. Log a completed workout routine"
        "\n3. Delete a workout routine"
        "\n4. View workout routines"
        "\n0. Back to main menu\n")

        # Takes user input to perform the correct function
        try:
            choice = int(input("Select an option: ").strip())

            if choice == 1:
                add_workout_routine(db)
            elif choice == 2:
                update_workout_routine(db)
            elif choice == 3:
                delete_workout_routine(db)
            elif choice == 4:
                view_workout_routines(db)
            elif choice == 0:
                break
            else:
                print("Invalid option. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

def goal_submenu(db):
    '''
    Returns the goal sub menu
    '''

    while True:
        print("\n--- Fitness Goals Menu ---\n"
        "\n1. Add a new goal"
        "\n2. Update an existing goal"
        "\n3. Delete a goal"
        "\n4. Add a goal category"
        "\n5. View all goals"
        "\n0. Back to main menu\n")

        # Takes user input to perform the correct function
        try:
            choice = int(input("Select an option: ").strip())

            if choice == 1:
                add_workout_goal(db)
            elif choice == 2:
                update_workout_goals(db)
            elif choice == 3:
                delete_workout_goal(db)
            elif choice == 4:
                add_goal_category(db)
            elif choice == 5:
                view_workout_goals(db)
            elif choice == 0:
                break
            else:
                print("Invalid option. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

############################
#    Core Data Operations  #
############################

def id_validation(db, table_name, id_value):
    '''
    Used to validate if an ID exists in a table
    '''

    cursor = db.cursor()

    # Checks for valid table IDs, and returns an error if invalid
    try:
        cursor.execute(f'''
            SELECT id FROM {table_name}
            WHERE id = ?
            ''', (id_value,))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Database error checking ID in {table_name}: {e}")
        return False
    finally:
        cursor.close()


def get_routine_exercises(db, routine_id):
    '''
    Used to return a list of exercise IDs assigned to a workout routine
    '''

    cursor = db.cursor()
    cursor.execute('''
    SELECT exercise_id 
    FROM workout_routine_exercises 
    WHERE routine_id = ?
    ''', (routine_id,))

    # Returns a list of excluded IDs for validation
    return [row[0] for row in cursor.fetchall()]

#####################################
#     Workout Category Functions    #
#####################################

def add_workout_category(db):
    '''
    Adds a workout category to the workout_category table
    '''

    print("\n--- Add Workout Category ---")
    category_name = input("Enter new workout category name: ").strip()

    # Returns when no workout category name is provided
    if not category_name:
        print("Workout category name cannot be blank.")
        return

    cursor = db.cursor()

    # Inserts the new category into the workout_categories table
    try:
        cursor.execute('''
            INSERT INTO workout_categories (name)
            VALUES (?)''',
            (category_name,))
        db.commit()
        print(f"Category '{category_name}' successfully added.")

    except sqlite3.IntegrityError:
        print(f"Error: A category named '{category_name}' already exists.")
    except sqlite3.Error as e:
        print(f"Error: Database error during category creation: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

def view_workout_categories(db):
    '''
    Returns a list of all workout catgories
    '''

    cursor = db.cursor()
    print("\n--- Workout Categories ---")

    try:
        cursor.execute('''
        SELECT id, name
        FROM workout_categories 
        ORDER BY id''')

        workout_categories = cursor.fetchall()

        # Returns if no workout categories are found to view
        if not workout_categories:
            print("\n No workout categories found.")
            return []

        print("ID | Category Name")
        print("------------------")

        for category_id, name in workout_categories:
            print(f"{category_id:<2} | {name}")

        return workout_categories

    except sqlite3.Error as e:
        print(f"Error: Database error during workout category query: {e}")
        return []

    finally:
        cursor.close()

def update_workout_category(db):
    '''
    Used to update an existing workout category
    '''

    print("\n--- Update Workout Category ---")
    workout_categories = view_workout_categories(db)

    # Returns if no workout categories are found to update
    if not workout_categories:
        return

    try:
        workout_category_id = int(input("Enter category ID to update: "))

        # Returns if no valid ID is found to match user input
        if not id_validation(db, 'workout_categories', workout_category_id):
            print(f"No category found with ID '{workout_category_id}'.")
            return

        workout_category_update_name = input("Enter a new category name: ") \
            .strip()

        # Returns when no workout category name is provided
        if not workout_category_update_name:
            print("Workout category name cannot be blank.")
            return

        cursor = db.cursor()

        # Updates the name of the workout category matching the provided ID
        cursor.execute('''
            UPDATE workout_categories 
            SET name = ? 
            WHERE id = ?''',
            (workout_category_update_name, workout_category_id))

        # Commits the changes to the database
        if cursor.rowcount > 0:
            db.commit()
            print(f"Workout Category ID '{workout_category_id}' updated to \
                  Name: {workout_category_update_name}.")
        else:
            print(f"Workout Category ID '{workout_category_id}' has not \
                  been updated.")

    except ValueError:
        print("Error: Invalid input. Please enter a valid ID number.")
    except sqlite3.IntegrityError:
        print(f"Error: {workout_category_update_name} already exists.")
    except sqlite3.Error as e:
        print(f"Error: Database error during category update: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

def delete_workout_category(db):
    '''
    Used to delete a workout category and it's associated exercises
    '''

    print("\n--- Delete Workout Category ---")
    workout_categories = view_workout_categories(db)

    # Returns when no workout categories are available to delete
    if not workout_categories:
        return

    try:
        workout_category_id = int(input("Enter category ID to delete: "))

        # Returns if no valid ID is found to match user input
        if not id_validation(db, 'workout_categories', workout_category_id):
            print(f"No category found with ID: {workout_category_id}.")
            return

        # Prompts the user for confimration before deletion
        delete_confirm = input(f"Confirmation Required: Deleting category ID \
            {workout_category_id} will delete all associated entries, type \
            'yes' to confirm: ").lower().strip()

        # Returns when the user inputs anything but 'yes', cancelling deletion
        if delete_confirm != "yes":
            print("Deletion cancelled.")
            return

        cursor = db.cursor()

        # Deletes the workout category matching the provided ID
        cursor.execute('''
        DELETE FROM workout_categories 
        WHERE id = ?''',
        (workout_category_id,))

        # Commits the changes to the database
        if cursor.rowcount > 0:
            db.commit()
            print(f"Workout Category \"ID: {workout_category_id}\" has been deleted.")
        else:
            print(f"Workout Category ID: {workout_category_id} has not been deleted.")

    except ValueError:
        print("Error: Invalid input. Please enter a valid ID number.")
    except sqlite3.Error as e:
        print(f"Error: Database error during category deletion: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

#####################################
#     Workout Exercise Functions    #
#####################################

def add_workout_exercise(db):
    '''
    Used to add a workout exercise to the workout_exercises table
    '''

    print("\n--- Add Workout Exercise ---")
    categories = view_workout_categories(db)

    # Returns if no valid workout category is found
    if not categories:
        print("Please add a workout category first before adding an exercise.")
        return

    try:
        exercise_name = input("Enter exercise name: ").strip()

        # Returns when no workout exercise name is provided
        if not exercise_name:
            print("Exercise name cannot be blank.")
            return

        muscle_group = input("Enter targeted muscle group (eg. Chest, Legs): ").strip()

        # Returns when no muscle group name is provided
        if not muscle_group:
            print("Muscle group cannot be blank.")
            return

        category_id = int(input("Enter the category ID for this exercise: "))

        # Returns if no valid ID is found to match user input
        if not id_validation(db, 'workout_categories', category_id):
            print(f"Error: No category found with ID: {category_id}.")
            return

        cursor = db.cursor()

        # Inserts the new workout exercise into the workout_exercises table
        cursor.execute('''
        INSERT INTO workout_exercises (name, muscle_group, category_id)
        VALUES (?,?,?)
        ''', (exercise_name, muscle_group, category_id))
        db.commit()
        print(f"Exercise '{exercise_name}' successfully added.")

    except ValueError:
        print("Error: Invalid input. Please enter a valid number for the \
        category ID.")
    except sqlite3.IntegrityError:
        print(f"Error: An exercise named '{exercise_name}' already exists.")
    except sqlite3.Error as e:
        print(f"Error: Database error during exercise creation: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

def view_workout_exercises(db):
    '''
    Used to return a list of workout exercises
    '''

    cursor = db.cursor()

    print("\n--- View All Workout Exercises ---\n")

    try:
        # Selects and joins the workout_exercises and workout_categories table
        cursor.execute('''
            SELECT we.id, we.name, we.muscle_group, wc.name 
            FROM workout_exercises 
            AS we 
            JOIN workout_categories 
            AS wc ON we.category_id = wc.id 
            ORDER BY we.id''')

        exercises = cursor.fetchall()

        # Returns if no workout exercises are found to display
        if not exercises:
            print("No workout exercises found.")
            return

        # Formats and prints the information headers
        print(f"| {'ID':<2} | {'Name':<20} | {'Muscle Group':<15} | \
            {'Category':<20} |")
        print("-" * 68)

        # Loops through the workout exercises and categories and prints each
        for exercise_id, name, muscle_group, category_name in exercises:
            print(f" {exercise_id:<2} | {name:<20} | {muscle_group:<15} | \
            {category_name:<20} |")

        return exercises

    except sqlite3.Error as e:
        print(f"Error: Database error during exercise query: {e}")
        return []

    finally:
        cursor.close()

def view_workout_exercises_by_category(db):
    '''
    Used to return a list of workout exercises by category
    '''

    print("\n--- View Workout Exercises by Category ---\n")

    # Displays available workout categories to view
    view_workout_categories(db)

    try:
        category_id = int(input("\nEnter the category ID to view exercises \
            for: "))

        # Returns if no valid ID is found to match user input
        if not id_validation(db, 'workout_categories', category_id):
            print(f"No category found with ID: {category_id}.")
            return

        cursor = db.cursor()

        # Selects a record from the workout_exercises table matching
        # the provided ID
        cursor.execute('''
        SELECT name, muscle_group 
        FROM workout_exercises 
        WHERE category_id = ? 
        ORDER BY name
        ''', (category_id,))
        exercises = cursor.fetchall()

        # Returns if no exercises are found to display
        if not exercises:
            print(f"No exercises found for category ID: {category_id}.")
            return

        print("\n--- Exercises in Selected Category ---")

        # Loops through and prints the exercises contained in the
        # selected category
        for name, muscle_group in exercises:
            print(f"- {name} (Muscle Group: {muscle_group})")

    except ValueError:
        print("Error: Invalid input. Please enter a valid number.")
    except sqlite3.Error as e:
        print(f"Error: Database error during exercise query: {e}")
    finally:
        cursor.close()

def view_available_exercises(db, excluded_ids):
    '''
    Used to return a list of available workout exercises
    '''
    cursor = db.cursor()
    print("\n--- Available Workout Exercises ---\n")

    try:
        # Stores a select and join command for the workout_exercises
        # and workout_categories tables
        query = '''
        SELECT we.id, we.name, we.muscle_group, wc.name
        FROM workout_exercises AS we
        JOIN workout_categories AS wc
        ON we.category_id = wc.id
        '''
        # Initializes a list to store each unavailable exercise
        params = []

        # Checks IDs against excluded IDs defined in add_workout_routine()
        if excluded_ids:
            # Stores formatting adjusting to IDs stored in excluded_ids
            placeholders = ', '.join(['?'] * len(excluded_ids))
            # Affixes a WHERE clause to query, adjusting it to the IDs
            # stored in placeholders
            query += f" WHERE we.id NOT IN ({placeholders})"
            # Assigns the excluded IDs to params
            params = excluded_ids

        # Affixes an ORDER BY clause to query
        query += " ORDER BY we.id"

        # Executes the constructed SELECT command
        cursor.execute(query, params)

        exercises = cursor.fetchall()

        # Returns if no workout exercises are available
        if not exercises:
            print("No workout exercises available.")
            return []

        # Formats and prints the information headers
        print(f"| {'ID':<2} | {'Name':<20} | {'Muscle Group':<15} | \
            {'Category':<20} |")
        print("-" * 68)

        # Loops through the workout exercises and categories and prints each
        for exercise_id, name, muscle_group, category_name in exercises:
            print(f" {exercise_id:<2} | {name:<20} | {muscle_group:<15} | \
                {category_name:<20} |")

        print("-" * 68)

        return exercises

    except sqlite3.Error as e:
        print(f"Error: Database error during exercise query: {e}")
        return []
    finally:
        cursor.close()

def delete_workout_exercise_by_category(db):
    '''
    Used to delete workout exercises by category
    '''
    print("\n--- Delete Workout Exercise by Category ---")

    categories = view_workout_categories(db)

    # Returns if no workout categories are available
    if not categories:
        print("No workout categories exist. Please add one before \
        attempting to delete.")
        return

    try:
        category_id = int(input("\nEnter the category ID to delete \
        exercises from: "))

        # Returns if no valid ID is found to match user input
        if not id_validation(db, 'workout_categories', category_id):
            print(f"No category found with ID: {category_id}.")
            return

        cursor = db.cursor()

        # Selects all exercises matching the category ID
        cursor.execute('''
        SELECT id, name 
        FROM workout_exercises 
        WHERE category_id = ? 
        ORDER BY name
        ''', (category_id,))
        exercises = cursor.fetchall()

        # Returns if no exercises are found matching the category ID
        if not exercises:
            print(f"No exercises found in category ID: {category_id}.")
            return

        # Loops through and prints each exercise matching the category ID
        print("\n Exercises:")
        for exercise_id, name in exercises:
            print(f"ID: {exercise_id} | Name: {name}")

        exercise_id_to_delete = int(input("\nEnter the the exercise ID to \
            delete: "))

        # Selects the exercise matching the provided ID
        cursor.execute('''
        SELECT id 
        FROM workout_exercises 
        WHERE id = ? 
        AND category_id = ?
        ''', (exercise_id_to_delete, category_id))

        # Returns if no matching ID is found
        if cursor.fetchone() is None:
            print(f"No exercise with ID {exercise_id_to_delete} found \
                  in category {category_id}.")
            return

        # Prompts the user before deletion
        delete_confirm = input(f"Confirmation Required: Deleting exercise ID: \
            {exercise_id_to_delete}, type 'yes' to confirm: ").lower().strip()

        # Returns if the user inputs anything besides 'yes'
        if delete_confirm != "yes":
            print("Deletion cancelled.")
            return

        # Deletes the exercise matching the provided ID
        cursor.execute('''
        DELETE FROM workout_exercises 
        WHERE id = ?
        ''', (exercise_id_to_delete,))

        # Commits the deletion to the database
        if cursor.rowcount > 0:
            db.commit()
            print(f"Exercise ID: {exercise_id_to_delete} has been deleted.")

    except ValueError:
        print("Error: Invalid input. Please enter a valid number.")
    except sqlite3.Error as e:
        print(f"Error: Database error during exercise deletion: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

def view_exercise_progress(db):
    '''
    Used to view exercise progress
    '''

    print("\n--- View Exercise Progress: ---")

    exercises_exist = view_workout_exercises(db)

    # Returns if no exercises are found
    if not exercises_exist:
        print("No exercises found to view progres. Please add an exercise \
            first.")
        return

    try:
        exercise_id = int(input("\nEnter the ID of the exercise you want to \
            view progress for: "))

        cursor = db.cursor()

        # Selects the exercise matching the provided ID
        cursor.execute('''
        SELECT name 
        FROM workout_exercises 
        WHERE id = ?
        ''', (exercise_id,))

        # Stores the selected exercise
        result = cursor.fetchone()

        # Returns if no matching exercise ID was found
        if result is None:
            print(f"No exercise found with ID: {exercise_id}.")
            return

        # Stores the exercise name
        exercise_name = result[0]

        # Selects and joins the workout_exercises, workout_routine_exercises
        # and workout_logs tables
        cursor.execute('''
        SELECT wl.date_completed, wre.sets, wre.reps
        FROM workout_exercises AS we 
        JOIN workout_routine_exercises AS wre ON we.id = wre.exercise_id
        JOIN workout_logs AS wl ON wre.routine_id = wl.routine_id
        WHERE we.id = ?
        ORDER BY wl.date_completed ASC
        ''', (exercise_id,))

        progress_data = cursor.fetchall()

        # Returns if no progress has been recorded
        if not progress_data:
            print(f"No progress found for '{exercise_name}'.")
            return

        print(f"\n--- Progress for '{exercise_name}' ---")

        # Loops through and prints the progress for each exercise
        for date, sets, reps in progress_data:
            print(f"Date: {date}")
            print(f" - {sets} sets of {reps} reps")

        print("-" * 30)

    except ValueError:
        print("Error: Invalid input. Please enter a valid number.")
    except sqlite3.Error as e:
        print(f"Error: Database error during progress query: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

#####################################
#      Workout Routine Functions    #
#####################################

def add_workout_routine(db):
    '''
    Used to add a workout workout routine to the workout_routines table
    '''

    print("\n--- Workout Routine ---")

    try:
        routine_name = input("Enter a name for the new workout routine: ") \
            .strip()

        # Returns if no workout routine name is provided
        if not routine_name:
            print("Workout routine name cannot be blank.")
            return

        routine_description = input("Optional: Enter workout routine \
            description: ").strip()

        cursor = db.cursor()

        # Inserts the new workout routine
        cursor.execute('''
        INSERT INTO workout_routines (name, description) 
        VALUES (?,?)
        ''', (routine_name, routine_description))
        routine_id = cursor.lastrowid
        print(f"Workout routine: '{routine_name}' has been created with ID: \
            {routine_id}.")

        # Returns if no exercises are available to add to the routine
        if not view_workout_exercises(db):
            print("No exercises found. Please add exercises before \
                continuing.")
            db.commit()
            print(f"Workout routine '{routine_name}' has been successfully \
                added.")
            return

        while True:
            # Stores the IDs of any exercises already in the workout routine
            excluded_ids = get_routine_exercises(db, routine_id)

            # Stores available exercises to be added
            available_exercises = view_available_exercises(db, excluded_ids)

            # Returns if no new exercises are available
            if not available_exercises:
                print(f"All available exercises have been added to Workout \
                Routine: '{routine_name}.")
                break

            # Prompts the user for an exercise ID to add, or allows them to
            # skip this stage
            exercise_id_str = input(f"\nEnter the ID of an exercise to add \
                to '{routine_name}', or leave blank to skip this step: ") \
                .strip()

            # Breaks the while loop when no ID is provided
            if not exercise_id_str:
                break

            try:
                # Converts the exercise ID to an int
                exercise_id = int(exercise_id_str)

                # Prints if no valid ID is found to match user input
                if not id_validation(db, 'workout_exercises', exercise_id):
                    print(f"No exercise found with ID: {exercise_id}.")
                    continue

                # Prints if exercise ID is already present in the
                # workout routine
                if exercise_id in excluded_ids:
                    print(f"Exercise ID: '{exercise_id}' has already been \
                        added to this routine.")
                    continue

                # Collects input for sets and reps
                sets = int(input("Enter number of sets: "))
                reps = int(input("Enter number of reps: "))

                # Inserts the exercise into the workout_routine_exercises
                # table
                cursor.execute('''
                INSERT INTO workout_routine_exercises \
                    (routine_id, exercise_id, sets, reps) 
                VALUES (?,?,?,?)
                ''', (routine_id, exercise_id, sets, reps))
                print("Exercise added to routine")

            except ValueError:
                print("Error: Invalid input. Please enter a valid numbers \
                    for ID, sets and reps.")

        # Commits the new workout routine to the database
        db.commit()
        print(f"Workout routine '{routine_name}' has been successfully \
            added.")

    except sqlite3.IntegrityError:
        print(f"Error: A workout routine named '{routine_name}' already \
            exists.")
    except sqlite3.Error as e:
        print(f"Error: Database error during exercise creation: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()

def update_workout_routine(db):
    '''
    Used to log a workout routine as completed
    '''

    print("\n--- Log a Completed Workout Routine ---")

    routines = view_workout_routines(db)

    # Returns if no workout routines are found
    if not routines:
        print("No workout routines found. Please add a routine before \
            logging progress.")
        return

    try:
        routine_id = int(input("\nEnter the ID of the routine you just \
            completed: "))

        # Returns if no valid ID is found to match user input
        if not id_validation(db, 'workout_routines', routine_id):
            print(f"No routine found with ID: {routine_id}.")
            return

        cursor = db.cursor()

        # Inserts the completed workout routine into workout_logs
        cursor.execute('''
        INSERT INTO workout_logs (routine_id)
        VALUES (?)
        ''', (routine_id,))

        # Commits the completed routine to the database
        db.commit()
        print(f"Workout routine ID: {routine_id} successfully logged as \
            completed.")

    except ValueError:
        print("Error: Invalid input. Please enter a valid ID number.")
    except sqlite3.Error as e:
        print(f"Error: Database error during workout logging: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

def view_workout_routines(db):
    '''
    Used to return a list of workout routines
    '''

    print("\n--- View Workout Routines ---")

    cursor = db.cursor()

    try:
        # Selects all workout routines
        cursor.execute('''
        SELECT id, name, description 
        FROM workout_routines 
        ORDER BY id
        ''')
        routines = cursor.fetchall()

        # Returns if no workout routines are found
        if not routines:
            print("No workout routines found.")
            return []

        # Initializes a list to store workout routine data
        all_routines_data = []

        # Loops through and prints each workout routine
        for routine_id, routine_name, description in routines:
            print(f"\nRoutine ID: {routine_id} | Name: {routine_name}")
            print(f"Description: {description}")

            # Selects and joins the workout_routine_exercises and
            # workout_exercises tables
            cursor.execute('''
            SELECT we.name, wre.sets, wre.reps
            FROM workout_routine_exercises AS wre
            JOIN workout_exercises AS we
            ON wre.exercise_id = we.id
            WHERE wre.routine_id = ?
            ORDER BY we.name
            ''', (routine_id,))

            exercises = cursor.fetchall()

            # Prints each exercise contained in its relevant workout routine
            if exercises:
                print("\n - Exercises:")
                for exercise_name, sets, reps in exercises:
                    print(f" - {exercise_name}: {sets} sets of {reps} reps.")

            # Prints if no exercises are found in a workout routine
            else:
                print("\n - No exercises found for this routine.")

            # Appends each workout routines data to the all_routines_data list
            all_routines_data.append((routine_id, routine_name, description, \
                exercises))

            print("-" * 65)

        return all_routines_data

    except sqlite3.Error as e:
        print(f"Error: Database error during routine query: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()

def delete_workout_routine(db):
    '''
    Used to delete a workout routine and it's associated exercises
    '''

    print("\n--- Delete Workout Routine ---")


    routines = view_workout_routines(db)

    # Returns if no workout routines are found
    if not routines:
        print("No workout routines found to delete.")
        return

    try:

        routine_id = int(input("\nEnter the ID of the workout routine to \
            delete: "))

        # Returns if no valid ID is found to match user input
        if not id_validation(db, 'workout_routines', routine_id):
            print(f"No Routine found with ID: {routine_id}.")
            return

        cursor = db.cursor()

        # Selects the workout_routines table
        cursor.execute('''
        SELECT name 
        FROM workout_routines 
        WHERE id = ?
        ''', (routine_id,))

        # Stores only the specified routine
        routine_name = cursor.fetchone()[0]

        # Prompts the user for confirmation before deletion
        confirm_delete = input(f"Confirmation Required: Deleting workout \
            routine '{routine_name}' (ID: {routine_id}), this will also \
            remove all its exercises. Type 'yes' to confirm: ") \
            .strip().lower()

        # Executes if the user inputs 'yes'
        if confirm_delete == 'yes':

            # First deletes the exercises from the routine
            cursor.execute('''
            DELETE FROM workout_routine_exercises 
            WHERE routine_id = ?
            ''', (routine_id,))

            # Secondly deletes the routine to maintain database integrity
            cursor.execute('''
            DELETE FROM workout_routines 
            WHERE id = ?
            ''', (routine_id,))

            # Commits the deletion to the database
            db.commit()
            print(f"Workout routine '{routine_name}' (ID: {routine_id}) has \
                been successfully deleted.")

        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Error: Invalid input. Please enter a valid number.")
    except sqlite3.Error as e:
        db.rollback()
        print(f"Error: Database error during routine deletion: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

#####################################
#       Goal Category Functions     #
#####################################

def add_goal_category(db):
    '''
    Used to add a goal category to the workout_goal_categories table
    '''

    print("\n--- Add Goal Category ---")
    goal_category_name = input("Enter new goal category name: ").strip()

    # Returns if no goal category is found
    if not goal_category_name:
        print("Goal category name cannot be blank.")
        return

    try:
        cursor = db.cursor()

        # Inserts a new goal category into the workout_goal_categories table
        cursor.execute('''
        INSERT INTO workout_goal_categories (name) 
        VALUES (?)
        ''', (goal_category_name,))
        db.commit()
        print(f"Goal category: '{goal_category_name}' successfully added.")

    except sqlite3.IntegrityError:
        print(f"Error: A goal category named '{goal_category_name}' \
            already exists.")
    except sqlite3.Error as e:
        print(f"Error: Database error during goal category creation: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

def view_goal_categories(db):
    '''
    Used to return a list of goal categories
    '''

    print("\n--- Goal Categories ---")

    cursor = db.cursor()

    try:

        # Selects the workout_goal_categories table
        cursor.execute('''
        SELECT id, name 
        FROM workout_goal_categories 
        ORDER BY id''')

        # Stores all selected goal categories
        view_goal_categories_search_output = cursor.fetchall()

        # Returns if no goal categories were found
        if not view_goal_categories_search_output:
            print("\n No goal categories found.")
            return []


        print("ID | Category Name")
        print("------------------")

        # Loops through and prints each goal category and relevant information
        for category_id, name in view_goal_categories_search_output:
            print(f"{category_id:<2} | {name}")

        return view_goal_categories_search_output

    except sqlite3.Error as e:
        print(f"Error: Database error during goal category query: {e}")
        return []

    finally:
        cursor.close()

def delete_goal_category(db):
    '''
    Used to delete a goal category and it's associated entries
    '''

    print("\n--- Delete Goal Category ---")

    goal_categories = view_goal_categories(db)

    # Returns if no goal categories were found
    if not goal_categories:
        return

    try:
        goal_category_id = int(input("Enter goal category ID to delete: "))

        # Returns if no valid ID is found to match user input
        if not id_validation(db, 'workout_goal_categories', goal_category_id):
            print(f"No goal category found with ID: {goal_category_id}.")
            return

        # Prompts the user for confirmation before deletion
        delete_confirm = input(f"Confirmation Required: Deleting category ID \
            {goal_category_id} will delete all associated entries, type \
            'yes' to confirm: ").lower().strip()

        # Returns if anything other than 'yes' was input
        if delete_confirm != "yes":
            print("Deletion cancelled.")
            return

        cursor = db.cursor()

        # Deletes the selected goal category from workout_goal categories
        cursor.execute('''
        DELETE FROM workout_goal_categories 
        WHERE id = ?
        ''', (goal_category_id,))

        # Commits the deletion to the databse
        if cursor.rowcount > 0:
            db.commit()
            print(f"Goal Category \"ID: {goal_category_id}\" has been \
                deleted.")

        # Prints if the deletion ahs been aborted
        else:
            print(f"Goal Category ID: {goal_category_id} has not been \
                deleted.")

    except ValueError:
        print("Error: Invalid input. Please enter a valid ID number.")
    except sqlite3.Error as e:
        print(f"Error: Database error during goal category deletion: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

#####################################
#           Goal Functions          #
#####################################

def add_workout_goal(db):
    '''
    Used to add a workout goal to the workout_goals table
    '''

    print("\n--- Add Workout Goal ---")

    goal_categories = view_goal_categories(db)

    # Returns if no goal categories were found
    if not goal_categories:
        print("Please add a goal category first before attempting to add a \
            goal.")
        return

    try:
        # Prompts the user to input relevant information for the workout goal
        goal_name = input("Enter goal name: ").strip()
        target_value_str = input("Enter target value (e.g 150 or 75.2): ") \
            .strip()
        goal_category_id = int(input("Enter the Goal Category ID to assign \
            to: "))

        # Returns if no goal name has been input
        if not goal_name:
            print("Goal name cannot be blank.")
            return

        # Returns a ValueError if target_value_str is not a number
        target_value = float(target_value_str)

        # Returns if no valid ID was found
        if not id_validation(db, 'workout_goal_categories', goal_category_id):
            print(f"No goal category found with ID: {goal_category_id}.")
            return

        cursor = db.cursor()

        # Inserts the new workout goal into the workout_goals table
        cursor.execute('''
        INSERT INTO workout_goals (name, target_value, goal_category_id) 
        VALUES (?,?,?)
        ''', (goal_name, target_value, goal_category_id))

        # Commits the new workout goal to the database
        db.commit()
        print(f"Goal '{goal_name}' with a target of {target_value} has been \
            added to category ID {goal_category_id}.")

    except ValueError:
        print("Error: Invalid input. Please enter valid numerical values \
            for target value and/or category ID.")
    except sqlite3.IntegrityError as e:
        print(f"Error: Database integrity error encountered: {e}")
    except sqlite3.Error as e:
        print(f"Error: Database error during goal creation: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

def view_workout_goals(db):
    '''
    Used to return a list of workout goals
    '''

    print("\n--- View Workout Goal ---")

    cursor = db.cursor()

    try:

        # Selects and joins the workout_goals and workout_goal_categories
        # tables
        cursor.execute('''
        SELECT wg.id, wg.name, wg.target_value, wgc.name 
        FROM workout_goals 
        AS wg 
        JOIN workout_goal_categories 
        AS wgc 
        ON wg.goal_category_id = wgc.id 
        ORDER BY wg.id''')

        # Stores the joined table records
        goals = cursor.fetchall()

        # Returns if no workout goals were found
        if not goals:
            print("No workout goals found.")
            return []

        # Prints formatting for viewing the results
        print(f"| {'ID':<2} | {'Goal':<23} | {'Target':<13} | \
            {'Category':<23} |")
        print("-" * 72)

        # Loops through and prints the joined information for each
        # workout goal
        for goal_id, goal_name, target_value, category_name in goals:
            print(f" {goal_id:<2} | {goal_name:<23} | {target_value:<13.2f} \
            | {category_name:<23} |")

        return goals

    except sqlite3.Error as e:
        print(f"Error: Database error during goal query: {e}")
        return []

    finally:
        cursor.close()

def update_workout_goals(db):
    '''
    Used to update a workout goal
    '''

    print("\n--- Update Workout Goal ---")

    goals = view_workout_goals(db)

    # Returns if no workout goals were found
    if not goals:
        return

    try:
        goal_id = int(input("Enter goal ID to update: "))

        # Returns if no valid ID was found
        if not id_validation(db, 'workout_goals', goal_id):
            print(f"No goal found with ID: {goal_id}.")
            return

        # Prompts the user to input new values to update the workout goal
        print("Please enter new goal values, or leave blank to skip \
            changing that value.")
        new_name = input("Enter new goal name: ").strip()
        new_target_value_str = input("Enter new target value: ").strip()
        new_category_id_str = input("Enter new category ID: ").strip()

        # Stores a list of clauses to execute during the SQL command
        set_clauses = []

        # Stores a list of new values to update during the SQL command
        params = []

        # Appends the new name and SQL syntax to their relevant lists
        if new_name:
            set_clauses.append("name = ?")
            params.append(new_name)

        # Appends the new target value and SQL syntax to their relevant lists
        if new_target_value_str:
            new_target_value = float(new_target_value_str)
            set_clauses.append("target_value = ?")
            params.append(new_target_value)

        # Appends the new category and SQL syntax to their relevant lists
        if new_category_id_str:
            new_category_id = int(new_category_id_str)

            # Returns if no valid ID is found
            if not id_validation(db, 'workout_goal_categories', \
                new_category_id):
                print(f"No goal category found with ID: {new_category_id}.")
                return
            set_clauses.append("goal_category_id = ?")
            params.append(new_category_id)

        # Returns if no changes were made
        if not set_clauses:
            print("No changes were made.")
            return

        # Appends the workout_goal id to the params list
        params.append(goal_id)

        # Constructs the SQL command for execution
        update_query = f'''
        UPDATE workout_goals 
        SET {', '.join(set_clauses)}
        WHERE id = ?'''

        cursor = db.cursor()

        # Executes the constructed SQL command
        cursor.execute(update_query, tuple(params))

        # Commits the changes to the database
        if cursor.rowcount > 0:
            db.commit()
            print(f"Goal ID: {goal_id} has been updated successfully.")

        # Returns if no changes were committed
        else:
            print(f" No changes made to goal ID: {goal_id}.")

    except ValueError:
        print("Error: Invalid input. Please enter a valid ID, target \
            and/or category number.")
    except sqlite3.IntegrityError as e:
        print(f"Error: A database integrity error has occured: {e}")
    except sqlite3.Error as e:
        print(f"Error: Database error during goal update: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

def delete_workout_goal(db):
    '''
    Used to delete a workout goal
    '''

    print("\n--- Delete Workout Goal ---")

    goals = view_workout_goals(db)

    # Returns if no workout_goals were found
    if not goals:
        return

    try:
        goal_id = int(input("Enter workout goal ID to delete: "))

        # Returns if no valid ID was found
        if not id_validation(db, 'workout_goals', goal_id):
            print(f"No workout goal found with ID: {goal_id}.")
            return

        # Prompts the user for confirmation before deletion
        delete_confirm = input(f"Confirmation Required: Deleting workout \
            goal ID {goal_id}, type 'yes' to confirm: ").lower().strip()

        # Returns if anything aside from 'yes' was input
        if delete_confirm != "yes":
            print("Deletion cancelled.")
            return

        cursor = db.cursor()

        # Deletes the workout goal from the workout_goals table
        cursor.execute('''
        DELETE FROM workout_goals 
        WHERE id = ?
        ''', (goal_id,))

        # Commits the changes to the database
        if cursor.rowcount > 0:
            db.commit()
            print(f"Workout goal \"ID: {goal_id}\" has been deleted.")

        # Returns if the deletion was aborted
        else:
            print(f"Workout goal ID: {goal_id} has not been deleted.")

    except ValueError:
        print("Error: Invalid input. Please enter a valid ID number.")
    except sqlite3.Error as e:
        print(f"Error: Database error during goal category deletion: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

def view_progress_fitness_goals(db):
    '''
    Used to return fitness goal progress
    '''

    print("\n View Progress Towards Fitness Goals ---")

    goals = view_workout_goals(db)

    # Returns if no workout goals were found
    if not goals:
        print("No goals found. Please add a goal first.")
        return

    try:
        goal_id = int(input("\nEnter the ID of the goal you want to view \
            progress for: "))

        cursor = db.cursor()

        # Selects and joins the workout_goals and workout_goal_categories
        # tables
        cursor.execute('''
        SELECT wg.name, wg.target_value, wgc.name
        FROM workout_goals AS wg
        JOIN workout_goal_categories AS wgc ON wg.goal_category_id = wgc.id
        WHERE wg.id = ?
        ''', (goal_id,))

        goal_details = cursor.fetchone()

        # Returns if no workout goal was found with the input ID
        if not goal_details:
            print(f"No goal found with ID: {goal_id}.")
            return

        # Assigns the following variables their relevant data
        goal_name, target_value, category_name = goal_details

        # Selects and joins the workout_logs, workout_routines,
        # workout_routine_exercises, workout_exercises and
        # workout_categories tables
        cursor.execute('''
        SELECT COUNT(wl.id)
        FROM workout_logs AS wl
        JOIN workout_routines AS wr ON wl.routine_id = wr.id
        JOIN workout_routine_exercises AS wre ON wr.id = wre.routine_id
        JOIN workout_exercises AS we ON wre.exercise_id = we.id
        JOIN workout_categories AS wc ON we.category_id = wc.id
        WHERE wc.name = ?
        ''', (category_name,))

        progress = cursor.fetchone()[0]

        # Prints the selected workout goal information
        print(f"\n--- Progress for Goal: '{goal_name}' ---")
        print(f"Goal Category: {category_name}")
        print(f"Target Value: {target_value}")
        print(f"Progress: {progress} completed routine(s)")

        # Prints and updates if the workout goal has been achieved
        if progress >= target_value:
            print("\n You have completed this goal.")
            cursor.execute('''
            UPDATE workout_goals 
            SET is_achieved = 1 
            WHERE id = ?
            ''', (goal_id,))

            # Commits the changes to the database
            db.commit()

        # Returns if the workout goal has not been completed
        else:
            remaining = target_value - progress
            print(f"You are {remaining:.0f} routines away from your goal.")

    except ValueError:
        print("Error: Invalid input. Please enter a valid number.")
    except sqlite3.Error as e:
        print(f"Error: Database error during progress query: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

############################
