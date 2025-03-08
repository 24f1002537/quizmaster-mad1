from flask import Flask , render_template,request,session
from database import *
import matplotlib.pyplot as plt
import io
import base64


app = Flask(__name__)
app.app_context().push()
app.secret_key = 'your_secret_key'
#login
@app.route('/')
def login():
    return render_template('login.html')

#login action

@app.route('/submit',methods = ["Post"])
def submit():
    if((request.form['username']=="prakhar@gmail.com")&(request.form['password']=="admin")):
        sub = res_get_subject()
        chapter = re_get_chapter()
        if sub:
            return render_template('Admin.html',subject = sub,chap=chapter,get = True)
        return render_template('Admin.html')
    elif(check(request.form['username'],request.form['password'])):
        u_id = get_u_id(request.form['username'],request.form['password'])
        rep = get_qz_d()
        return render_template('user.html',u=u_id,a=rep,x=len(get_qz_d()[1]))
    return render_template('login.html',again=True)

#creating user

@app.route('/create')
def create():
    return render_template('create.html')

#registry of user

@app.route('/to_database',methods = ["Post"])
def create_user():
    if check(request.form['username'],request.form['password']):
        return render_template('create.html',again = True)
    if ((request.form['username']=="prakhar@gmail.com")&(request.form['password']=="admin")):
        return render_template('create.html',again = True)
    create_student(request.form['username'],request.form['password'],request.form['full_name'],request.form['Qualification'],request.form['dob'])
    return render_template('create.html',succes=True)

#adding subject page render

@app.route('/add')
def add():
    return render_template('add_subject.html')

#admin page render

@app.route('/admin')
def admin():
    sub = res_get_subject()
    chapter = re_get_chapter()
    if sub:
        return render_template('Admin.html',subject = sub,chap=chapter,get = True)
    return render_template('Admin.html')

#adding subject to database

@app.route('/add_sub',methods=['Post'])
def add_sub():
    if check_sub(request.form['Name']):
        return render_template('add_subject.html', again = True)
    add_subject(request.form['Name'],request.form['description'])
    return render_template('add_subject.html',succes = True)

#adding chapter tao database

@app.route('/add_chap/<sub_name>',methods=['Post'])
def add_cha(sub_name):
    if check_sub(sub_name):
        add_chap(request.form['Name'],request.form['description'],sub_name)
        return render_template('add_chap.html',succes = True)
    return render_template('add_chap',again = True)

#add chapter page render

@app.route('/add_chapter/<a>')
def add_chapter(a):
    return render_template('add_chap.html',sub_name=a)

#quiz management page render

@app.route('/quizmg')
def quizmg():
    c = get_id()
    return render_template('quiz_managment.html',get=True,chap=c)

#adding quiz page render

@app.route('/add_quiz')
def add_quiz():
    return render_template('add_quiz.html')

#add quiz to database

@app.route('/add_quiz/quiz',methods=['Post'])
def quiz():
    if check_ch(request.form['chid']):
        add_entry_quiz(request.form['chid'],request.form['date'],request.form['time'],request.form['remark'])
        return render_template('add_quiz.html',succes=True)
    return render_template('add_quiz.html',again = True)

#add question page render

@app.route('/add_question/<i>')
def add_question(i):
    return render_template('add_question.html',q_id=i)

#add question to database

@app.route('/add_question/question/<q_id>',methods=['Post'])
def add_q(q_id):
    question_add(q_id,request.form['q_state'],request.form['option1'],request.form['option2'],request.form['option3'],request.form['option4'],request.form['croption'],request.form['Chapter_ID'],request.form['q_t'])
    return render_template('add_question.html',succes=True)

#user id home retrive

@app.route('/user/<id>')
def user(id):
    rep = get_qz_d()
    return render_template('user.html',u=id,a=rep,x=len(get_qz_d()[1]))

#quiz detail viewer

@app.route('/view/<id>/<u_id>')
def view(id,u_id):
    return render_template('detail_view.html',a=get_q_full_d(id),b=u_id)

#go to main quiz 

@app.route('/start_quiz/<int:id>/<int:u_id>', methods=['GET','POST'])
def start_quiz(id,u_id):
    QUESTIONS = question_get(id)
    if 'current_index' not in session:
        session['current_index'] = 0
        session['score'] = 0

    current_index = session['current_index']

    # If the quiz is complete
    if current_index >= len(QUESTIONS):
        score = session.pop('score', 0)
        total_questions = len(QUESTIONS)
        session.pop('current_index', None)
        update_score(id,u_id,score)
        return render_template('start_quiz.html', current_question=None, score=score, total_questions=total_questions,a=id,b=u_id)

    question_data = QUESTIONS[current_index]

    if request.method == 'POST':
        user_answer = request.form['user_answer']
        correct_answer = question_data['answer']
        if user_answer == correct_answer:
            session['score'] += 1
        session['current_index'] += 1

        

    return render_template(
        'start_quiz.html',
        current_question=question_data['question'],
        options=question_data['options'],
        question_number=current_index + 1,a=id,b=u_id
    )

#delete/edit1

@app.route('/delete/<name>')
def delete(name):
    delete_chap(name)
    sub = res_get_subject()
    chapter = re_get_chapter()
    if sub:
        return render_template('Admin.html',subject = sub,chap=chapter,get = True)
    return render_template('Admin.html')

@app.route('/edit/<name>')
def redirecting_update(name):
    return render_template('edit.html',a=eget_chap(name))

@app.route('/update_chap/<id>',methods=['Post'])
def up_chap(id):
    print(request.form['Name'])
    update_chap(id,request.form['Name'],request.form['desc'],request.form['subject'])
    sub = res_get_subject()
    chapter = re_get_chapter()
    if sub:
        return render_template('Admin.html',subject = sub,chap=chapter,get = True)
    return render_template('Admin.html')


#delete/edit2

@app.route('/edit2/<id>')
def edit_q(id):
    b = getqbyquesid(id)
    return render_template('edit2.html',a=b,i=id)

@app.route('/edit_q/<id>',methods=['POST'])
def edit_q_u(id):
    update_q(request.form['Chapter_ID'],request.form['q_t'],request.form['q_state'],request.form['option1'],request.form['option2'],request.form['option3'],request.form['option4'],request.form['croption'],id)
    c = get_id()
    return render_template('quiz_managment.html',get=True,chap=c)


@app.route('/delete2/<id>')
def del_q(id):
    delete_q(id)
    c = get_id()
    return render_template('quiz_managment.html',get=True,chap=c)


#search admin/user

@app.route('/search',methods=['GET','POST'])
def search():
    b=get_search(request.form['s'])
    if b:
        return render_template('Admin.html',search=True,a=b)
    return render_template('Admin.html',search = True)

@app.route('/search/<id>',methods=['GET','POST'])
def searc(id):
    b=get_searc(request.form['s'],id)
    if b:
       return render_template('user.html',search=True,l=b,u=id)
    return render_template('user.html',search=True,u=id)
    
#display scores

@app.route('/scores/<id>')
def scores(id):
    a = final_score(id)
    return render_template('scores.html',a=a,u=id)


#summary user/admin

@app.route('/summary/<id>')
def usummary(id):
    x = [i for i in sum_for_user(id).values()]
    y = [i for i in sum_for_user(id).keys()]

    plt.bar(y,x)

    plt.xlabel('Subjects')

    plt.ylabel('Total marks')

    img_buffer = io.BytesIO()

    plt.savefig(img_buffer,format="png")
    img_buffer.seek(0)

    img_data = base64.b64encode(img_buffer.read()).decode('utf-8')

    return render_template('summary.html',user=True,chart=img_data,u=id)

@app.route('/summary')
def asummary():
    a = final_score()
    l=[]
    for z in a:
        x = [i for i in z.values()]
        y = [i for i in z.keys()]

        plt.bar(y,x)

        plt.xlabel('Subjects')

        plt.ylabel('Total marks')

        img_buffer = io.BytesIO()

        plt.savefig(img_buffer,format="png")
        img_buffer.seek(0)

        img_data = base64.b64encode(img_buffer.read()).decode('utf-8')
        l.append(img_data)
    return render_template('summary.html',admin=True,chart=l)



if __name__ == '__main__':
    app.run(debug=True)
