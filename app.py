from flask import Flask , render_template,url_for,request
from database import *


app = Flask(__name__)
app.app_context().push()
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/submit',methods = ["Post"])
def submit():
    if((request.form['username']=="prakhar@gmail.com")&(request.form['password']=="admin")):
        sub = res_get_subject()
        chapter = re_get_chapter()
        if sub:
            return render_template('Admin.html',subject = sub,chap=chapter,get = True)
        return render_template('Admin.html')
    elif(check(request.form['username'],request.form['password'])):
        return render_template('user.html')
    return render_template('login.html',again=True)
@app.route('/create')
def create():
    return render_template('create.html')
@app.route('/to_database',methods = ["Post"])
def create_user():
    if check(request.form['username'],request.form['password']):
        return render_template('create.html',again = True)
    create_student(request.form['username'],request.form['password'],request.form['full_name'],request.form['Qualification'],request.form['dob'])
    return render_template('create.html',succes=True)
@app.route('/add')
def add():
    return render_template('add_subject.html')
@app.route('/admin')
def admin():
    sub = res_get_subject()
    chapter = re_get_chapter()
    if sub:
        return render_template('Admin.html',subject = sub,chap=chapter,get = True)
    return render_template('Admin.html')
@app.route('/add_sub',methods=['Post'])
def add_sub():
    if check_sub(request.form['Name']):
        return render_template('add_subject.html', again = True)
    add_subject(request.form['Name'],request.form['description'])
    return render_template('add_subject.html',succes = True)
@app.route('/add_chap/<sub_name>',methods=['Post'])
def add_cha(sub_name):
    if check_sub(sub_name):
        add_chap(request.form['Name'],request.form['description'],sub_name)
        return render_template('add_chap.html',succes = True)
    return render_template('add_chap',again = True)
@app.route('/add_chapter/<a>')
def add_chapter(a):
    return render_template('add_chap.html',sub_name=a)
@app.route('/quizmg')
def quizmg():
    q= get_ch()
    c = get_id()
    return render_template('quiz_managment.html',quiz = q ,get=True,chap=c)
@app.route('/add_quiz')
def add_quiz():
    return render_template('add_quiz.html')
@app.route('/add_quiz/quiz',methods=['Post'])
def quiz():
    if check_ch(request.form['chid']):
        add_entry_quiz(request.form['chid'],request.form['date'],request.form['time'],request.form['remark'])
        return render_template('add_quiz.html',succes=True)
    return render_template('add_quiz.html',again = True)
@app.route('/add_question/<i>')
def add_question(i):
    return render_template('add_question.html',q_id=i)

if __name__ == '__main__':
    app.run(debug=True)
