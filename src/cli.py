import sqlite3
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from datetime import datetime
from getpass import getpass


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

    validated = set()
    for u in users:
        print(f"{u['id']}: {u['name']}")
        validated.add(u["id"])

    while True:
        user_input = input("\nEnter user ID: ").strip()

        if not user_input.isdigit():
            print("Please enter a valid number.")
            continue

        user_id = int(user_input)

        if user_id not in validated:
            print("Invalid user ID. Choose from the list above.")
            continue

        stored_hash = get_user_password_hash(user_id)
        if stored_hash is None:
            print("User not found. Try again.")
            continue

        # ================================
        # Password loop with lockout
        # ================================
        attempts = 0
        MAX_ATTEMPTS = 3

        while attempts < MAX_ATTEMPTS:
            password = getpass("Enter password: ").strip()

            if check_password_hash(stored_hash, password):
                print("Login successful!\n")
                return user_id
            else:
                attempts += 1
                remaining = MAX_ATTEMPTS - attempts
                print(f"Incorrect password. {remaining} attempt(s) remaining.\n")

        print("Too many failed attempts. Returning to user selection...\n")
        return None






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

    print("\n==================================================== Assignments ====================================================")
    print(f"{'ID'.ljust(5)} {'Name'.ljust(30)} {'Class'.ljust(30)} {'Category'.ljust(15)} {'Due Date'.ljust(15)} {'Status'.ljust(10)}")
    print("-" * 117)

    for item in items:
        class_name = item["class_name"]  
        if item["status"] == 0:
            status_text = "Not Done"
        elif item["status"] == 1:
            status_text = "Done"
        else:
            status_text = "Unknown"

        print(
            f"{str(item['id']).ljust(5)} "
            f"{item['name'].ljust(30)} "
            f"{class_name.ljust(30)} "
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
        SELECT id, name, class_name, category, due_date, status
        FROM assignments
        WHERE user_id = ? AND status = '0'
        ORDER BY due_date ASC
        """,
        (user_id,)
    ).fetchall()
    db.close()

    print("\n================================================ Assignments Not Done ===============================================")


    if not items:
        print("No assignments found.")
        return


    print(f"{'ID'.ljust(5)} {'Name'.ljust(30)} {'Class'.ljust(25)} {'Category'.ljust(15)} {'Due Date'.ljust(15)} {'Status'}")
    print("-" * 117)

    for item in items:
        class_name = item["class_name"]
        status_text = "Done" if item["status"] == "1" else "Not Done"

        print(
            f"{str(item['id']).ljust(5)} "
            f"{item['name'].ljust(30)} "
            f"{class_name.ljust(30)} "
            f"{item['category'].ljust(15)} "
            f"{item['due_date'].ljust(15)} "
            f"{status_text}"
        )




# =========================
# View Assignment Notes
# =========================
def view_assignment_notes(user_id):
    db = get_db()

    # Fetch only assignments that HAVE notes
    items = db.execute(
        """
        SELECT id, name, class_name, category, due_date, notes
        FROM assignments
        WHERE user_id = ?
          AND notes IS NOT NULL
          AND TRIM(notes) != ''
        ORDER BY name COLLATE NOCASE
        """,
        (user_id,)
    ).fetchall()

    # If no assignments have notes
    if not items:
        print("\n================================")
        print("\nNo assignments with notes found.")
        print("\n================================")
        db.close()
        return

    print("\n====================== Assignments With Notes ======================")
    print(f"{'ID'.ljust(5)} {'Name'.ljust(40)} {'Due Date'.ljust(15)}")
    print("-" * 60)

    for item in items:
        print(f"{str(item['id']).ljust(5)} {item['name'].ljust(40)} {item['due_date'].ljust(15)}")

    # Ask user which assignment to view
    try:
        assignment_id = int(input("\nEnter the ID of the assignment to view notes: "))
    except ValueError:
        print("Invalid input. Must be a number.")
        db.close()
        return

    # Fetch the notes for the selected assignment
    row = db.execute(
        """
        SELECT name, class_name, category, due_date, notes
        FROM assignments
        WHERE id = ? AND user_id = ?
          AND notes IS NOT NULL
          AND TRIM(notes) != ''
        """,
        (assignment_id, user_id)
    ).fetchone()

    db.close()

    if row is None:
        print("Invalid assignment ID or no notes for this assignment.")
        return

    print("\n===================== Notes ======================")
    print(f"Assignment: {row['name']}")
    print(f"Class:      {row['class_name']}")
    print(f"Category:   {row['category']}")
    print(f"Due Date:   {row['due_date']}")
    print("-" * 50)
    print(row["notes"])





# =========================
# add Assignments
# =========================


def validate_due_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_assignment(user_id):
    print("\n=== Add New Assignment ===")

    name = input("Assignment name: ").strip()
    class_name = input("Class name (ex: Software Engineering): ").strip()
    category = input("Category (ex: Essay, Homework, Lab): ").strip()

    # Loop until date is valid
    while True:
        due_date = input("Due date (YYYY-MM-DD): ").strip()

        if validate_due_date(due_date):
            break
        else:
            print("Invalid date format. Please use YYYY-MM-DD.\n")

    
    if not name or not class_name or not category:
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

    if user_id is None:
        return "logout"

    # =========
    # Main Menu
    # =========
    while True:
        print("\nOptions:")
        print("1. View Assignments")
        print("2. View Assignments Not Done")
        print("3. Add Assignments") # (a bit annoying in terminal)
        print("4. View Assignment Notes")
        print("5. Mark Assignment as Done")
        print("6. Logout")
        print("0. Exit")
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
# =====================================================================================  4. View Assignment Notes 
        elif choice == "4":
            view_assignment_notes(user_id)
# =====================================================================================  5. Mark an assignment as Done
        elif choice == "5":
            mark_assignment_done(user_id)
# =====================================================================================  6. Logout
        elif choice == "6":
                print("\nLogging out...\n")
                return  "logout"# <-- sends user back to user select
# =====================================================================================  0. Exit
        elif choice == "0":
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
