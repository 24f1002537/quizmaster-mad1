import sqlite3
from datetime import datetime
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
cur.execute('''
    CREATE TABLE IF NOT EXISTS subject(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT
)''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS chapter(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    sub_name TEXT,
    FOREIGN KEY (sub_name) REFERENCES subject(name))
''')
cur.execute('''CREATE TABLE IF NOT EXISTS quiz(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER,
    date_of_quiz DATE,
    time_duration TIME,
    remarks TEXT,
    FOREIGN KEY(chapter_id) REFERENCES chapter(id)
)''')
cur.execute('''CREATE TABLE IF NOT EXISTS question(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER,
    question_statement TEXT,
    option_1 TEXT,
    option_2 TEXT,option_3 TEXT,option_4 TEXT,correct_option TEXT,chid TEXT,question_title TEXT,FOREIGN KEY(quiz_id) REFERENCES quiz(id)
)''')
cur.execute('''CREATE TABLE IF NOT EXISTS scores(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER,user_id INTEGER,time_stamp_of_atempt TIME,total_scored INTEGER,date_of_quiz DATE,
            FOREIGN KEY(quiz_id) REFERENCES quiz(id),FOREIGN KEY(user_id) REFERENCES user(id)            
)''')

conn.commit()
conn.close()

#checking for valid user
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

#adding user to database

def create_student(usrnm,psw,full_name,qual,dob):
    conn = sqlite3.connect('database.sqlite3')
    cur = conn.cursor()
    query = f"INSERT INTO users (username_email,password,full_name,qualification,dob) VALUES(?,?,?,?,?)"
    cur.execute(query,(usrnm,psw,full_name,qual,dob))
    conn.commit()
    conn.close()

#adding subject to database
def add_subject(sub_nm,desc):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"INSERT INTO subject (name,description) VALUES(?,?)"
    cur.execute(query,(sub_nm.upper(),desc))
    con.commit()
    con.close()

#checking for valid chapter name

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

#getting subject detail 

def res_get_subject():
    con =sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT name FROM subject"
    cur.execute(query)
    res = cur.fetchall()
    con.commit()
    con.close()
    return res

#adding chapter to dabase

def add_chap(chap_nm,desc,sub_name):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"INSERT INTO chapter(name,description,sub_name) VALUES(?,?,?)"
    cur.execute(query,(chap_nm.upper(),desc,sub_name.upper()))
    con.commit()
    con.close()

# getting chapter detail for admin page

def re_get_chapter():
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT * FROM chapter"
    cur.execute(query)
    res = cur.fetchall()
    con.commit()
    con.close()
    return res

#taking entries to new quiz in dataabase

def add_entry_quiz(ch_id,date,time,remark):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"INSERT INTO quiz(chapter_id,date_of_quiz,time_duration,remarks) VALUES(?,?,?,?)"
    cur.execute(query,(ch_id,date,time,remark))
    con.commit()
    con.close()

#checking chapter id to verify entry to database

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

#gettting chapter name and id fron database

def get_ch():
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT name,id FROM chapter"
    cur.execute(query)
    res = cur.fetchall()
    con.commit()
    con.close()
    return res

#getting quiz id ad chapter id for quiz management render page

def get_id():
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = "SELECT chapter_id,id FROM quiz"
    cur.execute(query)
    res_1 = cur.fetchall()
    query = "SELECT name,id FROM chapter"
    cur.execute(query)
    res_2 = cur.fetchall()
    query = "SELECT quiz_id,question_title,id FROM question"
    cur.execute(query)
    res_3 = cur.fetchall()
    con.commit()
    con.close()
    return [res_1,res_2,res_3]

#adding question to database

def question_add(q_id,q_state,o_1,o_2,o_3,o_4,co,id,q_t):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"INSERT INTO question(quiz_id,question_statement,option_1,option_2,option_3,option_4,correct_option,chid,question_title) VALUES(?,?,?,?,?,?,?,?,?)"
    cur.execute(query,(q_id,q_state,o_1,o_2,o_3,o_4,co,id,q_t))
    con.commit()
    con.close()

#userid geter

def get_u_id(name,psw):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT id FROM users WHERE username_email=? AND password=?"
    cur.execute(query,(name,psw))
    res = cur.fetchall()
    con.commit()
    con.close()
    return res

#getting quiz detail

def get_qz_d():
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query="SELECT * FROM quiz"
    cur.execute(query)
    f=cur.fetchall()
    query = f"SELECT COUNT(id),quiz_id FROM question WHERE quiz_id=?"
    l = []
    for a in f:
        cur.execute(query,(a[0],))
        g = cur.fetchall()
        l.append(g)
    con.commit()
    con.close()
    return [f,l]

#view purpose

def get_q_full_d(id):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT * FROM quiz WHERE id =?"
    cur.execute(query,(id,))
    res_1 = cur.fetchall()
    query = f"SELECT COUNT(id) FROM question WHERE quiz_id=?"
    cur.execute(query,(id,))
    res_2 = cur.fetchall()
    query = f"SELECT name,sub_name FROM chapter WHERE id =?"
    cur.execute(query,(res_1[0][1],))
    res_3 = cur.fetchall()
    con.commit()
    con.close()
    return [res_1,res_2,res_3]

#

def question_get(id):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT question_statement,option_1,option_2,option_3,option_4,correct_option FROM question WHERE quiz_id=?"
    cur.execute(query,(id,))
    res1 = cur.fetchall()
    con.commit()
    con.close()
    res = []
    
    for a in res1:
        l={}
        l['question'] = a[0]
        l['options'] = [a[1],a[2],a[3],a[4]]
        l['answer'] = a[5]
        res.append(l)
    return res

#update scores

def update_score(id,u_id,score):
    con=sqlite3.connect('database.sqlite3')
    cur=con.cursor()
    query=f"INSERT INTO scores('quiz_id','user_id','time_stamp_of_atempt','total_scored','date_of_quiz') VALUES(?,?,DATETIME('now'),?,DATE('now'))"
    cur.execute(query,(id,u_id,score))
    con.commit()
    con.close()

def delete_chap(name):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    cur.execute("DELETE FROM chapter WHERE name = ?",(name,))
    con.commit()
    con.close()

def eget_chap(name):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT * FROM chapter WHERE name = ?",(name.upper(),))
    res = cur.fetchall()
    con.commit()
    con.close()
    return res



def update_chap(id,name,desc,subname):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    cur.execute("UPDATE chapter SET name = ?, description = ?, sub_name=? WHERE id=?",(name.upper(),desc,subname.upper(),id))
    con.commit()
    con.close()

#getting q by qid

def getqbyquesid(id):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    cur.execute('SELECT chid,question_title,question_statement,option_1,option_2,option_3,option_4,correct_option FROM question WHERE id = ?',(id,))
    res = cur.fetchall()
    con.commit()
    con.close()
    return res

#update quiz

def update_q(chid,q_t,q_s,o_1,o_2,o_3,o_4,c_o,id):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    cur.execute("UPDATE question SET chid = ?, question_title = ?, question_statement=? ,option_1=?,option_2=?,option_3=?,option_4=?,correct_option=? WHERE id=?",(chid,q_t,q_s,o_1,o_2,o_3,o_4,c_o,id))
    con.commit()
    con.close()

#delete quiz

def delete_q(id):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    cur.execute("DELETE FROM question WHERE id = ?",(id,))
    con.commit()
    con.close()

def get_search(name):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query= f"SELECT users.username_email,chapter.sub_name,scores.total_scored,chapter.name FROM users INNER JOIN scores ON users.id=scores.user_id INNER JOIN quiz ON scores.quiz_id=quiz.id INNER JOIN chapter ON quiz.chapter_id=chapter.id WHERE users.username_email=? OR chapter.sub_name=?"
    cur.execute(query,(name,name.upper()))
    res = cur.fetchall()
    con.commit()
    con.close()
    return res

def get_searc(name,uid):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query= f"SELECT chapter.sub_name,scores.total_scored,chapter.name,quiz.date_of_quiz FROM users INNER JOIN scores ON users.id=scores.user_id INNER JOIN quiz ON scores.quiz_id=quiz.id INNER JOIN chapter ON quiz.chapter_id=chapter.id WHERE (quiz.date_of_quiz=? OR scores.total_scored=?) AND users.id=?"
    cur.execute(query,(name,name,uid))
    res = cur.fetchall()
    con.commit()
    con.close()
    return res

def sum_for_user(id):
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    query = f"SELECT scores.total_scored,chapter.sub_name FROM users INNER JOIN scores ON users.id = scores.user_id INNER JOIN quiz ON scores.quiz_id = quiz.id INNER JOIN chapter ON quiz.chapter_id=chapter.id WHERE users.id = ?"
    cur.execute(query,(id,))
    a = cur.fetchall()
    con.commit()
    con.close()
    d={}
    for b in a:
        if b[1] in d.keys():
            d[b[1]] += b[0]
        else:
            d[b[1]] = b[0]
    return d

