from flask import Flask , render_template,url_for,request
import sqlite3

app = Flask(__name__)
app.app_context().push()
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/submit',methods = ["Post"])
def submit():
    if((request.form['username']=="prakhar@gmail.com")&(request.form['password']=="admin")):
        return render_template('Admin.html')
    return render_template('login.html',again=True)
@app.route('/create')
def create():
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)
