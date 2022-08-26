import sqlite3
from flask import Flask, redirect, render_template, request, url_for,flash,jsonify
from flask_wtf import FlaskForm
from  flask_wtf.csrf import CSRFProtect
from wtforms import BooleanField, StringField,TextAreaField,IntegerField
from wtforms.validators import InputRequired,Length,DataRequired,Email
import json,psycopg2

app = Flask(__name__,instance_relative_config=True)
app.config.from_mapping({'WTF_CSRF_ENABLED':True})
app.secret_key = 'ff6f300767d1d0c82e02cd79515d50becb5061421ca151c8'
csrf = CSRFProtect()
csrf.init_app(app)


num_elements_to_generate = 500

class UserForm(FlaskForm):
    NGO_NAME=StringField('NGO_NAME', validators=[InputRequired(),Length(min=4,max=20)])
    contact_No=IntegerField('contact_No',validators=[InputRequired()])
    Email_ID=StringField('Email_ID', validators=[DataRequired("E-mail required!"), Email("Please enter a valid e-mail!")])

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur=conn.cursor()
    return conn

@app.route('/get_data')
def get_data():
    if(request.method =='GET'):
      conn = get_db_connection()
      posts = conn.execute("SELECT * FROM posts where NGO_NAME=TEAMA")
      tr=[] 
      for v in posts:
          tr.append(v)
      return jsonify(tr)
      '''row_header=[x[0] for x in posts.description]
      row_list=[]
      rv=posts.fetchall()
      for row in rv:
          row_list.append(dict(zip(row_header,row))) 
      #return json.dumps(row_list, indent=4) '''

@app.route('/')
def index():
    #csrf.generate_csrf()
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', datas=posts)

@app.route('/add_ngo',methods=['POST','GET'])
@csrf.exempt
def add_ngo(): 
    form=UserForm()
    if request.method=='POST':
        if form.validate_on_submit():
          conn= get_db_connection()
          cur=conn.cursor()
          try:
                
            cur.execute("SELECT * FROM posts where contact_No=?",(contact_No,))
            if cur.fetchone() is not None:
                    flash('User already exists','error')
                    return render_template("add_ngo.html")
            else:
                    cur.execute("insert into posts(NGO_NAME,contact_No,email) values (?,?)",(NGO_NAME,contact_No,Email_ID))
                    conn.commit()
                    flash('User added', 'Success')
                    return render_template("index.html")
          except:
                 conn.rollback()
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    flash("Error in {}: {}".format(
                    getattr(form, field).label.text,
                    error
                ), 'error')
    return render_template("add_ngo.html")

@app.route('/edit_ngo/<string:id>',methods=['POST','GET'])
@csrf.exempt
def edit_ngo(id):
    if request.method=='POST':
        NGO_NAME=request.form['NGO_NAME']
        contact_No=request.form['contact_No']
        Email_ID=request.form['email']
        con=sqlite3.connect("database.db")
        cur=con.cursor()
        try:
           cur.execute("SELECT * FROM posts where NGO_NAME=?",(NGO_NAME,))
           if cur.fetchone() is not None:
                    flash('User already exists','error')
                    return render_template("User_exist.html")
           else:
                cur.execute("update posts set NGO_NAME=?,contact_No=?,email=? where id=?",(NGO_NAME,contact_No,email,id))
                con.commit()
                flash('User Updated','success')
                return redirect(url_for("index"))
        except:
            conn.rollback()
    conn = get_db_connection()
    data=conn.execute("select * from posts where id=?",(id,)).fetchone()
    conn.close()
    return render_template("edit_ngo.html",datas=data)

@app.route("/delete_ngo/<string:id>",methods=['GET'])
def delete_user(id):
    conn = get_db_connection()
    data=conn.execute("delete from posts where id=?",(id,))
    conn.commit()
    flash('User Deleted','warning')
    return redirect(url_for("index"))


if __name__ == '__main__':
    
    app.run(debug = True)

    
