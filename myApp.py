import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for   
from flask_bootstrap import Bootstrap
#from BusinessLayer import BusinessLayer as bl, UserDataAccess as uda
#from ClassStructure import UserClass as user, FileClass as file ,FolderClass as folder

import ClassStructure
import BusinessLayer

WORKING_DIRECTORY = ""

myApp=Flask(__name__)
bootstrap = Bootstrap(myApp)

blayer = BusinessLayer.BusinessLayer()
userobject = ClassStructure.UserClass('','','','','','')
fileobject = ClassStructure.FileClass('','','','','','')
folderobject = ClassStructure.FolderClass('','','','','')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@myApp.route('/')
def login():
	return render_template('login.html')


@myApp.route('/logout')
def logout():
    del fileobject
    del folderobject
    del userobject
    return redirect(url_for('/'))    

@myApp.route('/index')
@myApp.route('/index/<path>')
def index(path='home'):
    
    validpath = blayer.checkValidDirectoryPath(path)

    if validpath is False:
        return render_template(404.html)

    folderflag,folderobject = blayer.GetFolders(userobject,path)
    filesflag,fileobject = blayer.GetFiles(userobject,path)

	return render_template('index.html',foldersobject = folderobject,fileobject = fileobject
                        ,userobject = userobject)


@myApp.route('/opendirectory', methods=['post', 'get'])
@myApp.route('/opendirectory/<temp>', methods=['post', 'get'])
def opendirectory(temp):



	return render_template('index.html',foldersobject = folderobject,fileobject = fileobject
                        ,userobject = userobject)

@myApp.route('/search', methods=['post', 'get'])
def search():
	fileName = request.form.get('fileName')

	return render_template('index.html',foldersobject = folderobject,fileobject = fileobject
                        ,userobject = userobject)


@myApp.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, WORKING_DIRECTORY)
    
    # print target

    if not os.path.isdir(target):
            os.mkdir(target)

    # print request.files.getlist("file")

    for upload in request.files.getlist("file"):
    
        filename = upload.filename
        destination = "/".join([target, filename])
        upload.save(destination)
    return redirect(url_for('index'))


@app.route('/myfiles/<string:id>/<string:filename>')
def downloadFile(id, filename):
    print("Filename is: ", filename)
    path = APP_STORAGE_PATH
    path += filename
    print("Path to download is: ", path)
    try:
        return send_file(path, as_attachment=True)
    except Exception as e:
        print(e)
    return render_template('download.html', id=id)


@myApp.route("/createfolder",methods=["POST"])
def createfolder():
    return "folder created"


@myApp.route("/showallfiles")
def showallfiles():
    return "success"    

@myApp.route("/download/<filename>")
def download(filename):
    return "success"    

@myApp.route("/permission/<value>")
def permission(value):
    perms,filename = value.split('-')
    print perms," ",filename
    return "It works"

@myApp.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

if __name__=='__main__':
	myApp.run(debug=True)