import sqlite3
from flask import Flask, redirect, render_template, request, url_for,flash,jsonify,session,g
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField,TextAreaField,IntegerField,PasswordField,SelectField
from wtforms.validators import InputRequired,Length,DataRequired,Email
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from flask_session import Session
import json,psycopg2

csrf = CSRFProtect()
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'ff6f300767d1d0c82e02cd79515d50becb5061421ca151c8'
csrf.init_app(app)
Session(app)

class UserForm(FlaskForm):
    NGO_NAME=StringField('NGO_NAME', validators=[InputRequired(),Length(min=4,max=20)])
    contact_No=IntegerField('contact_No',validators=[InputRequired()])
    Email_ID=StringField('Email_ID', validators=[DataRequired("E-mail required!"), Email("Please enter a valid e-mail!")])
class User(FlaskForm):
    user=StringField('User', validators=[InputRequired(),Length(min=4,max=20)])
    password=PasswordField(label=('Password'),validators=[DataRequired(), Length(min=8, message='Password should be at least %(min)d characters long')])
class Search(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur=conn.cursor()
    return conn

def search(search):
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute('SELECT * FROM posts WHERE NGO_NAME LIKE ? OR email LIKE ? OR contact_No LIKE ?', ["%"+search+"%"  , "%"+search+"%" , "%"+search+"%"])
        res=cur.fetchall()
        conn.close()
        return res

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route('/login', methods=['GET','POST'])
def login():
    error=None
    form=User()
    if request.method=='POST':
       if form.validate_on_submit():
                session['name'] = request.form.get('user')
                name=form.user.data
                password = form.password.data
                conn= get_db_connection()
                cur=conn.cursor()
                cur.execute("SELECT user FROM users where  user=?",(name,))
                u=cur.fetchone()
                #p=cur.execute("SELECT password FROM users where password=?",(password,)).fetchone()
                if u :
                    p=cur.execute("SELECT password FROM users where password=?",(password,))
                    pss=p.fetchone()
                    if pss:
                     posts = conn.execute('SELECT * FROM posts').fetchall()
                     conn.close()
                     #return render_template('index.html', datas=posts)
                     return redirect(url_for("index"))
                    else:
                        error = 'Invalid Credentials. Please try again.'   
                else:
                    error = 'Invalid Username. Please try again.'
       else:
           for field,errors in form.errors.items():
                for error in errors:
                    flash("Error in {}: {}".format(
                    getattr(form, field).label.text,
                    error
                ), 'error')

    return render_template('login.html', error=error)

@app.route('/get_data')
def get_data():
    if not session.get('name'):
        return redirect("/login")

    if(request.method =='GET'):
      conn = get_db_connection()
      posts = conn.execute("SELECT * FROM posts")
      posts_all=posts.fetchall()
      res = [list(i) for i in posts_all]
      row_header=[x[0] for x in posts.description]
      
      row_list=[]
      for row in res:
          row_list.append(dict(zip(row_header,row))) 
      return jsonify(row_list)

@app.route('/', methods=["GET", "POST"])
def index():
    if not session.get('name'):
        return redirect("/login")
    if request.method =='POST':
        data=dict(request.form)
        se=search(data["search"])
        return render_template('search_ngo.html', usr=se)
    else:
        se=[]

    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', datas=posts)

@app.route('/add_ngo/',methods=('POST','GET'))
@csrf.exempt
def add_ngo():
    if not session.get('name'):
        return redirect("/login")
    form=UserForm()
    if request.method=='POST':
        if form.validate_on_submit():
                name = form.NGO_NAME.data
                mobile = form.contact_No.data
                mail = form.Email_ID.data
                connection = sqlite3.connect('database.db')
                cur= connection.cursor()
                out=cur.execute("SELECT * FROM posts where contact_No=?",(mobile,)).fetchone()
                if out is None:
                  cur.execute("insert into posts(NGO_NAME,contact_No,email) values (?,?,?)",(name,mobile,mail))
                  connection.commit()
                  flash('User added', 'Success')
                  return redirect(url_for('index'))
                  posts = cur.execute("SELECT * FROM posts").fetchall()
                  connection.close()
                  return render_template('index.html',datas=posts)
                else:
                    flash('User already there', 'error')
                    return render_template('add_ngo.html')
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash("Error in {}: {}".format(
                    getattr(form, field).label.text,
                    error
                ), 'error')

    return render_template("add_ngo.html")

@app.route('/edit_ngo/<string:id>', methods=('POST','GET'))
@csrf.exempt
def edit_ngo(id):
    if not session.get('name'):
        return redirect("/login")
    form=UserForm()
    if request.method=='POST':
        #if form.validate():
           name= request.form.get('NGO_NAME')
           mobile= request.form.get('contact_No')
           mail= request.form.get('email')
           #name = form.NGO_NAME.data
           #mobile = form.contact_No.data
           #mail = form.Email_ID.data
           conn= get_db_connection()
           cur=conn.cursor()
           cur.execute("SELECT * FROM posts where contact_No=?",(mobile,))
           if cur.fetchone() is not None:
                flash('User already exists')
                data=conn.execute("select * from posts where id=?",(id,)).fetchone()
                return redirect(url_for("index"))
           else:
                cur.execute("update posts set NGO_NAME=?,contact_No=?,email=? where id=?",(name,mobile,mail,id))
                conn.commit()
                flash('User Updated','success')
                conn.close()
                return redirect(url_for("index"))
    conn = get_db_connection()
    data=conn.execute("select * from posts where id=?",(id,)).fetchone()
    conn.close()
    return render_template("edit_ngo.html",datas=data)     

@app.route("/delete_ngo/<string:id>",methods=['GET'])
def delete_user(id):
    if not session.get('name'):
        return redirect("/login")
    conn = get_db_connection()
    data=conn.execute("delete from posts where id=?",(id,))
    conn.commit()
    flash('User Deleted','warning')
    return redirect(url_for("index"))





if __name__ == '__main__':
    
    app.run(debug = True)

    
