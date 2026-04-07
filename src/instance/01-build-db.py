import sqlite3

# =================================================================
# Creates a database named astra.db with:
# user: id, name, username, password_hash, profile_picture
# assignment: id, user_id, name, class, category, due_date, status
# =================================================================

conn = sqlite3.connect("src/instance/astra.db") 
cursor = conn.cursor()

# ================================
# User table 
# ================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    profile_picture TEXT
)
""")

# ================================================
# Assignments table (items belong to current user)
# ================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    class_name INTEGER NOT NULL,
    category TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status BOOLEAN '0',
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")


conn.commit()
conn.close()