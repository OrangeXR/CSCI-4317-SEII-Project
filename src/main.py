import requests
import os
import sqlite3
import json
from werkzeug.security import check_password_hash
from dotenv import load_dotenv

# ==================
# open db connection
# ==================
def get_db():
    conn = sqlite3.connect("src/instance/astra.db")
    conn.row_factory = sqlite3.Row
    return conn




# ==================
# choose user
# ==================
def choose_user():
    db = get_db() 
    users = db.execute("SELECT id, name FROM users").fetchall()
    db.close()
    
    print("\nAvailable Users:")
    for u in users: 
        print(f"{u['id']}: {u['name']}") 
  
    user_id = int(input("\nEnter user ID: "))

    # Fetch stored password hash
    stored_hash = get_user_password_hash(user_id)
   
    if stored_hash is None:
        print("Invalid user ID.")   
        return choose_user()
      
    # Ask for password until correct 
    while True:
        password = input("Enter password: ").strip() 
    
        if check_password_hash(stored_hash, password):
            print("Login successful!\n") 
            return user_id
        else:    
            print("Incorrect password. Try again.\n")


# ======================================                         
# Validate Login(get hash from database)                         
# ======================================                           
def get_user_password_hash(user_id):
    db = get_db()
    row = db.execute(
        "SELECT password_hash FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    db.close()
    return row["password_hash"] if row else None





# =====================
# get Assignments
# =====================
def get_assignments(user_id):
    db = get_db()
    items = db.execute(
        "SELECT * FROM assignments WHERE user_id = ? ",
        (user_id,)
    ).fetchall()
    db.close()

    items = sorted(items, key=lambda item: item["name"].lower())

    print("\n========================================== Assignments ==========================================")
    print(f"{'Name'.ljust(30)} {'Class'.ljust(25)} {'Category'.ljust(15)} {'Due Date'.ljust(15)} {'Status'.ljust(10)}")
    print("-" * 97)

    for item in items:
        class_name = str(item["class_name"])  # convert INT → string
        if item["status"] == 0:
            status_text = "Not Done"
        elif item["status"] == 1:
            status_text = "Done"
        else:
            status_text = "Unknown"

        print(
            f"{item['name'].ljust(30)} "
            f"{class_name.ljust(25)} "
            f"{item['category'].ljust(15)} "
            f"{item['due_date'].ljust(15)}"
            f"{status_text}"
        )

# =====================
# get items not done
# =====================
def get_assignments_not_done(user_id):
    db = get_db()
    items = db.execute(
        """
        SELECT name, class_name, category, due_date, status
        FROM assignments
        WHERE user_id = ? AND status = '0'
        ORDER BY due_date ASC
        """,
        (user_id,)
    ).fetchall()
    db.close()

    print("\n======================================= Assignments Not Done =====================================")


    if not items:
        print("No assignments found.")
        return


    print(f"{'Name'.ljust(30)} {'Class'.ljust(25)} {'Category'.ljust(15)} {'Due Date'.ljust(15)} {'Status'}")
    print("-" * 99)

    for item in items:
        class_name = str(item["class_name"])  # convert INT → string
        status_text = "Done" if item["status"] == "1" else "Not Done"

        print(
            f"{item['name'].ljust(30)} "
            f"{class_name.ljust(25)} "
            f"{item['category'].ljust(15)} "
            f"{item['due_date'].ljust(15)} "
            f"{status_text}"
        )


# =====================================================================================================
# =====================================================================================  Select Options
# =====================================================================================================
def main():
    # ===========
    # Select User
    # ===========
    print("\n=== Assignment Tracker ===")
    user_id = choose_user()

    # =========
    # Main Menu
    # =========
    while True:
        print("\nOptions:")
        print("1. View Assignments")
        print("2. View Assignments Not Done")
#        print("3. Add Item to Assignments") # (a bit annoying in terminal)
#        print("3. Generate Binny Menu")
        print("4. Logout")
        print("5. Exit")
        choice = input("\nChoose an option: ")
# =====================================================================================  1. Get User Assignments
        if choice == "1":
            get_assignments(user_id)
# =====================================================================================  2. Get/sort Assignments by date   
        elif choice == "2":
            get_assignments_not_done(user_id)
# =====================================================================================  3. Add an item to user Assignments (not sure if we'll use it in terminal)           
#        elif choice == "3":
#            add_item(user_id)
# =====================================================================================  4. Logout
        elif choice == "4":
                print("\nLogging out...\n")
                return  "logout"# <-- sends user back to user select
# =====================================================================================  5. Exit
        elif choice == "5":
            print("Goodbye!")
            return "exit"

        else:
            print("Invalid choice.")



if __name__ == "__main__":
    while True:  
        result = main() # <--- Loop

        if result == "logout": 
            continue    # <--- Change user
        if result == "exit":
            break       # <---- Exit
