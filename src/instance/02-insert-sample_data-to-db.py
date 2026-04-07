import sqlite3

# Inserts sample users and assignments into astra.db
# It was helpful at the start of the site/app
# but is no longer needed

conn = sqlite3.connect("src/instance/astra.db") # <-----  if database or tables are not found on your system check this line first
cursor = conn.cursor()

# ===============
# Sample users
# ===============
sample_users = [
    ("demo",   "demo", "scrypt:32768:8:1$IT3KjqtMgxIUZB1S$0cc425013292eac69df26608de00c8b9f028162d6b56ba08a16ec75e5277a3319b7d1f431f9a103527fb618bf92fc0f58f12dc51186833295cfd9284bdf99cfa",  "demo.png"),
    ("demo2", "demo2", "scrypt:32768:8:1$UIENB92CqyeJJyLg$1d7a6b3bd5d0bc9673627a380181e8734de2147eadb09aa3a1d16f917dd63ec1076223fd5c9d5afbade302f45683d344218659cdbb4fd10a2e45f9b1f3be2b2e", "demo2.png")
]



cursor.executemany("""
INSERT OR IGNORE INTO users (name, username, password_hash, profile_picture)
VALUES (?, ?, ?, ?)
""", sample_users)

# =========================================
# Get player IDs 
# (for demo, assign items to users)
# =========================================

cursor.execute("SELECT id FROM users WHERE name = ?", ("demo",))
demo_id = cursor.fetchone()[0]


cursor.execute("SELECT id FROM users WHERE name = ?", ("demo2",))
demo2_id = cursor.fetchone()[0]


sample_assignments = [
#   (id,        user_id,                      "name",                  "class_name",             "category",     "due_date",         "status")
    ( 1,        demo_id,             'Assignment 01',        'Software Engineering',                'Essay',   '2026-02-16',                1),
    ( 2,        demo_id,             'Assignment 02',        'Software Engineering',                'Essay',   '2026-02-17',                1),
    ( 3,        demo_id,             'Assignment 03',        'Software Engineering',                'Essay',   '2026-02-18',                1),  
    ( 4,       demo2_id,             'Assignment 01',        'Software Engineering',                'Essay',   '2026-02-16',                1),
    ( 5,       demo2_id,             'Assignment 02',        'Software Engineering',                'Essay',   '2026-02-17',                1),
    ( 6,       demo2_id,             'Assignment 03',        'Software Engineering',                'Essay',   '2026-02-18',                0)
]


cursor.executemany("""
INSERT INTO assignments (id, user_id, name, class_name, category, due_date, status)
VALUES (?,?,?,?,?,?,?)
""", sample_assignments)


conn.commit()
conn.close()
