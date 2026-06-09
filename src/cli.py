import sqlite3
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from datetime import datetime
from getpass import getpass
from colorama import Fore, Back, Style, init
init(autoreset=True)

# ================================
# Setting Color Variables
# ================================

ORANGE = "\033[38;5;208m"   # bright orange
RED = "\033[38;5;196m"        # Overdue
YELLOW = "\033[38;5;226m"     # Due today
PINK = "\033[38;5;205m"       # Due in 3 days
PURPLE = "\033[38;5;141m"     # Due in 5 days
BLUE = "\033[38;5;75m"        # Due in 7 days
GREEN = "\033[38;5;82m"       # Done
BLINK = "\033[5m"
BOLD = "\033[1m"
RESET = Style.RESET_ALL

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
                print(Fore.GREEN + "Login successful!\n")
                return user_id
            else:
                attempts += 1
                remaining = MAX_ATTEMPTS - attempts
                print(Fore.RED + f"Incorrect password. {remaining} attempt(s) remaining.\n")

        print(Fore.YELLOW + "Too many failed attempts. Returning to user selection...\n")
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

    print(ORANGE + "\n==================================================== Assignments ====================================================" + RESET)
    print(f"{'ID'.ljust(5)} {'Name'.ljust(30)} {'Class'.ljust(30)} {'Category'.ljust(15)} {'Due Date'.ljust(15)} {'Status'.ljust(10)}")
    print(ORANGE + "-" * 117 + RESET)

    for item in items:
        urgency = get_urgency_color(item["due_date"], item["status"])

        print(
            f"{str(item['id']).ljust(5)} "
            f"{item['name'].ljust(30)} "
            f"{item['class_name'].ljust(30)} "
            f"{item['category'].ljust(15)} "
            f"{item['due_date'].ljust(15)} "
            f"{urgency}"
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
        WHERE user_id = ? AND status = 0
        ORDER BY due_date ASC
        """,
        (user_id,)
    ).fetchall()
    db.close()

    print(ORANGE + "================================================ Assignments Not Done ===============================================" + RESET)


    if not items:
        print("No assignments found.")
        return


    print(f"{'ID'.ljust(5)} {'Name'.ljust(30)} {'Class'.ljust(25)} {'Category'.ljust(15)} {'Due Date'.ljust(15)} {'Status'}")
    print(ORANGE + "-" * 117 + RESET)

    for item in items:
        urgency = get_urgency_color(item["due_date"], item["status"])

        print(
            f"{str(item['id']).ljust(5)} "
            f"{item['name'].ljust(30)} "
            f"{item['class_name'].ljust(30)} "
            f"{item['category'].ljust(15)} "
            f"{item['due_date'].ljust(15)} "
            f"{urgency}"
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
        print(ORANGE + "\n================================" + RESET)
        print("\nNo assignments with notes found.")
        print(ORANGE + "\n================================" + RESET)
        db.close()
        return

    print(ORANGE + "\n====================== Assignments With Notes ======================" + RESET)
    print(f"{'ID'.ljust(5)} {'Name'.ljust(40)} {'Due Date'.ljust(15)}")
    print(ORANGE + "-" * 60 + RESET)

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


    
    print(ORANGE + "\n===================== Notes ======================" + RESET)
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
    print(ORANGE + "\n=== Add New Assignment ===" + RESET)

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

    print(Fore.GREEN + "\nAssignment added successfully!")




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

    print(ORANGE + "\n=========== Mark Assignment as Done ===========" + RESET)
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

    print(Fore.GREEN + "\nAssignment marked as Done!")



# =============================================================
# Added Features
# =============================================================

def delete_assignment(user_id):
    db = get_db()

    items = db.execute(
        "SELECT id, name FROM assignments WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    if not items:
        print(ORANGE + "\nNo assignments found." + RESET)
        db.close()
        return

    print(ORANGE + "\n=========== Delete Assignment ===========" + RESET)
    print(f"{'ID'.ljust(5)} {'Name'}")
    print("-" * 40)

    for item in items:
        print(f"{str(item['id']).ljust(5)} {item['name']}")

    try:
        assignment_id = int(input("\nEnter the ID to delete: "))
    except ValueError:
        print("Invalid input.")
        db.close()
        return

    db.execute(
        "DELETE FROM assignments WHERE id = ? AND user_id = ?",
        (assignment_id, user_id)
    )
    db.commit()
    db.close()

    print(Fore.GREEN + "\nAssignment deleted successfully!" + RESET)


def mark_assignment_not_done(user_id):
    db = get_db()

    items = db.execute(
        "SELECT id, name, status FROM assignments WHERE user_id = ? AND status = 1",
        (user_id,)
    ).fetchall()

    if not items:
        print(ORANGE + "\nNo completed assignments found." + RESET)
        db.close()
        return

    print(ORANGE + "\n=========== Mark Assignment as NOT Done ===========" + RESET)
    print(f"{'ID'.ljust(5)} {'Name'}")
    print("-" * 40)

    for item in items:
        print(f"{str(item['id']).ljust(5)} {item['name']}")

    try:
        assignment_id = int(input("\nEnter the ID to mark as NOT done: "))
    except ValueError:
        print("Invalid input.")
        db.close()
        return

    db.execute(
        "UPDATE assignments SET status = 0 WHERE id = ? AND user_id = ?",
        (assignment_id, user_id)
    )
    db.commit()
    db.close()

    print(Fore.GREEN + "\nAssignment marked as NOT done!" + RESET)



def edit_assignment(user_id):
    db = get_db()

    items = db.execute(
        "SELECT id, name FROM assignments WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    if not items:
        print(ORANGE + "\nNo assignments found." + RESET)
        db.close()
        return

    print(ORANGE + "\n=========== Edit Assignment ===========" + RESET)
    print(f"{'ID'.ljust(5)} {'Name'}")
    print("-" * 40)

    for item in items:
        print(f"{str(item['id']).ljust(5)} {item['name']}")

    try:
        assignment_id = int(input("\nEnter the ID to edit: "))
    except ValueError:
        print("Invalid input.")
        db.close()
        return

    row = db.execute(
        "SELECT * FROM assignments WHERE id = ? AND user_id = ?",
        (assignment_id, user_id)
    ).fetchone()

    if not row:
        print("Invalid assignment ID.")
        db.close()
        return

    print(ORANGE + "\nWhat would you like to edit?" + RESET)
    print("1. Name")
    print("2. Class")
    print("3. Category")
    print("4. Due Date")
    print("5. Notes")
    print("0. Cancel")

    choice = input("\nChoose: ").strip()

    field_map = {
        "1": ("name", "New name"),
        "2": ("class_name", "New class name"),
        "3": ("category", "New category"),
        "4": ("due_date", "New due date (YYYY-MM-DD)"),
        "5": ("notes", "New notes")
    }

    if choice not in field_map:
        print("Cancelled.")
        db.close()
        return

    column, prompt = field_map[choice]
    new_value = input(f"{prompt}: ").strip()

    db.execute(
        f"UPDATE assignments SET {column} = ? WHERE id = ? AND user_id = ?",
        (new_value, assignment_id, user_id)
    )
    db.commit()
    db.close()

    print(Fore.GREEN + "\nAssignment updated successfully!" + RESET)




def search_assignments(user_id):
    keyword = input("\nEnter search keyword: ").strip().lower()

    db = get_db()
    items = db.execute(
        """
        SELECT *
        FROM assignments
        WHERE user_id = ?
          AND (
                LOWER(name) LIKE ?
             OR LOWER(class_name) LIKE ?
             OR LOWER(category) LIKE ?
             OR LOWER(notes) LIKE ?
          )
        """,
        (user_id, f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
    ).fetchall()
    db.close()

    print(ORANGE + "\n=========== Search Results ===========" + RESET)

    if not items:
        print("No matching assignments found.")
        return

    for item in items:
        print(f"- {item['name']} ({item['class_name']}) — due {item['due_date']}")



def filter_assignments(user_id):
    print(ORANGE + "\nFilter by:" + RESET)
    print("1. Category")
    print("2. Class")
    print("3. Status (Done / Not Done)")
    print("0. Cancel")

    choice = input("\nChoose: ").strip()

    db = get_db()

    if choice == "1":
        category = input("Enter category: ").strip()
        query = """
            SELECT * FROM assignments
            WHERE user_id = ? AND category = ?
        """
        params = (user_id, category)

    elif choice == "2":
        class_name = input("Enter class name: ").strip()
        query = """
            SELECT * FROM assignments
            WHERE user_id = ? AND class_name = ?
        """
        params = (user_id, class_name)

    elif choice == "3":
        print("1. Done")
        print("2. Not Done")
        s = input("Choose: ").strip()
        status = 1 if s == "1" else 0
        query = """
            SELECT * FROM assignments
            WHERE user_id = ? AND status = ?
        """
        params = (user_id, status)

    else:
        print("Cancelled.")
        db.close()
        return

    items = db.execute(query, params).fetchall()
    db.close()

    print(ORANGE + "\n=========== Filter Results ===========" + RESET)

    if not items:
        print("No assignments found.")
        return

    for item in items:
        print(f"- {item['name']} ({item['class_name']}) — due {item['due_date']}")



def get_urgency_color(due_date, status):
    if status == 1:
        return GREEN + "Done" + RESET

    try:
        due = datetime.strptime(due_date, "%Y-%m-%d").date()
    except:
        return ORANGE + "No Date" + RESET

    today = datetime.today().date()
    days_left = (due - today).days

    if days_left < 0:
        return BLINK + BOLD + RED + "OVERDUE" + RESET
    elif days_left == 0:
        return YELLOW + "Due Today" + RESET
    elif days_left <= 3:
        return PINK + f"Due in {days_left}d" + RESET
    elif days_left <= 5:
        return PURPLE + f"Due in {days_left}d" + RESET
    elif days_left <= 7:
        return BLUE + f"Due in {days_left}d" + RESET
    else:
        return ORANGE + f"{days_left}d left" + RESET











































# =====================================================================================================
# =====================================================================================  MAIN MENU
# =====================================================================================================
def main():
    # ===========
    # Select User
    # ===========
    print(ORANGE + "\n=== Assignment Tracker ===" + RESET)
    user_id = choose_user()

    if user_id is None:
        return "logout"

    # =========
    # Main Menu
    # =========
    while True:
        print(Fore.CYAN + "\nOptions:")
        print(Fore.CYAN + "1." + Style.RESET_ALL + " View Assignments")
        print(Fore.CYAN + "2." + Style.RESET_ALL + " View Assignments Not Done")
        print(Fore.CYAN + "3." + Style.RESET_ALL + " Add Assignments")
        print(Fore.CYAN + "4." + Style.RESET_ALL + " Edit Assignment")
        print(Fore.CYAN + "5." + Style.RESET_ALL + " View Assignment Notes")
        print(Fore.CYAN + "6." + Style.RESET_ALL + " Mark Assignment as Done")
        print(Fore.CYAN + "7." + Style.RESET_ALL + " Mark Assignment as NOT Done")
        print(Fore.CYAN + "8." + Style.RESET_ALL + " Delete Assignment")
        print(Fore.CYAN + "9." + Style.RESET_ALL + " Filter Assignments")
        print(Fore.CYAN + "10." + Style.RESET_ALL + " Search Assignments")
        print(Fore.CYAN + "11." + Style.RESET_ALL + " Logout")
        print(Fore.CYAN + "0." + Style.RESET_ALL + " Exit")

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
# =====================================================================================  4. Edit an Assignment  
        elif choice == "4":
            edit_assignment(user_id)
# =====================================================================================  5. View Assignment Notes 
        elif choice == "5":
            view_assignment_notes(user_id)
# =====================================================================================  6. Mark an assignment as Done
        elif choice == "6":
            mark_assignment_done(user_id)
# =====================================================================================  7. Mark Assignment as Not Done
        elif choice == "7":
            mark_assignment_not_done(user_id)
# =====================================================================================  8. Delete Assignment
        elif choice == "8":
            delete_assignment(user_id)
# =====================================================================================  9. Filter Assignments
        elif choice == "9":
            filter_assignments(user_id)
# =====================================================================================  10. Search Assignments
        elif choice == "10":
            search_assignments(user_id)
# =====================================================================================  11. Logout
        elif choice == "11":
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
