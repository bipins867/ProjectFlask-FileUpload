from flask import Flask, request
from flask_restful import Api, Resource
from functools import wraps
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from UserAuthentication.Login import UserLogin, UserSignUp
from FileManagement.FileSystem import UploadFile, DownloadFile,DownloadFileLink

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:bipinsingh@localhost/flaskdb'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_ops_user = db.Column(db.Boolean, default=False)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class FileLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encoded = db.Column(db.String(255), nullable=False)
    fileId = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

class FileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = File

class FileLinkSchema(SQLAlchemyAutoSchema):
    class Meta:
        model=FileLink


api = Api(app)
api.add_resource(UserLogin, '/user/login', resource_class_kwargs={'db': db,'User':User})
api.add_resource(UserSignUp, '/user/signup', resource_class_kwargs={'db': db,'User':User})
api.add_resource(UploadFile, '/files/upload', resource_class_kwargs={'db': db,'User':User,'File':File})
api.add_resource(DownloadFileLink, '/files/download', resource_class_kwargs={'db': db,'User':User,'File':File,'FileLink':FileLink})
api.add_resource(DownloadFile,'/files/download/<string:encoded>',resource_class_kwargs={'db': db,'User':User,'File':File,'FileLink':FileLink})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
