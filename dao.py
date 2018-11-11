from model import User, File, Folder, db 

def insertUser(uname, passwd, name, email, phone, address):
    newUser = User(username=uname, passwd=passwd, name=name, email=email, phone=phone, address=address)
    db.session.add(newUser)
    db.session.commit()
    uId = newUser.uId
    newFolder = Folder(folderName='home', uId=uId, pFolderId=None)
    db.session.add(newFolder)
    db.session.commit()
    return newUser,newFolder

def updateUserDetails(uId, uname, passwd, name, email, phone, address):
    user = User.query.filter_by(uId=uId).first()
    user.username = uname
    user.passwd = passwd
    user.name = name
    user.email = email
    user.phone = phone
    user.address = address
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
#     print(pFolderId, uId)    
    files = File.query.filter_by(pFolderId=pFolderId, uId=uId).all()
    folders = Folder.query.filter_by(pFolderId=pFolderId, uId=uId).all()
#     print(files,folders)
    return files,folders          

def isFileExist(fName, pFolderId, uId):
    file = File.query.filter_by(fileName=fName, pFolderId=pFolderId, uId=uId).first()
#     print(file)    
    return file   


# Testing goes here
# insertFile('FILE1',1,526.99,1,1)
# print(listFilesForUser(1))    
# listContentUnderFolder(1,1)
# file = isFileExist('FILE1', 1, 1)
files = listAllPublicFilesByFilename('FILE2')
print(files)
# user = validateUser('nitish11', 'Pass3')
# user = isUserExist('chitta007')
# user = updateUserDetails(1, 'user1', 'pass1', 'Raj', 'paddi@outlook.com', '7387633123', 'Valsad')
# if  not user:
#     # print("Username or password incorrect..")
#     print("User is not updated")
# else:
#     print("User details updated..")        
