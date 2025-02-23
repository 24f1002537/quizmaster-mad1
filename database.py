import sqlite3
conn = sqlite3.connect('database.sqlite3')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username_email TEXT NOT NULL,
    password TEXT UNIQUE NOT NULL,
    full_name TEXT,
    qualification TEXT,
    dob DATE
)''')
conn.commit()
conn.close()
def check(usrnm,psw):
    con =sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT id FROM users WHERE username_email=? AND password = ?"
    cur.execute(query,(usrnm,psw))
    res = cur.fetchall()
    con.commit()
    con.close()
    if res:
        return True
    return False
def create_student(usrnm,psw,full_name,qual,dob):
    conn = sqlite3.connect('database.sqlite3')
    cur = conn.cursor()
    query = f"INSERT INTO users (username_email,password,full_name,qualification,dob) VALUES(?,?,?,?,?)"
    cur.execute(query,(usrnm,psw,full_name,qual,dob))
    conn.commit()
    conn.close()
