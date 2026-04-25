import sqlite3
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

# =========================
# get Assignments not done
# =========================
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


# =========================
# add Assignments
# =========================

def add_assignment(user_id):
    print("\n=== Add New Assignment ===")

    name = input("Assignment name: ").strip()
    class_name = input("Class name (ex: Software Engineering): ").strip()
    category = input("Category (ex: Essay, Homework, Lab): ").strip()
    due_date = input("Due date (YYYY-MM-DD): ").strip()

    # Basic validation
    if not name or not class_name or not category or not due_date:
        print("\nAll fields are required. Assignment not added.")
        return

    db = get_db()
    db.execute(
        """
        INSERT INTO assignments (user_id, name, class_name, category, due_date, status)
        VALUES (?, ?, ?, ?, ?, 0)
        """,
        (user_id, name, class_name, category, due_date)
    )
    db.commit()
    db.close()

    print("\nAssignment added successfully!")



# =========================
# Mark assignment Done
# =========================

def mark_assignment_done(user_id):
    db = get_db()

    # Fetch assignments for this user
    items = db.execute(
        "SELECT id, name, status FROM assignments WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    if not items:
        print("\nNo assignments found.")
        db.close()
        return

    print("\n=========== Mark Assignment as Done ===========")
    print(f"{'ID'.ljust(5)} {'Name'.ljust(40)} {'Status'}")
    print("-" * 60)

    for item in items:
        status_text = "Done" if item["status"] == 1 else "Not Done"
        print(f"{str(item['id']).ljust(5)} {item['name'].ljust(40)} {status_text}")

    try:
        assignment_id = int(input("\nEnter the ID of the assignment to mark as Done: "))
    except ValueError:
        print("Invalid input. Must be a number.")
        db.close()
        return

    # Update the assignment
    db.execute(
        "UPDATE assignments SET status = 1 WHERE id = ? AND user_id = ?",
        (assignment_id, user_id)
    )
    db.commit()
    db.close()

    print("\nAssignment marked as Done!")




















# =====================================================================================================
# =====================================================================================  MAIN MENU
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
        print("3. Add Assignments") # (a bit annoying in terminal)
        print("4. Mark Assignment as Done")
        print("5. Logout")
        print("6. Exit")
        choice = input("\nChoose an option: ")
# =====================================================================================  1. Get User Assignments
        if choice == "1":
            get_assignments(user_id)
# =====================================================================================  2. Get/sort Assignments by date   
        elif choice == "2":
            get_assignments_not_done(user_id)
# =====================================================================================  3. Add an item to user Assignments (not sure if we'll use it in terminal)           
        elif choice == "3":
            add_assignment(user_id)
# =====================================================================================  4. Mark an assignment as Done
        elif choice == "4":
            mark_assignment_done(user_id)
# =====================================================================================  5. Logout
        elif choice == "5":
                print("\nLogging out...\n")
                return  "logout"# <-- sends user back to user select
# =====================================================================================  6. Exit
        elif choice == "6":
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
