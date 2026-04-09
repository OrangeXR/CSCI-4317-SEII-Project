import sqlite3

def get_db():
    conn = sqlite3.connect("src/instance/astra.db")
    conn.row_factory = sqlite3.Row
    return conn



# ===============================
# 
# ===============================

def get_user_by_username(username):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row



# ===============================
# 
# ===============================

def get_all_assignments(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM assignments WHERE user_id = ?",
        (user_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows



# ===============================
# 
# ===============================

def add_assignment(user_id, name, class_name, category, due_date):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO assignments (user_id, name, class_name, category, due_date, status) VALUES (?, ?, ?, ?, ?, 0)",
        (user_id, name, class_name, category, due_date)
    )
    conn.commit()
    conn.close()



# ===============================
# 
# ===============================

def get_assignment(assignment_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM assignments WHERE id = ?", (assignment_id,))
    row = cur.fetchone()
    conn.close()
    return row



# ===============================
# Update Assignment
# ===============================

def update_assignment(assignment_id, name, class_name, category, due_date):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE assignments
        SET name = ?, class_name = ?, category = ?, due_date = ?
        WHERE id = ?
    """, (name, class_name, category, due_date, assignment_id))
    conn.commit()
    conn.close()



# ===============================
# 
# ===============================

def delete_assignment(assignment_id):
    conn = getdb()
    cur = conn.cursor()
    cur.execute("DELETE FROM assignments WHERE id=?", (assignment_id,))
    conn.commit()
    conn.close()

# ===============================
# 
# ===============================

def get_user_by_id(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row   



# ===============================
# Upload profile_pic
# ===============================

def update_profile_picture(user_id, filename):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET profile_picture = ? WHERE id = ?",
        (filename, user_id)
    )
    conn.commit()
    conn.close()