#####################
#       Modules     #
#####################

import sys
from tracker_app_functions import menu_function, db_connect, \
database_creation, goal_submenu, workout_category_submenu, \
workout_exercise_submenu, workout_routine_submenu, \
view_progress_fitness_goals, view_exercise_progress

#####################
#      Database     #
#####################

db = db_connect()

database_creation(db)

#####################
#      Runtime      #
#####################

'''--- Menu ---"
1. Workout category options"
2. Exercise options
3. Workout routine options"
4. Goal options"
5. View Exercise Progress"
6. View Progress towards Fitness Goals"
0. Quit")'''

# Main runtime application that takes user input and displays relevant options
while True:
    try:

        menu_input = menu_function()

        if menu_input == 1:
            workout_category_submenu(db)

        elif menu_input == 2:
            workout_exercise_submenu(db)

        elif menu_input == 3:
            workout_routine_submenu(db)

        elif menu_input == 4:
            goal_submenu(db)

        elif menu_input == 5:
            view_exercise_progress(db)
        elif menu_input == 6:
            view_progress_fitness_goals(db)

        elif menu_input == 0:
            print("Exiting.")
            db.commit()
            break

# Generic error catch
    except Exception as e:
        print("Error detected. Exiting.")
        db.rollback()
        db.close()
        sys.exit()

# Database and system close
db.close()
sys.exit()
