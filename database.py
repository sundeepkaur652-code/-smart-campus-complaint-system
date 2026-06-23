import sqlite3

conn = sqlite3.connect('complaints.db')

cursor = conn.cursor()

# Users Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Complaints Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS complaints(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_type TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'Pending'
)
''')

conn.commit()
conn.close()

print("Database Created Successfully!")