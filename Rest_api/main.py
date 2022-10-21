
from enum import unique
from functools import wraps
from flask import Flask, make_response,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import uuid
import jwt
import datetime
from werkzeug.security import generate_password_hash,check_password_hash


app = Flask(__name__)
# basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']='ce7032d8a6cdcbba5354a92d29e684ce'
basedir=r"C:\Users\svas2\OneDrive\Desktop\PortableGit\NGO\NGO"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True

db=SQLAlchemy(app)
ma=Marshmallow(app)

class Users(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   public_id = db.Column(db.Integer)
   name = db.Column(db.String(50))
   password = db.Column(db.String(50))
   admin = db.Column(db.Boolean)

class posts(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    NGO_NAME=db.Column(db.String(100))
    contact_No=db.Column(db.Integer())
    email=db.Column(db.String())
    
    def __init__(self,NGO_NAME,contact_No,email):
        self.NGO_NAME=NGO_NAME
        self.contact_No=contact_No
        self.email=email



class UserSchema(ma.Schema):
    class Meta:
        fields=('id','NGO_NAME','contact_No','  ')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# jwt 
def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = request.args.get('tokens')
       if 'tokens' in request.headers:
           token = request.headers['tokens']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        #    current_user = Users.query.filter_by(public_id=data['public_id']).first()
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(*args, **kwargs)
   return decorator

@app.route('/register', methods=['POST'])
def signup_user(): 
   data = request.get_json() 
   hashed_password = generate_password_hash(data['password'], method='sha256')
 
   new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
   db.session.add(new_user) 
   db.session.commit()   
   return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['POST']) 
def login_user():
   auth = request.authorization  
   if not auth or not auth.username or not auth.password: 
       return make_response('could not verify', 401, {'Authentication': 'login required"'})   
 
   user = Users.query.filter_by(name=auth.username).first()  
   if check_password_hash(user.password, auth.password):
       token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
 
       return jsonify({'token' : token})
 
   return make_response('could not verify',  401, {'Authentication': '"login required"'})
   
@app.route('/users', methods=['GET'])
def get_all_users(): 
 
   users = Users.query.all()
   result = []  
   for user in users:  
       user_data = {}  
       user_data['public_id'] = user.public_id 
       user_data['name'] = user.name
       user_data['password'] = user.password
       user_data['admin'] = user.admin
     
       result.append(user_data)  
   return jsonify({'users': result})

#add new NGO details
@app.route('/user',methods=['POST'])
@token_required
def add_user():
    NGO_NAME=request.json['NGO_NAME']
    contact_No=request.json['contact_No']
    email=request.json['email']
    new_user=posts(NGO_NAME,contact_No,email)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)
#get all NGO details 
@app.route('/user', methods=['GET'])
@token_required
def getAllUser():
   all_users=posts.query.all()
   result=users_schema.dump(all_users)
   return jsonify(result)

#get NGO details by id
@app.route('/user/<id>', methods=['GET'])
@token_required
def getUserByid(id):
   user=posts.query.get(id)
   return user_schema.jsonify(user)

#update NGO details by id
@app.route('/user/<id>', methods=['PUT'])
@token_required
def UpdateUser(id):
   user=posts.query.get(id)
   NGO_NAME=request.json['NGO_NAME']
   contact_No=request.json['contact_No']
   email=request.json['email']
   user.NGO_NAME=NGO_NAME
   user.contact_No=contact_No
   user.email=email
   db.session.commit()
   return user_schema.jsonify(user)

#Dlete NGO details by id
@app.route('/user/<id>', methods=['DELETE'])
@token_required
def deleteuserByid(id):
    user=posts.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)



if __name__=='__main__':

    app.run(debug=True,port=7000)