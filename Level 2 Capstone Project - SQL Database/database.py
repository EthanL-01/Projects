import sqlite3

db = sqlite3.connect("ebookstore.db")
cursor = db.cursor()

class Book:
    '''
    Defines the Book object class.
    This class is used to structure the initial dataset.
    '''
    def __init__(self, bookid, title, author, quantity):
        self.bookid = bookid
        self.title = title
        self.author = author
        self.quantity = quantity

# Defines the initial dataset and collects them in a list for insertion
book1 = Book(3001, "A Tale of Two Cities", "Charles Dickens",
             30)
book2 = Book(3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling",
            30)
book3 = Book(3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis",
             25)
book4 = Book(3004, "The Lord of the Rings", "J.R.R Tolkien",
             37)
book5 = Book(3005, "Alice in Wonderland", "Lewis Carol",
             12)

initial_book_data = [book1, book2, book3, book4, book5]

# Defines the menu as a function
def menu():
    '''
    Prints the menu selection for operation navigation.
    '''
    print("""
    Menu:
    1. Enter Book
    2. Update Book
    3. Delete Book
    4. Search Books
    0. Exit
        """)

# --- Table Creation Section ---
try:
    # Drop table command used for testing purposes
    # cursor.execute('''
    #                DROP TABLE books''')

    # Creates the 'books' table with pertinent constraints
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books
                   (
                   id INTEGER PRIMARY KEY,
                   title TEXT UNIQUE,
                   author TEXT,
                   quantity INTEGER
                   )
                   ''')
    db.commit()

    # --- Initial Data Insertion Section ---

    # Selects all books in the table for validation
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        print("Populating database with initial book data...")

        # Inserts the contents of initial_book_data into the table on startup
        for book_item in initial_book_data:
            cursor.execute('''
                INSERT INTO books(id, title, author, quantity)
                VALUES(?,?,?,?)''',
                (book_item.bookid,
                 book_item.title,
                 book_item.author,
                 book_item.quantity))

        db.commit()
        print("Initial book data committed.")

    else:
        print("Database already contains data. Skipping initial setup.")

except sqlite3.Error as e:
    print(f"Error during databse initialization: {e}")
    db.rollback()
    exit()

# --- Main runtime application ---
while True:
    try:
        menu()
        user_input = int(input("Input Selection: "))

        # --- Enter new Book Section ---
        if user_input == 1:
            try:
                # Collects inputs for a new book entry
                print("\n--- Enter New Book ---")
                book_new_id = int(input("Enter ID: "))
                book_new_title = input("Enter Title: ")
                book_new_author = input("Enter Author: ")
                book_new_quantity = int(input("Enter Quantity: "))

                # Inserts the new book into the table
                cursor.execute('''
                    INSERT INTO books(id, title, author, quantity)
                    VALUES(?,?,?,?)''',
                    (book_new_id,
                     book_new_title,
                     book_new_author,
                     book_new_quantity))

                db.commit()
                print(f"\nBook '{book_new_title}' (ID: {book_new_id}) "
                      f"successfully entered.")

            except ValueError:
                print("\nInvalid input. Please ensure ID and Quantity " \
                "are integers.")
                db.rollback()
            except sqlite3.IntegrityError as e:
                print(f"\nError: A book with this ID or Title already exists: {e}")
                db.rollback()
            except sqlite3.Error as e:
                print(f"Database error during book entry: {e}")
                db.rollback()
            except Exception as e:
                print(f"An unexpected error occured during book entry: {e}")
                db.rollback()

        # --- Update Book Section ---
        if user_input == 2:
            try:
                # Collects input for which book is to be updated
                print("\n --- Update Book ---")
                original_id = int(input("Enter Original Book ID: "))

                # Selects the relevant book in the table
                cursor.execute('''
                                SELECT id FROM books WHERE id = ?''',
                                (original_id,))
                existing_db_book = cursor.fetchone()

                # Executes if no valid book was selected for validation
                if not existing_db_book:
                    print(f"Book with ID {original_id} not found. " \
                          f"Cannot update.")
                    continue

                # Collects inputs for book updating
                print("\nEnter the revised details:")
                id_update = int(input("Enter Revised ID: "))
                title_update = input("Enter Revised Title: ")
                author_update = input("Enter Revised Author: ")
                quantity_update = int(input("Enter Revised Quantity: "))

                # Selects the relevant book in the table for updating
                cursor.execute('''
                    SELECT id FROM books WHERE id = ? AND id != ?''',
                    (id_update, original_id))

                # Executes if a duplicate id is detected
                if cursor.fetchone():
                    print("\nInvalid input. The revised ID already exists " \
                    "for another book.")
                    continue

                # Selects the relevant book in the table for updating
                cursor.execute('''
                    SELECT title FROM books WHERE title = ? AND id != ?''',
                    (title_update,
                     original_id))

                # Executes if a duplicate title is detected
                if cursor.fetchone():
                    print("\nInvalid input. The revised Title already exists "
                    "for another book.")
                    continue

                # Updates the relevant book with the collected inputs
                cursor.execute('''
                    UPDATE books
                    SET id = ?,
                    title = ?,
                    author = ?,
                    quantity = ?
                    WHERE id = ?''',
                    (id_update,
                     title_update,
                     author_update,
                     quantity_update,
                     original_id))

                db.commit()

                # Checks if the update operation was successful
                if cursor.rowcount > 0:
                    print(f"\nBook with ID {original_id} successfully updated" \
                          f"to ID {id_update}.")
                # Executes if changes were not made
                else:
                    print(f"Book with ID {original_id} was not found or no" \
                          f"changes were made.")

            except ValueError:
                print("\n Invalid input. Please ensure IDs and quantities are " \
                "integers.")
                db.rollback()
            except sqlite3.Error as e:
                print(f"\nDatabase error during book update: {e}")
                db.rollback()
            except Exception as e:
                print(f"\nAn unexpected error occured during book update: {e}")
                db.rollback()

        # --- Delete Book Section ---
        elif user_input == 3:
            try:
                # Collects input for which book is to be deleted
                print("\n--- Delete Book ---")
                book_id_to_delete = int(input("Enter Book ID to delete: "))

                # Selects the relevant book in the table
                cursor.execute('''SELECT id FROM books WHERE id = ?''',
                               (book_id_to_delete,))
                existing_db_book = cursor.fetchone()

                # Executes if no valid book was selected
                if not existing_db_book:
                    print(f"\nBook with ID {book_id_to_delete} not found. " \
                    f"Cannot delete.")
                    continue

                # Deletes the selected book from the table
                cursor.execute('''DELETE FROM books WHERE id = ?''',
                               (book_id_to_delete,))

                db.commit()

                # Checks if the update operation was successful
                if cursor.rowcount > 0:
                    print(f"\nBook with ID {book_id_to_delete}" \
                          f"successfully deleted.")
                # Executes if changes were not made
                else:
                    print(f"Book with ID {book_id_to_delete} not found.")

            except ValueError:
                print("\nInvalid input. Please ensure the ID is an integer.")
                db.rollback()
            except sqlite3.Error as e:
                print(f"Database error during book deletion: {e}")
                db.rollback()
            except Exception as e:
                print(f"\nAn unexpected error occured during book" \
                      f"deletion: {e}")
                db.rollback()

        # --- Search Books Section ---
        elif user_input == 4:
            try:
                print("\n--- Search Books ---")
                search_category_input = int(input(
                    "\nSearch by:\n"
                    "1. ID\n"
                    "2. Title\n"
                    "3. Author\n"
                    "0. Cancel Search\n"
                    "\nInput Search Category: "
                ))

                # Defines a variable for validation check
                search_query_executed = False

                # --- ID Search Section ---
                if search_category_input == 1:
                    # Collects id input and selects the relevant book
                    search_id = int(input("\nEnter ID: "))
                    cursor.execute('''
                                    SELECT id, title, author, quantity
                                   FROM books
                                   WHERE id = ?''', (search_id,))
                    # Updates validation bool
                    search_query_executed = True

                # --- Title Search Section ---
                elif search_category_input == 2:
                    # Collects title input and selects the relevant book
                    search_title = input("\nEnter Title " \
                    "(Inc. Partial Matches): ")
                    cursor.execute('''
                                    SELECT id, title, author, quantity
                                   FROM books
                                   WHERE title LIKE ?''',
                                   ('%' + search_title + '%',))
                    # Updates validation bool
                    search_query_executed = True

                # --- Author Search Section ---
                elif search_category_input == 3:
                    # Collects author input and selects the relevant book
                    search_author = input("\nEnter Author " \
                    "(Inc. Partial Matches): ")
                    cursor.execute('''
                                    SELECT id, title, author, quantity
                                   FROM books
                                   WHERE author LIKE ?''',
                                   ('%' + search_author + '%',))
                    # Updates validation bool
                    search_query_executed = True

                # --- Search Cancel Section ---
                elif search_category_input == 0:
                    print("\nSearch Cancelled.")
                    continue
                else:
                    print("\nInvalid search category input. Please try again.")
                    continue

                # Executes if validation check is True
                if search_query_executed:
                    search_output = cursor.fetchall()

                    # Prints each field for the relevant books
                    if search_output:
                        print("\n--- Search Results ---")
                        for row in search_output:
                            print(f"ID: {row[0]}\n"
                                  f"Title: {row[1]}\n"
                                  f"Author: {row[2]}\n"
                                  f"Quantity: {row[3]}\n"
                                  f"--------------------")
                    # Executes if no valid books are present
                    else:
                        print("\nNo books found matching " \
                        "the search criteria.")

            except ValueError:
                print("\nInvalid input for search category or ID. " \
                "Please input a valid integer.")
            except sqlite3.Error as e:
                print(f"\nDatabase error during search: {e}")
            except Exception as e:
                print(f"\nAn unexpected error occured during search: {e}")

        # --- Exit Application Section ---
        elif user_input == 0:
            print("\nExiting Application.")
            break

    except ValueError:
        print("\nInvalid Input. Please enter a valid integer " \
        "for your menu selection.")
    except Exception as e:
        print(f"\nAn unexpected error occured: {e}")

# Closes the database connection
db.close()
print("Database connection terminated.")
