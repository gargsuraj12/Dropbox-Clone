#!/usr/bin/python3

from model import db
import os,errno
import shutil
from flask import Flask, render_template,send_from_directory,request, send_from_directory, redirect, url_for, send_file,session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from ClassStructure import UserClass , FileClass, FolderClass
import BusinessLayer
from mimetypes import MimeTypes
import urllib 

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

# @app.route('/')
# def landingPage():
#     return render_template("login.html")

@app.route('/')
def landingPage():
    print("----APP ROOT IS ACCESSED----")
    if len(session) != 0:
        print("------User already logged in------")
        return redirect(url_for('index',folderId = session['homeFolderId']))
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
        
        if("Invalid Login Attempt" in UserData.values()):

            error="Please check username or password !"
            return render_template("login.html",error=error)


        print("  #### ",UserData['UserDetails'].currentFolderId)

        AddToSession('userId',UserData['UserDetails'].userid)
        AddToSession('userName',UserData['UserDetails'].userName)
        AddToSession('currentFolderId',UserData['UserDetails'].currentFolderId)
        AddToSession('homeFolderId',UserData['UserDetails'].HomeFolderId)
        AddToSession('TotalSize',BusinessLayer.getTotalSize(UserData['UserDetails'].userid))

        foldername = UserData['UserDetails'].currentFolderName[:-1]

        AddToSession('currentFolderName',foldername)


        if 'InvalidLogin' in UserData:
            if UserData['InvalidLogin'] == 'Invalid Login Attempt':  
                return render_template("login.html",error=error)
        else:
            print("---------User Validated------")
            userId = UserData['UserDetails'].userid
            print("Userid is: ", userId)
            
            homeFolder = BusinessLayer.getHomeFolderId(userId)
            print("HomeFolderId is: ", homeFolder.folderid)

            return redirect(url_for('index',folderId = homeFolder.folderid))
    else:
        return render_template('login.html')


@app.route('/registerUser',methods=['POST','GET'])
def registerUser():

    error=None

    if request.method == 'POST':
        email = request.form['email']
        pswd = request.form['psw']
        repswd = request.form['repswd']
        userName = request.form['username']
        name=request.form['name']

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
    
    # session.pop('currentFolderName',None)    
    # session.pop('userId', None)
    # session.pop('userName',None)
    # session.pop('currentFolderId', None)
    # session.pop('homeFolderId',None)    

    session.clear()
    return render_template('login.html')
    

@app.route('/index/<folderId>')
def index(folderId):

    userId = RetrieveSessionDetails('userId')
    AddToSession('currentFolderId',folderId)
    foldername = BusinessLayer.getPathForFolder(userId,folderId)
    foldername = foldername[:-1]
    AddToSession('currentFolderName',foldername)
    #keyToAdd = 'PFDEL_'+foldername
    #AddToSession('directory_home',foldername)

    UserData = BusinessLayer.getFolderContents(userId, folderId)
    UserData["sourceParameter"]="NotsearchIndex" 
    UserData["AllFilesource"]="NotAllFileSource"
    # if BusinessLayer.getHomeFolderId(folderId) == folderId:
    #     UserData["homefolder"] = "home"
    # else:    
    #     UserData["homefolder"] = "nothome"

    userclassInstance = UserClass()
    userclassInstance.setUserDetails(RetrieveSessionDetails('userId'),RetrieveSessionDetails('userName'),"passwd","name","email","phone")
    userclassInstance.setCurrentFolderId(RetrieveSessionDetails('currentFolderId'))
    userclassInstance.setCurrentFolderName(RetrieveSessionDetails('currentFolderName'))
    userclassInstance.setHomeFolderId(RetrieveSessionDetails('homeFolderId'))

    UserData['TotalSize'] = RetrieveSessionDetails('TotalSize')
    UserData['UserDetails'] = userclassInstance
    return render_template('index.html', **UserData)

#search result is returning empty list always
@app.route('/search', methods=["POST"])
def search():

    userId = RetrieveSessionDetails('userId')
    fileName = request.form.get('fileName')
    
    if fileName == '':
        currentFolderId = RetrieveSessionDetails('currentFolderId')
        return redirect(url_for('index',folderId = currentFolderId))

    UserData = BusinessLayer.searchFile(userId,fileName)
    
    if UserData != None:
        # UserData['searchStatus'] = 'True'
        
        userclassInstance = UserClass()
        userclassInstance.setUserDetails(RetrieveSessionDetails('userId'),
        RetrieveSessionDetails('userName'),"passwd","name","email","phone")
        userclassInstance.setCurrentFolderId("0")
        userclassInstance.setCurrentFolderName("Search Result")
        userclassInstance.setHomeFolderId(RetrieveSessionDetails('homeFolderId'))

        UserData['UserDetails'] = userclassInstance        
        UserData["AllFilesource"]="NotAllFileSource"
        UserData["sourceParameter"]="searchSource"  
        
        print("Search Result: ",UserData['FileDetails'][0].filename)
        return render_template('index.html',**UserData)
        # return redirect(url_for('indexSearch',folderId = homeFolder.folderid))

    else:
        homeFolder = BusinessLayer.getHomeFolderId(userId)
        # UserData['searchStatus'] = 'False'
        AddToSession('searchResult','False')
        return redirect(url_for('index',folderId = homeFolder.folderid))


@app.route("/upload", methods=["POST"])
def upload():

    if request.method == "POST":

        userId = RetrieveSessionDetails('userId')
        currentFolderId = RetrieveSessionDetails('currentFolderId')

        print("userId: ",userId)
        print("currentFolderId: ",currentFolderId)

        path = BusinessLayer.getPathForFolder(userId,currentFolderId)
        
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
            print(fileObj)

        UserData = BusinessLayer.getFolderContents(userId,currentFolderId)

        AddToSession('TotalSize',BusinessLayer.getTotalSize(userId))
        
        return redirect(url_for('index',folderId = currentFolderId))    

    else:
        return render_template("404.html")            

@app.route('/download/<fileId>/<filename>')
def download(fileId,filename):

    path = APP_STORAGE_PATH

    userId = RetrieveSessionDetails('userId')
    currentFolderId = RetrieveSessionDetails('currentFolderId')

    path += BusinessLayer.getPathForFile(userId,fileId)
    path += filename
    
    try:
        return send_file(path, as_attachment=True)

    except Exception as e:
        print(e)

    return redirect(url_for('index',folderId = currentFolderId))


@app.route("/createfolder",methods=["POST"])
def createfolder():

    if request.method == "POST":
        
        userId = RetrieveSessionDetails('userId')
        currentFolderId = RetrieveSessionDetails('currentFolderId')

        foldername = request.form.get('folder')
        
        if foldername != '':
            folderobj = BusinessLayer.createfolder(userId,currentFolderId,foldername)
                
            if folderobj != None:

                UserData = BusinessLayer.getFolderContents(userId,currentFolderId)
                path = BusinessLayer.getPathForFolder(userId,currentFolderId)

                print("APP_STORAGE_PATH: ",APP_STORAGE_PATH)
                target = APP_STORAGE_PATH+path
                
                destination = target+foldername
                
                if not os.path.isdir(destination):
                    os.mkdir(destination)
                    return redirect(url_for('index',folderId = currentFolderId))                            
                else:  
                    return render_template("404.html")
        else:
            return redirect(url_for('index',folderId = currentFolderId))                    
    else:
        return render_template("404.html")     

#module 'dao' has no attribute 'changePermission'
@app.route("/permission/<fileId>/<perms>")
def permission(fileId,perms):

    userId = RetrieveSessionDetails('userId')
    currentFolderId = RetrieveSessionDetails("currentFolderId")
    isPermissionChanged = BusinessLayer.changePermission(userId,fileId,perms,currentFolderId)

    if isPermissionChanged == False :
            return render_template("404.html") 

    folderId = RetrieveSessionDetails('currentFolderId')

    return redirect(url_for('index',folderId = folderId))            



@app.route('/deleteFolder/<folderId>/<foldername>')
def deleteFolder(folderId,foldername):
    userId = RetrieveSessionDetails('userId')
    currentFolderId = RetrieveSessionDetails('currentFolderId')
    path = BusinessLayer.getPathForFolder(userId,folderId)
    flag = BusinessLayer.RemoveExisitngFolder(userId,currentFolderId,folderId,foldername)

    if flag == 1:

        target = os.path.join(APP_STORAGE_PATH,path)

        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa target: ",target)

        shutil.rmtree(target)
        AddToSession('TotalSize',BusinessLayer.getTotalSize(userId))
   

    AddToSession('TotalSize',BusinessLayer.getTotalSize(userId))

    return redirect(url_for('index',folderId = currentFolderId))    


@app.route('/deleteFile/<fileId>/<filename>')
def deleteFile(fileId,filename):

    userId = RetrieveSessionDetails('userId')
    currentFolderId = RetrieveSessionDetails('currentFolderId')
    
    parentFolderId,parentfolderName = BusinessLayer.getParentFolderForFile(fileId,userId)
    print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk: ",parentFolderId)
    print("llllllllllllllllllllllllllllllllllllllllll: ",parentfolderName)

    flag = BusinessLayer.RemoveExisitngFile(userId,currentFolderId,fileId,filename)    

    if flag == True:
        
        try:
            path = BusinessLayer.getPathForFolder(userId,parentFolderId)
            target = os.path.join(APP_STORAGE_PATH,path)
            destination = "/".join([target, filename])
            os.remove(destination)
            AddToSession('TotalSize',BusinessLayer.getTotalSize(userId))

        except OSError:
            pass    
            
    return redirect(url_for('index',folderId = currentFolderId))

@app.route('/allfiles')
def allfiles():

    userId = RetrieveSessionDetails('userId')

    UserData = BusinessLayer.getAllFiles(userId)

    userclassInstance = UserClass()
    userclassInstance.setUserDetails(RetrieveSessionDetails('userId'),RetrieveSessionDetails('userName'),"passwd","name","email","phone")
    userclassInstance.setCurrentFolderId('0')
    userclassInstance.setCurrentFolderName("All files")
    userclassInstance.setHomeFolderId(RetrieveSessionDetails('homeFolderId'))

    UserData['UserDetails'] = userclassInstance
    UserData["sourceParameter"]="NotsearchIndex"
    UserData["AllFilesource"]="AllFilesource" 
    return render_template('index.html',**UserData)


@app.route('/open/<fileId>/<fileName>')
def openfile(fileId,fileName):

    userId = RetrieveSessionDetails('userId')

    parentFolderId,parentfolderName = BusinessLayer.getParentFolderForFile(fileId,userId)

    print("///////////////////////////////////////",parentFolderId,parentfolderName)    

    path = BusinessLayer.getPathForFolder(userId,parentFolderId)
    target = os.path.join(APP_STORAGE_PATH,path)       


    mime = MimeTypes()
    url = urllib.request.pathname2url(target)
    mime_type = mime.guess_type(url)
    print (mime_type)

    return send_from_directory(directory = target,filename = fileName,mimetype = mime_type[0])


@app.route('/copyCurrentPath',methods=["POST"])
def copyCurrentPath():
    print("----Inside copyCurrentPath ----")
    currentFolderId = RetrieveSessionDetails('currentFolderId')
    AddToSession('newParentFolderId',currentFolderId)
    return redirect(url_for('index',folderId = currentFolderId))


@app.route('/moveFile/<fileId>/<fileName>')
def moveFile(fileId, fileName):
    print("File id to move is: ", fileId, " and filename to move is: ", fileName)
    currentFolderId = RetrieveSessionDetails('currentFolderId')
    userId = RetrieveSessionDetails('userId')
    if 'newParentFolderId' in session:
        newParentFolderId = session['newParentFolderId']
        if BusinessLayer.CheckFilePresent(fileName, newParentFolderId, userId) == True:
            print("File cannot be moved at destination as a file with same name already present at destination....")
            session.pop('newParentFolderId', None)
            return redirect(url_for('index',folderId = currentFolderId))


        if BusinessLayer.setNewParentFolderForFile(fileId, userId, newParentFolderId) == False:
            print("---Unable to update new Parent folder of file in DB")
            session.pop('newParentFolderId', None)
            return redirect(url_for('index',folderId = currentFolderId))

        srcPath = APP_STORAGE_PATH
        srcPath += BusinessLayer.getPathForFolder(userId, currentFolderId)
        srcPath += fileName
        print("-------File src path is: ", srcPath)
        destPath = APP_STORAGE_PATH
        destPath += BusinessLayer.getPathForFolder(userId, newParentFolderId)
        destPath += fileName
        print("------Destination path is: ", destPath)
        try:
            os.rename(srcPath, destPath)
            session.pop('newParentFolderId', None)
            print("----OH YEAH!! File successfully moved----")
        except OSError:
            print("-------OH NO!!! Unable to move file---------")    
    else:
        print("Key not present in session")
        
    return redirect(url_for('index',folderId = currentFolderId))

@app.errorhandler(Exception)
def exception_handler(error):
    return render_template('404.html')

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

