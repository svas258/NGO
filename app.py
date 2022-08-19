from curses import flash
import sqlite3
from flask import Flask, redirect, render_template, request, url_for 
app = Flask(__name__)
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur=conn.cursor()
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', datas=posts)

@app.route('/add_ngo',methods=['POST','GET'])
def add_ngo(): 
    if request.method=='POST':
        NGO_NAME=request.form['NGO_NAME']
        contact_No=request.form['contact_No']
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM posts where NGO_NAME=?",['NGO_NAME'])
        # if cur is not None:
        #     error = "User already exists"
        #     return render_template("index.html", error=error)
        cur.execute("insert into posts(NGO_NAME,contact_No) values (?,?)",(NGO_NAME,contact_No))
        conn.commit()
        flash(u'User added')
        return redirect(url_for("index"))
    return render_template("add_ngo.html")

@app.route('/edit_ngo/<string:id>',methods=['POST','GET'])
def edit_ngo(id):
    if request.method=='POST':
        NGO_NAME=request.form['NGO_NAME']
        contact_No=request.form['contact_No']
        con=sqlite3.connect("database.db")
        cur=con.cursor(dictionary=True, buffered=True)
        old_user = cur.execute("SELECT * FROM posts where NGO_NAME=?",['NGO_NAME'])
        if old_user:
            error = "User already exists"
            return render_template("edit_ngo.html", error=error)
        cur.execute("update posts set NGO_NAME=?,contact_No=? where id=?",(NGO_NAME,contact_No,id))
        con.commit()
        flash('User Updated','success')
        return redirect(url_for("index"))
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from posts where id=?",(id,))
    data=cur.fetchone()
    return render_template("edit_ngo.html",datas=data)


if __name__ == '__main__':
    app.run(debug = True)