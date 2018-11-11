#!/usr/bin/python3

from model import db
import os,errno
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, send_file,session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from ClassStructure import UserClass , FileClass, FolderClass
import BusinessLayer

BusinessLayer = BusinessLayer.BusinessLayer()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_path = os.path.join(os.path.dirname(__file__), 'dropbox.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
app.debug = True

app.secret_key = os.urandom(24)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STORAGE_PATH = APP_ROOT + str('/Repository/')

@app.route('/')
def landingPage():
    return render_template("login.html")


@app.route('/validate', methods=['GET','POST'])
def validate():
    print("-------Inside Validate-------")
    error=None
    # if request.method == 'GET':
    #     print("-------Inside Validate method GET-------")
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     print("Username is: ", username, " and Password is: ",password)
    if request.method == 'POST':
        print("-------Inside Validate method POST-------")
        username = request.form.get('username')
        password = request.form.get('password')
        # print("Username is: ", username, " and Password is: ",password)
        
        UserData = BusinessLayer.ValidateUser(username,password)
        
        print("  #### ",UserData['UserDetails'].currentFolderId)

        AddToSession('userId',UserData['UserDetails'].userid)
        AddToSession('currentFolderId',UserData['UserDetails'].currentFolderId)

        if 'InvalidLogin' in UserData:
            if UserData['InvalidLogin'] == 'Invalid Login Attempt':  
                return render_template("login.html",error=error)
        else:
            print("---------User Validated------")
            userId = UserData['UserDetails'].userid
            print("Userid is: ", userId)
            
            homeFolder = BusinessLayer.getHomeFolderId(userId)
            print("HomeFolderId is: ", homeFolder.folderid)

            # UserData = BusinessLayer.getFolderContents(userId,currentFolderId)
            # UserData['UserDetails'] = 

            return redirect(url_for('index', userId = UserData['UserDetails'].userid,folderId = homeFolder.folderid))
    else:
        return render_template('login.html')


@app.route('/registerUser',methods=['POST','GET'])
def registerUser():
    error=None
    # print("hello")

    if request.method == 'POST':
        # print("hello1")
        email = request.form['email']
        pswd = request.form['psw']
        repswd = request.form['repswd']
        userName = request.form['username']
        name=request.form['name']
        # print("pswd "+pswd+" repswd "+repswd)
        # name= "userName"
        phone="9878989890"

        if(pswd!=repswd):
            error="Passwords do not match"
            return render_template('login.html',error=error)

        userexist = BusinessLayer.isUserExist(userName)

        if userexist == True:
            error="This username is already is use"
            return render_template("login.html",error=error)
        else:
            ucobj = UserClass()
            ucobj.setUserDetails(7,userName,name,pswd,email,phone)
            UserData = BusinessLayer.RegisterUser(ucobj)
            
            destination = "/".join([APP_STORAGE_PATH, UserData['UserDetails'].userName+"_home"])

            if not os.path.isdir(destination):
                os.mkdir(destination)

            return render_template("login.html")

    else:
        return render_template('404.html')


@app.route('/logout')
def logout():
    session.pop('userId', None)
    session.pop('currentFolderId', None)
    return render_template('login.html')
    # return redirect(url_for('/'))


@app.route('/index/<string:userId>/<string:folderId>')
def index(userId,folderId):

    print("user id: ",userId)
    print("folder id: ",folderId)
    
    #userId = RetrieveSessionDetails('userId')
    UserData = BusinessLayer.getFolderContents(userId, folderId)
    print(" &&&& ",UserData['UserDetails'].currentFolderId)
    AddToSession('currentFolderId',folderId)

    return render_template('index.html', **UserData)

#user object needed
@app.route('/opendirectory/<string:userId>/<string:folderId>/<string:foldername>')
def opendirectory(userId,folderId,foldername):

    UserData = BusinessLayer.getFolderContents(userId,folderId)
    
    userobj = UserData['UserDetails']
    # userobj.userid = userId
    # userobj.currentFolderId = folderId
    # userobj.currentFolderName = foldername

    AddToSession('userId',userId)

    return render_template('index.html',**UserData)


@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":

        fileName = request.form.get('fileName')
        userId = request.method.get('userId')
        UserData = BusinessLayer.searchFile(userId,fileName)

        return render_template('index.html',**UserData)

    else:
        return render_template("404.html")


@app.route("/upload", methods=["POST"])
def upload():

    if request.method == "POST":

        currentFolderId = request.form.get('folderId')
        userId = request.form.get('userId')

        print("userId: ",userId)
        print("currentFolderId: ",currentFolderId)


        path = BusinessLayer.getPathForFolder(userId,currentFolderId)
        # path = ""
        print("path: ",path)
        target = os.path.join(APP_STORAGE_PATH,path)
        print("Target path: ",target)

        if not os.path.isdir(target):
                os.mkdir(target)

        for upload in request.files.getlist("file"):
            
            filename = upload.filename
            destination = "/".join([target, filename])
            upload.save(destination)

            file_size = os.stat(destination).st_size
            print("file size: ",file_size)

            fileObj = FileClass()
            fileObj.setFileDetails(46,filename,0,file_size,userId,currentFolderId)

            fileObj = BusinessLayer.createFile(fileObj,userId,currentFolderId)
            print("7777777777777777777777777777777777777777777777777777path: ")
            print(fileObj)

        UserData = BusinessLayer.getFolderContents(userId,currentFolderId)
        return render_template('index.html',**UserData)

    else:
        return render_template("404.html")            


@app.route('/download/<userId>/<fileId>')
def download(userId, fileId):
    pass
    # print("Filename is: ", filename)
    # path = APP_STORAGE_PATH
    # path += filename
    # print("Path to download is: ", path)
    # try:
    #     return send_file(path, as_attachment=True)
    # except Exception as e:
    #     print(e)
    # return render_template('download.html', id=id)


@app.route("/createfolder",methods=["POST"])
def createfolder():

    if request.method == "POST":
        
        userId = request.form.get('userId')
        foldername = request.form.get('folder')
        currentFolderId = request.form.get('folderId')

        print("userId: " ,userId)
        print("FolderName: " ,foldername)
        print("currentFolderId: " ,currentFolderId)
        
        folderobj = BusinessLayer.createfolder(userId,currentFolderId,foldername)
        
        if folderobj != None:

            UserData = BusinessLayer.getFolderContents(userId,currentFolderId)
            path = BusinessLayer.getPathForFolder(userId,currentFolderId)

            print("APP_STORAGE_PATH: ",APP_STORAGE_PATH)
            target = APP_STORAGE_PATH+path
            
            # target = os.path.join(APP_STORAGE_PATH,path)
            destination = target+foldername
            # destination = "/".join([target, foldername])

            if not os.path.isdir(destination):
                    os.mkdir(destination)

            return render_template('index.html',**UserData)

        else:    

            return render_template("404.html")    
    else:
        return render_template("404.html")     

@app.route("/permission/<userId>/<fileId>/<perms>")
def permission(userId,fileId,perms):
    
    UserData = BusinessLayer.changePermission(userId,fileId,perms)
    # currentFolderId = BusinessLayer.getParentFolderId(userId,fileId)

    return render_template('index.html',**UserData)


@app.route('/aboutus')
def aboutus():

    return render_template('aboutus.html')


@app.route('/deleteFolder/<userId>/<fileId>')
def deleteFolder(userId,folderId):
    pass

@app.route('/deleteFile/<userId>/<fileId>')
def deleteFile(userId,fileId):
    pass

@app.route('/allfiles',methods = ["POST"])
def allfiles():

    if request.method == "POST":
        
        userId = request.form.get('userId')
        
        UserData = BusinessLayer.getAllFiles(userId)
        return render_template('index.html',**UserData)

    else:
        return render_template("404.html")

@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html')

def StoreSessionDetails(UserData):
    AddToSession('UserDetails',UserData['UserDetails'])     

def RetrieveSessionDetails(key):
    if session[key] != None:
        return session[key]
    return None

def AddToSession(key,value):
    session[key] = value


if __name__=='__main__':
    app.run(debug=True)

