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
if __name__ == '__main__':
    app.run(debug=True)
