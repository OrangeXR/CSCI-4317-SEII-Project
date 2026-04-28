import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "astra.db")

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


# =============================================================
# USER FUNCTIONS
# =============================================================

# ==========================================
# Create User 
# ==========================================

def create_user(name, username, password_hash):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO users (name, username, password_hash, profile_picture)
        VALUES (?, ?, ?, ?)
    """, (name, username, password_hash, "default.png"))
    db.commit()
    db.close()




# ==========================================
# Get User by Username
# ==========================================

def get_user_by_username(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    db.close()
    return row

# ==========================================
# Get User by id
# ==========================================

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    db.close()
    return row


# ==========================================
# Upload profile_pic
# ==========================================

def update_profile_picture(user_id, filename):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE users
        SET profile_picture = ?
        WHERE id = ?
    """, (filename, user_id))
    db.commit()
    db.close()


# =============================================================
# ASSIGNMENT FUNCTIONS
# =============================================================

# ======================================
# Get All Assignments (for specified user)
# ======================================

def get_all_assignments(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM assignments
        WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    db.close()
    return rows



# ======================================
# Get done Assignments
# ======================================

def get_done_assignments(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM assignments
        WHERE user_id = ? AND status = 1
        ORDER BY due_date DESC
    """, (user_id,))
    rows = cursor.fetchall()
    db.close()
    return rows


# ======================================
# Get Assignments by id
# ======================================
def get_assignment(assignment_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM assignments WHERE id = ?", (assignment_id,))
    row = cursor.fetchone()
    db.close()
    return row



# ======================================
# Add Assignment 
# ======================================

def add_assignment(user_id, name, class_name, category, due_date, notes, file_path):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO assignments (user_id, name, class_name, category, due_date, status, notes, file_path)
        VALUES (?, ?, ?, ?, ?, 0, ?, ?)
    """, (user_id, name, class_name, category, due_date, notes, file_path))
    db.commit()
    assignment_id = cursor.lastrowid
    db.close()
    return assignment_id



# ==================================
# Update Assignment 
# ==================================

def update_assignment(assignment_id, name, class_name, category, due_date, notes, file_path):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE assignments
        SET name = ?, class_name = ?, category = ?, due_date = ?, notes = ?, file_path = ?
        WHERE id = ?
    """, (name, class_name, category, due_date, notes, file_path, assignment_id))
    db.commit()
    db.close()


# ==================================
# Update Assignment Files
# ==================================
def update_assignment_files(assignment_id, file_paths_str):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE assignments
        SET file_path = ?
        WHERE id = ?
    """, (file_paths_str, assignment_id))
    db.commit()
    db.close()


# ==================================
# Remove file from Assignment
# ==================================
def remove_file_from_assignment(assignment_id, new_file_path_str):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE assignments
        SET file_path = ?
        WHERE id = ?
    """, (new_file_path_str, assignment_id))
    db.commit()
    db.close()



# ==================================
# Mark Assignment Done
# ==================================

def mark_assignment_done(assignment_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE assignments
        SET status = 1
        WHERE id = ?
    """, (assignment_id,))
    db.commit()
    db.close()



# ==================================
# Delete Assignment
# ==================================

def delete_assignment(assignment_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
    db.commit()
    db.close()



