from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import jwt
import os
from werkzeug.security import generate_password_hash,check_password_hash

JWT_SECRET=os.getenv('JWT_SECRET')


class UserLogin(Resource):
    def __init__(self,db,User):
        self.db=db
        self.User=User


    def post(self):
        data=request.get_json()

        try:

            email=data.get('email')
            password=data.get('password')
            
            

            
            existing_user=self.User.query.filter_by(email=email).first()

            if not existing_user:
                
                return jsonify({'status':"User don't Exists!"})

            passCond=check_password_hash(existing_user.password,password)

            if not passCond:
                return jsonify({'status':"Incorrect Password !"})

            #All the checking has been done

            obj={"email":email}
            token=jwt.encode(obj,JWT_SECRET,algorithm='HS256')

            return jsonify({'token':token})

            
        except:
            
            return jsonify({"status","Please provide all information <email,password,type>!"})
        

       
       
    

class UserSignUp(Resource):
    
    def __init__(self,db,User):
        self.db=db
        self.User=User
    

    def post(self):

        data=request.get_json()
        
        try:

            email=data.get('email')
            password=data.get('password')
            typeUser=data.get('is_ops_type')
        
            if typeUser==1 or typeUser=='1':
                typeUser=True
            else:
                typeUser=False

            existing_user=self.User.query.filter_by(email=email).first()

            
            if existing_user:
                return jsonify({'status':"User Already Exists!"})
            passw=generate_password_hash(password,salt_length=10)
            new_user=self.User(email=email,password=passw,is_ops_user=typeUser)

            self.db.session.add(new_user)
            self.db.session.commit();
        
            return jsonify({'status':"Signup Successfull!"})
        except:
            
            return jsonify({"status","Please provide all information <email,password,type>!"})
        
       
       