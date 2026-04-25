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
#   (id,        user_id,      "name",              "class_name",             "category",   "due_date",        "status")
    (  1,       demo_id,       'Assignment 01',     'Software Engineering',    'Essay',      '2026-01-01',           0),
    (  2,       demo_id,       'Assignment 02',     'Data Structures',         'Essay',      '2026-01-08',           0),
    (  3,       demo_id,       'Assignment 03',     'Algorithms',              'Essay',      '2026-01-15',           0),
    (  4,       demo_id,       'Assignment 04',     'Software Engineering',    'Essay',      '2026-01-22',           0),
    (  5,       demo_id,       'Assignment 05',     'Data Structures',         'Essay',      '2026-01-29',           0),
    (  6,       demo_id,       'Assignment 06',     'Algorithms',              'Essay',      '2026-02-05',           0),
    (  7,       demo_id,       'Assignment 07',     'Software Engineering',    'Essay',      '2026-02-12',           0),
    (  8,       demo_id,       'Assignment 08',     'Data Structures',         'Essay',      '2026-02-19',           0),
    (  9,       demo_id,       'Assignment 09',     'Algorithms',              'Essay',      '2026-02-26',           0),
    ( 10,       demo_id,       'Assignment 10',     'Software Engineering',    'Essay',      '2026-03-05',           0),
    ( 11,       demo_id,       'Assignment 11',     'Data Structures',         'Essay',      '2026-03-12',           0),
    ( 12,       demo_id,       'Assignment 12',     'Algorithms',              'Essay',      '2026-03-19',           0),
    ( 13,       demo_id,       'Assignment 13',     'Software Engineering',    'Essay',      '2026-03-26',           0),
    ( 14,       demo_id,       'Assignment 14',     'Data Structures',         'Essay',      '2026-04-02',           0),
    ( 15,       demo_id,       'Assignment 15',     'Algorithms',              'Essay',      '2026-04-09',           0),
    ( 16,       demo_id,       'Assignment 16',     'Software Engineering',    'Essay',      '2026-04-16',           0),
    ( 17,       demo_id,       'Assignment 17',     'Data Structures',         'Essay',      '2026-04-23',           0),
    ( 18,       demo_id,       'Assignment 18',     'Algorithms',              'Essay',      '2026-04-30',           0),
    ( 19,       demo_id,       'Assignment 19',     'Software Engineering',    'Essay',      '2026-05-07',           0),
    ( 20,       demo_id,       'Assignment 20',     'Data Structures',         'Essay',      '2026-05-14',           0),
    ( 21,       demo_id,       'Assignment 21',     'Algorithms',              'Essay',      '2026-05-21',           0),
    ( 22,       demo_id,       'Assignment 22',     'Software Engineering',    'Essay',      '2026-05-28',           0),
    ( 23,       demo_id,       'Assignment 23',     'Data Structures',         'Essay',      '2026-06-04',           0),
    ( 24,       demo_id,       'Assignment 24',     'Algorithms',              'Essay',      '2026-06-11',           0),
    ( 25,       demo_id,       'Assignment 25',     'Software Engineering',    'Essay',      '2026-06-18',           0),
    ( 26,       demo_id,       'Assignment 26',     'Data Structures',         'Essay',      '2026-06-25',           0),
    ( 27,       demo_id,       'Assignment 27',     'Algorithms',              'Essay',      '2026-07-02',           0),
    ( 28,       demo_id,       'Assignment 28',     'Software Engineering',    'Essay',      '2026-07-09',           0),
    ( 29,       demo_id,       'Assignment 29',     'Data Structures',         'Essay',      '2026-07-16',           0),
    ( 30,       demo_id,       'Assignment 30',     'Algorithms',              'Essay',      '2026-07-23',           0),
    ( 31,       demo_id,       'Assignment 31',     'Software Engineering',    'Essay',      '2026-07-30',           0),
    ( 32,       demo_id,       'Assignment 32',     'Data Structures',         'Essay',      '2026-08-06',           0),
    ( 33,       demo_id,       'Assignment 33',     'Algorithms',              'Essay',      '2026-08-13',           0),
    ( 34,       demo_id,       'Assignment 34',     'Software Engineering',    'Essay',      '2026-08-20',           0),
    ( 35,       demo_id,       'Assignment 35',     'Data Structures',         'Essay',      '2026-08-27',           0),
    ( 36,       demo_id,       'Assignment 36',     'Algorithms',              'Essay',      '2026-09-03',           0),
    ( 37,       demo_id,       'Assignment 37',     'Software Engineering',    'Essay',      '2026-09-10',           0),
    ( 38,       demo_id,       'Assignment 38',     'Data Structures',         'Essay',      '2026-09-17',           0),
    ( 39,       demo_id,       'Assignment 39',     'Algorithms',              'Essay',      '2026-09-24',           0),
    ( 40,       demo_id,       'Assignment 40',     'Software Engineering',    'Essay',      '2026-10-01',           0),
    ( 41,       demo_id,       'Assignment 41',     'Data Structures',         'Essay',      '2026-10-08',           0),
    ( 42,       demo_id,       'Assignment 42',     'Algorithms',              'Essay',      '2026-10-15',           0),
    ( 43,       demo_id,       'Assignment 43',     'Software Engineering',    'Essay',      '2026-10-22',           0),
    ( 44,       demo_id,       'Assignment 44',     'Data Structures',         'Essay',      '2026-10-29',           0),
    ( 45,       demo_id,       'Assignment 45',     'Algorithms',              'Essay',      '2026-11-05',           0),
    ( 46,       demo_id,       'Assignment 46',     'Software Engineering',    'Essay',      '2026-11-12',           0),
    ( 47,       demo_id,       'Assignment 47',     'Data Structures',         'Essay',      '2026-11-19',           0),
    ( 48,       demo_id,       'Assignment 48',     'Algorithms',              'Essay',      '2026-11-26',           0),
    ( 49,       demo_id,       'Assignment 49',     'Software Engineering',    'Essay',      '2026-12-03',           0),
    ( 50,       demo_id,       'Assignment 50',     'Data Structures',         'Essay',      '2026-12-10',           0),
    ( 51,       demo_id,       'Assignment 51',     'Algorithms',              'Essay',      '2026-12-17',           0),
    ( 52,       demo_id,       'Assignment 52',     'Software Engineering',    'Essay',      '2026-12-24',           0),
    ( 53,       demo2_id,      'Assignment 01',     'Software Engineering',    'Essay',      '2026-01-01',           0),
    ( 54,       demo2_id,      'Assignment 02',     'Data Structures',         'Essay',      '2026-01-08',           0),
    ( 55,       demo2_id,      'Assignment 03',     'Algorithms',              'Essay',      '2026-01-15',           0),
    ( 56,       demo2_id,      'Assignment 04',     'Software Engineering',    'Essay',      '2026-01-22',           0),
    ( 57,       demo2_id,      'Assignment 05',     'Data Structures',         'Essay',      '2026-01-29',           0),
    ( 58,       demo2_id,      'Assignment 06',     'Algorithms',              'Essay',      '2026-02-05',           0),
    ( 59,       demo2_id,      'Assignment 07',     'Software Engineering',    'Essay',      '2026-02-12',           0),
    ( 60,       demo2_id,      'Assignment 08',     'Data Structures',         'Essay',      '2026-02-19',           0),
    ( 61,       demo2_id,      'Assignment 09',     'Algorithms',              'Essay',      '2026-02-26',           0),
    ( 62,       demo2_id,      'Assignment 10',     'Software Engineering',    'Essay',      '2026-03-05',           0),
    ( 63,       demo2_id,      'Assignment 11',     'Data Structures',         'Essay',      '2026-03-12',           0),
    ( 64,       demo2_id,      'Assignment 12',     'Algorithms',              'Essay',      '2026-03-19',           0),
    ( 65,       demo2_id,      'Assignment 13',     'Software Engineering',    'Essay',      '2026-03-26',           0),
    ( 66,       demo2_id,      'Assignment 14',     'Data Structures',         'Essay',      '2026-04-02',           0),
    ( 67,       demo2_id,      'Assignment 15',     'Algorithms',              'Essay',      '2026-04-09',           0),
    ( 68,       demo2_id,      'Assignment 16',     'Software Engineering',    'Essay',      '2026-04-16',           0),
    ( 69,       demo2_id,      'Assignment 17',     'Data Structures',         'Essay',      '2026-04-23',           0),
    ( 70,       demo2_id,      'Assignment 18',     'Algorithms',              'Essay',      '2026-04-30',           0),
    ( 71,       demo2_id,      'Assignment 19',     'Software Engineering',    'Essay',      '2026-05-07',           0),
    ( 72,       demo2_id,      'Assignment 20',     'Data Structures',         'Essay',      '2026-05-14',           0),
    ( 73,       demo2_id,      'Assignment 21',     'Algorithms',              'Essay',      '2026-05-21',           0),
    ( 74,       demo2_id,      'Assignment 22',     'Software Engineering',    'Essay',      '2026-05-28',           0),
    ( 75,       demo2_id,      'Assignment 23',     'Data Structures',         'Essay',      '2026-06-04',           0),
    ( 76,       demo2_id,      'Assignment 24',     'Algorithms',              'Essay',      '2026-06-11',           0),
    ( 77,       demo2_id,      'Assignment 25',     'Software Engineering',    'Essay',      '2026-06-18',           0),
    ( 78,       demo2_id,      'Assignment 26',     'Data Structures',         'Essay',      '2026-06-25',           0),
    ( 79,       demo2_id,      'Assignment 27',     'Algorithms',              'Essay',      '2026-07-02',           0),
    ( 80,       demo2_id,      'Assignment 28',     'Software Engineering',    'Essay',      '2026-07-09',           0),
    ( 81,       demo2_id,      'Assignment 29',     'Data Structures',         'Essay',      '2026-07-16',           0),
    ( 82,       demo2_id,      'Assignment 30',     'Algorithms',              'Essay',      '2026-07-23',           0),
    ( 83,       demo2_id,      'Assignment 31',     'Software Engineering',    'Essay',      '2026-07-30',           0),
    ( 84,       demo2_id,      'Assignment 32',     'Data Structures',         'Essay',      '2026-08-06',           0),
    ( 85,       demo2_id,      'Assignment 33',     'Algorithms',              'Essay',      '2026-08-13',           0),
    ( 86,       demo2_id,      'Assignment 34',     'Software Engineering',    'Essay',      '2026-08-20',           0),
    ( 87,       demo2_id,      'Assignment 35',     'Data Structures',         'Essay',      '2026-08-27',           0),
    ( 88,       demo2_id,      'Assignment 36',     'Algorithms',              'Essay',      '2026-09-03',           0),
    ( 89,       demo2_id,      'Assignment 37',     'Software Engineering',    'Essay',      '2026-09-10',           0),
    ( 90,       demo2_id,      'Assignment 38',     'Data Structures',         'Essay',      '2026-09-17',           0),
    ( 91,       demo2_id,      'Assignment 39',     'Algorithms',              'Essay',      '2026-09-24',           0),
    ( 92,       demo2_id,      'Assignment 40',     'Software Engineering',    'Essay',      '2026-10-01',           0),
    ( 93,       demo2_id,      'Assignment 41',     'Data Structures',         'Essay',      '2026-10-08',           0),
    ( 94,       demo2_id,      'Assignment 42',     'Algorithms',              'Essay',      '2026-10-15',           0),
    ( 95,       demo2_id,      'Assignment 43',     'Software Engineering',    'Essay',      '2026-10-22',           0),
    ( 96,       demo2_id,      'Assignment 44',     'Data Structures',         'Essay',      '2026-10-29',           0),
    ( 97,       demo2_id,      'Assignment 45',     'Algorithms',              'Essay',      '2026-11-05',           0),
    ( 98,       demo2_id,      'Assignment 46',     'Software Engineering',    'Essay',      '2026-11-12',           0),
    ( 99,       demo2_id,      'Assignment 47',     'Data Structures',         'Essay',      '2026-11-19',           0),
    (100,       demo2_id,      'Assignment 48',     'Algorithms',              'Essay',      '2026-11-26',           0),
    (101,       demo2_id,      'Assignment 49',     'Software Engineering',    'Essay',      '2026-12-03',           0),
    (102,       demo2_id,      'Assignment 50',     'Data Structures',         'Essay',      '2026-12-10',           0),
    (103,       demo2_id,      'Assignment 51',     'Algorithms',              'Essay',      '2026-12-17',           0),
    (104,       demo2_id,      'Assignment 52',     'Software Engineering',    'Essay',      '2026-12-24',           0)
]




cursor.executemany("""
INSERT INTO assignments (id, user_id, name, class_name, category, due_date, status)
VALUES (?,?,?,?,?,?,?)
""", sample_assignments)


conn.commit()
conn.close()
