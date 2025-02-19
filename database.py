import sqlite3
conn = sqlite3.connect('database.sqlite3')
cur = conn.cursor()
conn.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username_email TEXT NOT NULL,
    password TEXT UNIQUE NOT NULL,
    full_name TEXT,
    qualification TEXT,
    dob INTEGER
)''')
conn.commit()
conn.close()