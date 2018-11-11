#!/usr/bin/python3
from model import db
import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from ClassStructure import UserClass , FileClass, FolderClass
#from BusinessLayer 
import BusinessLayer

# app=Flask(__name__)
app = Flask(__name__)
BusinessLayer = BusinessLayer.BusinessLayer();

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/prakashjha/Desktop/nitish/scripting_project-master/dropbox.db'
db_path = os.path.join(os.path.dirname(__file__), 'dropbox.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
app.debug = True

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STORAGE_PATH = APP_ROOT + str('/Repository')


@app.route('/')
def landingPage():
    return render_template("login.html")

@app.route('/validate',methods=['POST'])
def validate():
    error=None
    if request.method == "POST":

        username = request.form.get('username')
        password = request.form.get('password')

        UserData = BusinessLayer.ValidateUser(username,password)

        if 'InvalidLogin' in UserData:
            if UserData['InvalidLogin'] == 'Invalid Login Attempt':  
                return render_template("login.html",error=error)
        else:
            folderId =BusinessLayer.getHomeFolderId(UserData['UserDetails'].userid)
            return redirect(url_for('index', userId = UserData['UserDetails'].userid,folderId = folderId))
    else:
        return render_template('login.html')


@app.route('/registerUser',methods=['POST','GET'])
def registerUser():
    if request.method == "POST":
        
        email = request.form.get('email')
        psw = request.form.get('psw')
        repsw = request.form.get('repsw')

        userexist = BusinessLayer.isUserExist(email)

        if userexist == True:
            error = "error"
            return render_template("login.html",error=error)
        else:
            ucobj = UserClass()
            ucobj.setUserDetails(email,email,psw,email,email,email)
            UserData = BusinessLayer.RegisterUser(ucobj)

            return render_template("index.html",UserData=UserData,currentFolderId = "1")                

    else:
        return render_template('login.html')    

@app.route('/logout')
def logout():

    return redirect(url_for('/'))

@app.route('/index')
@app.route('/index/<string:userId>/<string:folderId>')
def index(userId='1',folderId='3'):

	UserData = {}
	#UserData["UserDetails"] = UserClass()
	UserData = BusinessLayer.getFolderContents(userId,folderId)
	#print(UserData["FileDetails"][0].filename)
	
	#return **UserData['FileDetails']
	return render_template('test.html',**UserData,currentFolderId = folderId)



@app.route('/opendirectory', methods=['POST'])
def opendirectory(temp):
    
    if request.method == "POST":

        folderId = request.form.get('folderId')
        userId = request.form.get('userId')

        # path = BusinessLayer.getPathForFile(userId,folderId)
        UserData = BusinessLayer.getFolderContents(userId,folderId)

        return render_template('index.html',UserData=UserData,currentFolderId=folderId)
    else:
        return render_template('404.html')    


@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":

        fileName = request.form.get('fileName')
        userId = request.method.get('userId')
        UserData = BusinessLayer.searchFile(userId,fileName)

        return render_template('index.html',UserData=UserData,currentFolderId="")

    else:
        return render_template("404.html")


@app.route("/upload", methods=["POST"])
def upload():

    if request.method == "POST":

        currentFolderId = request.form.get('folderId')
        userId = request.form.get('userId')
        path = BusinessLayer.getPathForFile(userId,currentFolderId)

        target = os.path.join(APP_STORAGE_PATH,path)

        if not os.path.isdir(target):
                os.mkdir(target)

        for upload in request.files.getlist("file"):

            filename = upload.filename
            destination = "/".join([target, filename])
            upload.save(destination)

        UserData = BusinessLayer.getFolderContents(userId,currentFolderId)
        return render_template('index.html',UserData=UserData,currentFolderId=currentFolderId)

    else:
        return render_template("404.html")            


@app.route('/download/<string:id>/<string:filename>')
def download(id, filename):
    print("Filename is: ", filename)
    path = APP_STORAGE_PATH
    path += filename
    print("Path to download is: ", path)
    try:
        return send_file(path, as_attachment=True)
    except Exception as e:
        print(e)
    return render_template('download.html', id=id)


@app.route("/createfolder",methods=["POST"])
def createfolder():

    if request.method == "POST":
        
        userId = request.form.get('userId')
        foldername = request.form.get('foldername')
        currentFolderId = request.form.get('folderId')

        UserData = BusinessLayer.createfolder(userId,currentFolderId,foldername)
        return render_template('index.html',UserData=UserData,currentFolderId=currentFolderId)

    else:
        return render_template("404.html")     

@app.route("/permission/<userId>/<fileId>/<perms>")
def permission(userId,fileId,perms):
    
    UserData = BusinessLayer.changePermission(userId,fileId,perms)
    currentFolderId = BusinessLayer.getParentFolderId(userId,fileId)

    return render_template('index.html',UserData=UserData,currentFolderId=currentFolderId)


@app.route('/aboutus')
def aboutus():

    return render_template('aboutus.html')

@app.route('/myfiles',methods = ["POST"])
def myfiles():

    if request.method == "POST":
        
        userId = request.form.get('userId')
        
        UserData = BusinessLayer.getAllFiles(userId)
        return render_template('index.html',UserData=UserData,currentFolderId="")

    else:
        return render_template("404.html")

@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html')

if __name__=='__main__':
    app.run(debug=True)
