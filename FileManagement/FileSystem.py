from flask import Flask, request, jsonify,send_file
from flask_restful import Api, Resource
from functools import wraps
import os
import jwt
import uuid

JWT_SECRET=os.getenv('JWT_SECRET')

def opsUser(f):
    @wraps(f)
    def decorated(self,*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'status':"Un-Authorized User!"})
        
        try:
            data=jwt.decode(token,JWT_SECRET,algorithms='HS256')

        except:

            return jsonify({'status':"Invalid Signature!"})
        
        existing_user=self.User.query.filter_by(email=data['email']).first()
        
        if not  existing_user.is_ops_user:
            return jsonify({'status':"You are not Authorized to Access this!"})

        return f(self,{'User':existing_user}, *args, **kwargs)
    return decorated


def clientUser(f):
    @wraps(f)
    def decorated(self,encoded,*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'status':"Un-Authorized User!"})
        
        try:
            data=jwt.decode(token,JWT_SECRET,algorithms='HS256')

        except:

            return jsonify({'status':"Invalid Signature!"})
        
        existing_user=self.User.query.filter_by(email=data['email']).first()
        
        if existing_user.is_ops_user:
            return jsonify({'status':"You are not Authorized to Access this!"})

        return f(self,{'User':existing_user,'encoded':encoded}, *args, **kwargs)
    return decorated


def writeContent2File(fileName,extension,cidx,fileContent):
    

    fileName=str(cidx)+'.'+extension

    fileLoc=os.path.join('.','Data',fileName)
    file=open(fileLoc,'wb')
   
    file.write(bytes(fileContent,'utf-8'))

    file.close()


class UploadFile(Resource):
    
    def __init__(self,db,User,File):
        self.db=db
        self.User=User
        self.File=File

    @opsUser
    def post(self,info):
        crrUser=info['User']
        data=request.get_json()

        try:

            fileName=data.get('fileName')
            fileContent=data.get('fileContent')

            extension=fileName.split('.')[-1]

            if extension not in ['pptx','docx','xlsx']:
                return jsonify({'status':"Upload file must be only of pptx,docx, and xlsx type"})

            newFile=self.File(filename=fileName,user_id=crrUser.id)
            
            
            self.db.session.add(newFile)
            self.db.session.commit()

            writeContent2File(fileName,extension,newFile.id,fileContent)
        except :
            return jsonify({'status':'Something went wrong'})
        
        
        return jsonify({"status":"File Uploaded Successfully!"})


class DownloadFileLink(Resource):
    
    def __init__(self,db,User,File,FileLink):
        self.db=db
        self.User=User
        self.File=File
        self.FileLink=FileLink
    
    @clientUser
    def get(self,info):

        try:
            fileInfo=self.File.query.all()
            fileData=[[file.id,file.filename] for file in fileInfo]
            
            return jsonify({'files':fileData})
        except:
            return jsonify({"status":"Something went wrong!"})
        
        

    @clientUser
    def post(self, info):
        data = request.get_json()
        crrUser=info['User']
        
        try:
            file_id = data.get('file_id')
            existinFile=self.File.query.filter_by(id=file_id).first()
            
            if not existinFile:
                return jsonify({"status":"Please enter correct File Id!"})
            encoded=uuid.uuid4().hex

        
            newFileLink=self.FileLink(encoded=encoded,fileId=existinFile.id,userId=crrUser.id)
            
            
            
            self.db.session.add(newFileLink)
            self.db.session.commit()

            return jsonify({"download-link" :f"http://127.0.0.1:5000/files/download/{encoded}",
                            "status":"Success"})

        except:
            return jsonify({'status':'Something went wrong!'})


class DownloadFile(Resource):
    
    def __init__(self,db,User,File,FileLink):
        self.db=db
        self.User=User
        self.File=File
        self.FileLink=FileLink

    @clientUser
    def get(self,info):
        
        crrUser=info['User']
        encoded=info['encoded']

        fileLink=self.FileLink.query.filter_by(encoded=encoded,userId=crrUser.id).first()
        
        if not fileLink:
            return jsonify({'status':'You are not Authorized to access the File!'})
        
        file=self.File.query.filter_by(id=fileLink.fileId).first()

        extension=file.filename.split('.')[-1]

        fileLocation=f'.\\Data\\{file.id}.{extension}'
        
        
        return send_file(fileLocation,as_attachment=True)
#encoded
   
   