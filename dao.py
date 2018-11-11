from model import User, File, Folder, db 
from sqlalchemy import text

def insertUser(uname, passwd, name, email, phone):
    newUser = User(username=uname, passwd=passwd, name=name, email=email, phone=phone)
    db.session.add(newUser)
    db.session.commit()
    uId = newUser.uId
    newFolder = Folder(folderName=uname+'home', uId=uId, pFolderId=None)
    db.session.add(newFolder)
    db.session.commit()
    return newUser,newFolder

def updateUserDetails(uId, uname, passwd, name, email, phone):
    user = User.query.filter_by(uId=uId).first()
    user.username = uname
    user.passwd = passwd
    user.name = name
    user.email = email
    user.phone = phone
    db.session.commit()
    return user

def insertFile(fname, filePerm, size, uId, pFolderId):
    newFile = File(fileName=fname, filePerm=filePerm, size=size, uId=uId, pFolderId=pFolderId)
    db.session.add(newFile)
    db.session.commit()
    return newFile

def insertFolder(fname, uId, pFolderId):
    newFolder = Folder(folderName=fname, uId=uId, pFolderId=pFolderId)
    db.session.add(newFolder)
    db.session.commit()
    return newFolder

def validateUser(uname, password):
    user = User.query.filter_by(username=uname, passwd=password).first()
    return user

def isUserExist(uname):
    user = User.query.filter_by(username=uname).first()
    return user

def listFilesForUser(uId):
    user = User.query.filter_by(uId=uId).all()
    files = user.files
    return files

def listAllPublicFilesByFilename(fName):
    files = File.query.filter_by(fileName=fName, filePerm=0).all()
    return files

def listContentUnderFolder(pFolderId, uId):
    files = File.query.filter_by(pFolderId=pFolderId, uId=uId).all()
    folders = Folder.query.filter_by(pFolderId=pFolderId, uId=uId).all()
    return files,folders

def isFileExist(fName, pFolderId, uId):
    file = File.query.filter_by(fileName=fName, pFolderId=pFolderId, uId=uId).first  
    return file   

def getPathForFile(fileId):
    sql = text("with cte(FOLDERID, FULLPATH, RECLEVEL) as (select C.FOLDERID, cast(C.FOLDERNAME as TEXT) as FULLPATH, 0 as RECLEVEL from FOLDER C where C.P_FOLDERID IS NULL UNION ALL select C1.FOLDERID, CAST((C.FULLPATH || \'/\' || C1.FOLDERNAME) AS TEXT) as FULLPATH, C.RECLEVEL + 1 as RECLEVEL from FOLDER C1 inner join cte C on C1.P_FOLDERID = C.FOLDERID) select FULLPATH from cte where FOLDERID in (select P_FOLDERID from file where FILEID=:fId)")
    result = db.engine.execute(sql, fId=fileId).first()
    path = str(result[0])
    path += '/'
    return path

def getParentFolderForFile(fileId, uId):
    sql = text("select FOLDERID, FOLDERNAME from FOLDER where FOLDERID in (select P_FOLDERID from file where FILEID= :fId and UID = :userId)")
    result = db.engine.execute(sql, fId=fileId, userId=uId).first()
    return (result[0],result[1])

def getParentFolderForFolder(folderId, uId):
    sql = text("SELECT FOLDERID, FOLDERNAME FROM FOLDER WHERE FOLDERID IN (SELECT P_FOLDERID FROM FOLDER WHERE FOLDERID= :fId AND UID= :userId)")
    result = db.engine.execute(sql, fId=folderId, userId=uId).first()
    return (result[0],result[1])

def updateFilePerm(fileId, uId, newPerm):
    file = File.query.filter_by(fileId = fileId, uId = uId).first()
    file.filePerm = newPerm
    db.session.commit()

def getHomeFolderForUser(uId):
    folder = Folder.query.filter_by(pFolderId=None, uId=uId).first()
    return folder



# Testing goes here
# insertFile('FILE1',1,526.99,1,1)
# print(listFilesForUser(1))    
# listContentUnderFolder(1,1)
# file = isFileExist('FILE1', 1, 1)
# files = listAllPublicFilesByFilename("FILE2")
# print(files)
# user = validateUser('nitish11', 'Pass3')
# user = isUserExist('chitta007')
# user = updateUserDetails(1, 'user1', 'pass1', 'Raj', 'paddi@outlook.com', '7387633123', 'Valsad')
# if  not user:
#     # print("Username or password incorrect..")
#     print("User is not updated")
# else:
#     print("User details updated..")        

# updateFilePerm(3, 1, 1)
# folder = getHomeFolderForUser(2)
# print(folder.folderName)