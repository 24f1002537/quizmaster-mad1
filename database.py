import sqlite3
conn = sqlite3.connect('database.sqlite3')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY ,
    username_email TEXT NOT NULL,
    password TEXT UNIQUE NOT NULL,
    full_name TEXT,
    qualification TEXT,
    dob DATE
)''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS subject(
    id INTEGER PRIMARY KEY ,
    name TEXT,
    description TEXT
)''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS chapter(
    id INTEGER PRIMARY KEY ,
    name TEXT,
    description TEXT,
    sub_name TEXT,
    FOREIGN KEY (sub_name) REFERENCES subject(name))
''')
cur.execute('''CREATE TABLE IF NOT EXISTS quiz(
    id INTEGER PRIMARY KEY,
    chapter_id INTEGER,
    date_of_quiz DATE,
    time_duration TIME,
    remarks TEXT,
    FOREIGN KEY(chapter_id) REFERENCES chapter(id)
)''')
cur.execute('''CREATE TABLE IF NOT EXISTS question(
    id INTEGER PRIMARY KEY ,
    quiz_id INTEGER,
    question_statement TEXT,
    option_1 TEXT,
    option_2 TEXT,option_3 TEXT,option_4 TEXT,correct_option TEXT,chid TEXT,question_title TEXT,FOREIGN KEY(quiz_id) REFERENCES quiz(id)
)''')
cur.execute('''CREATE TABLE IF NOT EXISTS scores(
            id INTEGER PRIMARY KEY,
            quiz_id INTEGER,user_id INTEGER,time_stamp_of_atempt TIME,total_scored INTEGER,
            FOREIGN KEY(quiz_id) REFERENCES quiz(id),FOREIGN KEY(user_id) REFERENCES user(id)            
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
def add_subject(sub_nm,desc):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"INSERT INTO subject (name,description) VALUES(?,?)"
    cur.execute(query,(sub_nm.upper(),desc))
    con.commit()
    con.close()
def check_sub(usrnm):
    con =sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT id FROM subject WHERE name=?"
    cur.execute(query,(usrnm.upper(),))
    res = cur.fetchall()
    con.commit()
    con.close()
    if res:
        return True
    return False 
def res_get_subject():
    con =sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT name FROM subject"
    cur.execute(query)
    res = cur.fetchall()
    con.commit()
    con.close()
    return res
def add_chap(chap_nm,desc,sub_name):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"INSERT INTO chapter(name,description,sub_name) VALUES(?,?,?)"
    cur.execute(query,(chap_nm.upper(),desc,sub_name.upper()))
    con.commit()
    con.close()
def re_get_chapter():
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT * FROM chapter"
    cur.execute(query)
    res = cur.fetchall()
    con.commit()
    con.close()
    return res
def add_entry_quiz(ch_id,date,time,remark):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"INSERT INTO quiz(chapter_id,date_of_quiz,time_duration,remarks) VALUES(?,?,?,?)"
    cur.execute(query,(ch_id,date,time,remark))
    con.commit()
    con.close()
def check_ch(id):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT name FROM chapter WHERE id=?"
    cur.execute(query,(id,))
    res = cur.fetchall()
    con.commit()
    con.close()
    if res:
        return True
    return False
def get_ch():
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT name,id FROM chapter"
    cur.execute(query)
    res = cur.fetchall()
    con.commit()
    con.close()
    return res
def get_id():
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = "SELECT chapter_id,id FROM quiz"
    cur.execute(query)
    res = cur.fetchall()
    con.commit()
    con.close()
    return res
def question_add(q_id,q_state,o_1,o_2,o_3,o_4,co,id,q_t):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"INSERT INTO question(quiz_id,question_statement,option_1,option_2,option_3,option_4,correct_option,chid,question_title) VALUES(?,?,?,?,?,?,?,?,?)"
    cur.execute(query,(q_id,q_state,o_1,o_2,o_3,o_4,co,id,q_t))
    con.commit()
    con.close()
def quiz_id():
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = "SELECT id FROM quiz"
    cur.execute(query)
    res = cur.fetchall()
    con.commit()
    con.close()
    return res
