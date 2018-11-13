from model import User, File, Folder, db 
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy import event, and_, update
from sqlalchemy.exc import SQLAlchemyError

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def insertUser(uname, passwd, name, email, phone):
    try:    
        newUser = User(username=uname, passwd=passwd, name=name, email=email,   phone=phone)
        db.session.add(newUser)
        db.session.commit()
        uId = newUser.uId
        homeFolder = uname+"_home"
        newFolder = Folder(folderName=homeFolder, uId=uId, pFolderId=None)
        db.session.add(newFolder)
        db.session.commit()
        folders = Folder.query.filter_by(folderId=newFolder.folderId).all()
        return newUser,folders
    except SQLAlchemyError as e:
        print(e)
        return False

def updateUserDetails(uId, uname, passwd, name, email, phone):
    try:    
        user = User.query.filter_by(uId=uId).first()
        user.username = uname
        user.passwd = passwd
        user.name = name
        user.email = email
        user.phone = phone
        db.session.commit()
        return user
    except SQLAlchemyError as e:
        print(e)
        return False

def insertFile(fname, filePerm, size, uId, pFolderId):
    try:    
        newFile = File(fileName=fname, filePerm=filePerm, size=size, uId=uId,   pFolderId=pFolderId)
        db.session.add(newFile)
        db.session.commit()
        return newFile
    except SQLAlchemyError as e:
        print(e)
        return False


def insertFolder(fname, uId, pFolderId):
    try:    
        newFolder = Folder(folderName=fname, uId=uId, pFolderId=pFolderId)
        db.session.add(newFolder)
        db.session.commit()
        return newFolder
    except SQLAlchemyError as e:
        print(e)
        return False


def validateUser(uname, password):
    user = User.query.filter_by(username=uname, passwd=password).first()
    return user

def isUserExist(uname):
    user = User.query.filter_by(username=uname).first()
    return user

def listFilesForUser(uId):
    files = File.query.filter_by(uId=uId).all()
    return files

def listAllPublicFilesByFilename(fName):
    files = File.query.filter(File.fileName.like("%"+fName+"%"), File.filePerm==0).all()
    return files

def listContentUnderFolder(pFolderId, uId):
    files = File.query.filter_by(pFolderId=pFolderId, uId=uId).all()
    folders = Folder.query.filter_by(pFolderId=pFolderId, uId=uId).all()
    return files,folders

def isFileExist(fName, pFolderId, uId):
    file = File.query.filter_by(fileName=fName, pFolderId=pFolderId, uId=uId).first()
    return file

def isFolderExist(fName, pFolderId, uId):
    folder = Folder.query.filter_by(folderName=fName, pFolderId=pFolderId, uId=uId).first()
    return folder

def getPathForFile(fileId):
    sql = text("with cte(FOLDERID, FULLPATH, RECLEVEL) as (select C.FOLDERID, cast(C.FOLDERNAME as TEXT) as FULLPATH, 0 as RECLEVEL from FOLDER C where C.P_FOLDERID IS NULL UNION ALL select C1.FOLDERID, CAST((C.FULLPATH || \'/\' || C1.FOLDERNAME) AS TEXT) as FULLPATH, C.RECLEVEL + 1 as RECLEVEL from FOLDER C1 inner join cte C on C1.P_FOLDERID = C.FOLDERID) select FULLPATH from cte where FOLDERID in (select P_FOLDERID from file where FILEID=:fId)")
    result = db.engine.execute(sql, fId=fileId).first()
    if result == None:
        return None
    path = str(result[0])
    path += '/'
    return path

def getPathForFolder(folderId):
    sql = text("with cte(FOLDERID, FULLPATH, RECLEVEL) as (select C.FOLDERID, cast(C.FOLDERNAME as TEXT) as FULLPATH, 0 as RECLEVEL from FOLDER C where C.P_FOLDERID IS NULL UNION ALL select C1.FOLDERID, CAST((C.FULLPATH || '/' || C1.FOLDERNAME) AS TEXT) as FULLPATH, C.RECLEVEL + 1 as RECLEVEL from FOLDER C1 inner join cte C on C1.P_FOLDERID = C.FOLDERID) select FULLPATH from cte where folderid =:fId")
    result = db.engine.execute(sql, fId=folderId).first()
    if result == None:
        return None
    path = str(result[0])
    path += '/'
    return path

def getParentFolderForFile(fileId, uId):
    #sql = text("select FOLDERID, FOLDERNAME from FOLDER where FOLDERID in (select P_FOLDERID from file where FILEID= :fId and UID = :userId)")
    sql = text("select FOLDERID, FOLDERNAME from FOLDER where FOLDERID in (select P_FOLDERID from file where FILEID= :fId)")
    result = db.engine.execute(sql, fId=fileId, userId=uId).first()
    if result == None:
        return None,None
    return (result[0],result[1])

def getParentFolderForFolder(folderId, uId):
    sql = text("SELECT FOLDERID, FOLDERNAME FROM FOLDER WHERE FOLDERID IN (SELECT P_FOLDERID FROM FOLDER WHERE FOLDERID= :fId AND UID= :userId)")
    result = db.engine.execute(sql, fId=folderId, userId=uId).first()
    if result == None:
        return None
    return (result[0],result[1])

def getFolderName(folderId,uId):
    sql = text("SELECT FOLDERID,FOLDERNAME FROM FOLDER WHERE FOLDERID = :fId AND UID= :userId")
    result = db.engine.execute(sql, fId=folderId, userId=uId).first()
    if result == None:
        return None
    return (result[0],result[1])    

def getFileName(fileId,uId):
    sql = text("SELECT FILEID,FILENAME FROM FILE WHERE FILEID = :fId AND UID= :userId")
    result = db.engine.execute(sql, fId=fileId, userId=uId).first()
    if result == None:
        return None
    return (result[0],result[1])    


def updateFilePerm(fileId, uId, newPerm):
    try:
        file = File.query.filter_by(fileId = fileId, uId = uId).first()
        file.filePerm = newPerm
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        print(e)
        return False

def getHomeFolderForUser(uId):
    folder = Folder.query.filter_by(pFolderId=None, uId=uId).first()
    return folder

def deleteFile(fileId, userId):
    try:
        result = File.query.filter_by(fileId=fileId, uId=userId).delete()
        db.session.commit()
        return result
    except SQLAlchemyError as e:
        print(e)
        return False

def deleteFolder(folderId, userId):
    try:    
        result = Folder.query.filter_by(folderId=folderId, uId=userId).delete()
        db.session.commit()
        return result
    except SQLAlchemyError as e:
        print(e)
        return 0

def getUserDetailsByUserId(userId):
    user = User.query.filter_by(uId=userId).first()
    return user

def getConsumedSpaceByUser(userId):
    sql = text("SELECT SUM(SIZE) FROM FILE WHERE UID=:uId")
    size = db.engine.execute(sql, uId=userId).first()
    if size[0] == None:
        return 0
    return size[0]

def updateParentFolderForFile(fileId, userId, newParentFolderId):
    try:
        file = File.query.filter_by(fileId = fileId, uId = userId).first()
        file.pFolderId = newParentFolderId
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        print(e)
        return False

# Testing goes here

# print(updateFilePerm(1,1,"0"))

# files = listAllPublicFilesByFilename("iNdEx")
# for file in files:
#     print(file.fileName)
# print(getConsumedSpaceByUser(3))
# files = listFilesForUser(1)
# for file in files:
#     print(file.fileName)

#user = getUserDetailsByUserId(1)
#print(user.files)
# print(getPathForFolder(6))
# print(getPathForFolder(4))
# updateUserDetails(2, "user2", "pass2", "Jha G", "pnj@outlook.com", "9876543210", 10)
# insertFile("file32",1, 102.45, 5, 4)
# print(deleteFolder(5))
# print(deleteFile(1))
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

# updateFilePerm(1, 1, 1)
# folder = getHomeFolderForUser(2)
# print(folder.folderName)
# validateUser("user1", "pass1")
# print(insertUser('testDummy','dummy123','NameDummy','dummy@dum.com','5555'))
# print(isFolderExist("dir1", 2, 3))