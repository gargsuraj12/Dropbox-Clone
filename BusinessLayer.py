#!/usr/bin/python3

import ClassStructure as classObject
import dao as dataaccessobject
import model
import sqlalchemy

class BusinessLayer:
    
    def __init__(self):
        self.dbObject = dataaccessobject

    #sqlite://///home/nitish/IIITH/Semester1/Scripting/Project-DropBox/scripting_project-master/dropbox.db  
    
    def getTotalSize(self,userid):
        return self.dbObject.getConsumedSpaceByUser(userid)
        

    #If User Valid 
    # return Dictionary : 
    #   Key     Value
    #   userDetails UserObject with details
    #   FolderDetails   User listofFolderDetails
    #   FileDetails User listofFileDetails
    #   If user Not Valid 
    #   InvalidLogin    UserObject with details
    def ValidateUser(self,userName,password):
        #print(self.dbObject.getPathForFile(3))
        user = self.dbObject.validateUser(userName,password)
        #print(user.uId,user.username,user.name,user.passwd,user.email,user.phone)
        #print(user.folders)
        UserData = {} 
        if user == None:
            UserData["InvalidLogin"]="Invalid Login Attempt"
            return UserData     
        userclassInstance = classObject.UserClass()
        userclassInstance.setUserDetails(user.uId,user.username,user.name,user.passwd,user.email,user.phone)
        
        listofFolderDetails = []
        listofFileDetails = []
        
        for item in user.folders: 
            if item.folderName != None and item.folderName ==  userName+'_home':
                #print('Inside name of User')
                userclassInstance.currentFolderId=item.folderId
                userclassInstance.setCurrentFolderName(item.folderName)
                userclassInstance.setHomeFolderId(item.folderId)
            FolderDetails = classObject.FolderClass()
            FolderDetails.setFolderDetails(item.folderId,item.folderName,item.uId,item.pFolderId)
            listofFolderDetails.append(FolderDetails)   
    
        for item in user.files:             
            FileDetails = classObject.FileClass()
            FileDetails.setFileDetails(item.fileId,item.fileName,item.filePerm,item.size,item.uId,item.pFolderId)
            listofFileDetails.append(FileDetails)           
        
        #print(listofFolderDetails[0].foldername)       
        
        UserData["UserDetails"]=userclassInstance
        UserData["FolderDetails"]=listofFolderDetails
        UserData["FileDetails"]=listofFileDetails
        
        print(UserData)         

        return UserData
        #All Details of File , Folder and user will  return UserData dictionary 
        

    def isUserExist(self,userName):
        user = self.dbObject.isUserExist(userName)
        #print(user)
        if not user:
            return False
        return True

    #PreRequisite : 
    #User Should Be Providing Input as a Name and Password  
    #Output:    
    #If User is Successfully Registered 
    # return Dictionary : 
    #   Key     Value
    #   userDetails UserObject with details
    #   FolderDetails   User listofFolderDetails
    #   FileDetails User listofFileDetails
    #If user is already registered 
    #   Key         Value
    #   UserAlreadyExist    New User Already Exist UserObject with details
    def RegisterUser(self,UserClass):
        #registeredUserId=-1
        #UserDetails=None
        FolderDetails=None
        UserData = {} 
        userid,userName,name,passwd,email,phone = self.makeUserInfo(UserClass)
        userExistence = self.isUserExist(name)  
        if userExistence == False:
            UserDetailsDB,FDDB = self.dbObject.insertUser(userName,name,passwd,email,phone)
            
            #UserDetails = classObject.UserClass()
            #UserDetails.setUserDetails(user.uId,user.username,user.name,user.passwd,user.email,user.phone)
            
            if UserDetailsDB.uId == None:
                UserData["UserAlreadyExist"]="User is Not Created"
                return 
            UserClass.userId = UserDetailsDB.uId
            
            #print(UserClass)
            #print(FolderDetails)
            
            listofFolderDetails = []
            listofFileDetails = []

            for item in FDDB:
                if item!=None and item.folderName != None and item.folderName == userName+'_home':
                    UserClass.currentFolderId=item.folderId
                    UserClass.setCurrentFolderName(item.folderName)
                    UserClass.setHomeFolderId(item.folderId)
                FolderDetails = classObject.FolderClass()
                FolderDetails.setFolderDetails(item.folderId,item.folderName,item.uId,item.pFolderId)
                listofFolderDetails.append(FolderDetails)       
                
            UserData["UserDetails"]=UserClass
            UserData["FolderDetails"]=listofFolderDetails
            UserData["FileDetails"]=listofFileDetails           
        return UserData 

    #Output:
    #UserDetails - Return On Successfully Updated
    #-1- Return On Not Updated Successfully
    def UpdateDetailsOfUser(self,UserClass):
        userid,userName,name,passwd,email,phone = self.makeUserInfo(UserClass)
        userExistence = self.isUserExist(name)  
        if userExistence == False:
            UserDetails = self.dbObject.updateUserDetails(userid, userName, passwd, name, email, phone)
            return UserDetails
        return -1

    #Get All the Directory Content For the Current Folder of the User
    #Output:    
    #If User is Successfully Registered 
    # return Dictionary : 
    #   Key     Value
    #   userDetails UserObject with details
    #   FolderDetails   User listofFolderDetails
    #   FileDetails User listofFileDetails
    #If user is already registered 
    #   Key         Value
    #   UserAlreadyExist    New User Already Exist UserObject with details
    def getFolderContents(self,userid,CurrentFolderId):
        FolderDetails=None
        UserData = {} 
        UFiles,UFolders = self.dbObject.listContentUnderFolder(CurrentFolderId,userid)
        listofFolderDetails = []
        listofFileDetails = []

        for item in UFolders: 
            FolderDetails = classObject.FolderClass()
            FolderDetails.setFolderDetails(item.folderId,item.folderName,item.uId,item.pFolderId)
            listofFolderDetails.append(FolderDetails)

        #fileid,filename,filepermission,size,owner,parentFolderId
        for item in UFiles: 
            FileDetails = classObject.FileClass()
            FileDetails.setFileDetails(item.fileId,item.fileName,item.filePerm,item.size,item.uId,item.pFolderId)
            listofFileDetails.append(FileDetails)       
        
        user = self.dbObject.getUserDetailsByUserId(userid)
        userclassInstance = classObject.UserClass()
        userclassInstance.setUserDetails(user.uId,user.username,user.name,user.passwd,user.email,user.phone)
        userclassInstance.currentFolderId = CurrentFolderId

        UserData["UserDetails"]=userclassInstance
        UserData["FolderDetails"]=listofFolderDetails
        UserData["FileDetails"]=listofFileDetails
        print(userclassInstance.currentFolderId)            
        return UserData 

        def getUserDetailsByUserId(self,userid):
            user = self.dbObject.getUserDetailsByUserId(userid)
            userclassInstance = classObject.UserClass()
            userclassInstance.setUserDetails(user.uId,user.username,user.name,user.passwd,user.email,user.phone)
            return userclassInstance

    #Used For Searching the File 
    #List Only the File Details 
    def searchFile(self,userid,FileName):
        FolderDetails=None
        UserData = {} 
        UFiles = self.dbObject.listAllPublicFilesByFilename(FileName)
        listofFileDetails = []

        for item in UFiles: 
            FileDetails = classObject.FileClass()
            FileDetails.setFileDetails(item.fileId,item.fileName,item.filePerm,item.size,item.uId,item.pFolderId)
            listofFileDetails.append(FileDetails)       
        
        if len(listofFileDetails) == 0:
            return None
        else:    
            UserData["FileDetails"]=listofFileDetails
            UserData["sourceParameter"]="searchSource"           
            return UserData 


    #Returns Full Qualified Path For the File 
    #def getPathForFile(self,User,CurrentFolder):
    def getPathForFile(self,userid,fileId):
        fullQualifiedPath = self.dbObject.getPathForFile(fileId)           
        return fullQualifiedPath

    #Returns Full Qualified Path For the File 
    #def getPathForFolder(self,User,CurrentFolder):
    def getPathForFolder(self,userid,currentFolderId):
        fullQualifiedPath = self.dbObject.getPathForFolder(currentFolderId)         
        return fullQualifiedPath

    #Create A New File
    #Output:    
    #If File is Successfully Created 
    # return Created File Class Object
    #If Folder is not able to create return None
    def createfolder(self,userId,currentFolderId,foldername):
        successReturn = self.dbObject.isFolderExist(foldername,currentFolderId,userId)      
        if successReturn != None:
            return None 
        item = self.dbObject.insertFolder(foldername,userId,currentFolderId)
        if item == None:
            return None             
        FolderDetails = classObject.FolderClass()
        FolderDetails.setFolderDetails(item.folderId,item.folderName,item.uId,item.pFolderId)
        return FolderDetails
            
    #Create A New File
    #Output:    
    #If File is Successfully Created 
    # return Created File Class Object
    #If Folder is not able to create return None
    def createFile(self,FileClass,userId,currentFolderId):
        successReturn = self.dbObject.isFileExist(FileClass.filename,currentFolderId,userId)  
        print('Check1')      
        if successReturn != None:
            return None         
        print('Check2')      
        
        item = self.dbObject.insertFile(FileClass.filename,FileClass.filepermission,
                                        FileClass.size,userId,currentFolderId)
        if item == None:
            return None     
        print('Check3')      
        FileDetails = classObject.FileClass()
        FileDetails.setFileDetails(item.fileId,item.fileName,item.filePerm,item.size,item.uId,
        item.pFolderId)
        return FileDetails
    
    #Changes the Permission Details for Particular FileId  
    #Output:    
    #If Folder is Successfully Created 
    # return Dictionary : 
    #   Key     Value
    #   userDetails UserObject with details
    #   FolderDetails   User listofFolderDetails
    #   FileDetails User listofFileDetails
    #If Folder is not able to create 
    #   Key         Value
    #   Error   Problem In Updating Permission Details
    def changePermission(self,userId,fileId,perms,currentFolderId):
        isPublic=None
        if perms=='public':
            isPublic = 0
        if perms=='private':
            isPublic = 1
        #Not IN DB 
        #0 -> PUBLIC
        #1 -> PRIVATE

        print("88888888888888888888888888",userId,fileId,perms,currentFolderId)

        UFiles = self.dbObject.updateFilePerm(fileId,userId,isPublic)

        #print(UFiles)

        if UFiles == None:
            return False
        else:
            return True

    #Obtain the Parent Folder ID for the userid and fileid
    def getParentFolderId(self,uId,fileId):
        parentFolderId = self.dbObject.getParentFolderId(uId,fileId)
        return parentFolderId

    def getParentFolderForFile(self,uId,fileId):
        fileId,folderName = self.dbObject.getParentFolderForFile(uId,fileId)
        if fileId == None:
            return None,None
        return fileId,folderName

    def getParentFolderForFolder(self,uId,folderId):
        folderId,folderName = self.dbObject.getParentFolderForFolder(folderId,uId)
        if folderId == None:
            return None,None
        return folderId,folderName

    def getFolderName(self,uId,folderId):
        folderId,folderName = self.dbObject.getFolderName(folderId,uId)
        if folderId == None:
            return None,None
        return folderId,folderName     

    def getFileName(self,uId,folderId):
        fileId,fileName = self.dbObject.getFileName(fileId,uId)
        if fileId == None:
            return None,None
        return fileId,fileName

    #Output:    
    #If Folder is Successfully Created 
    # return Dictionary : 
    #   Key     Value
    #   userDetails UserObject with details
    #   FileDetails User listofFileDetails
    #If Folder is not able to create 
    #   Key         Value
    #   Error   Problem In Updating Permission Details
    def getAllFiles(self,userId):
        UserData = {}
        listofFileDetails = []
        FileDetailsDB = self.dbObject.listFilesForUser(userId)
                
        for item in FileDetailsDB: 
            FileDetails = classObject.FileClass()
            FileDetails.setFileDetails(item.fileId,item.fileName,item.filePerm,item.size,item.uId,item.pFolderId)
            listofFileDetails.append(FileDetails)   

        UserData["FileDetails"] = listofFileDetails;
        return UserData

    #Get user Id's home Folder Details 
    def getHomeFolderId(self,userid):
        item = self.dbObject.getHomeFolderForUser(userid)
        FolderDetails = classObject.FolderClass()
        FolderDetails.setFolderDetails(item.folderId,item.folderName,item.uId,item.pFolderId)
        return FolderDetails
        

    #Helper Method 
    def ParseUserDBClassToUserClass(self,UserClass,user):
        userclassInstance.userid = user.uId
        userclassInstance.name = user.name
        userclassInstance.passwd=user.passwd
        userclassInstance.email=user.email
        userclassInstance.phone=user.phone
        userclassInstance.address=user.address
        return userclassInstance

    #Helper Method 
    def ParseFolderDBToFolder(self,FolderClass,Folder):
        FolderClass.folderid=Folder.folderId
        FolderClass.foldername=Folder.folderName
        #self.folderpermission=folderpermission
        #with respect to DataBase Onwer is User Id who Own the file
        FolderClass.uId=Folder.uId
        FolderClass.parentFolderId=Folder.pFolderId
        return FolderClass

    #Helper Method 
    def makeUserInfo(self,UserClass):               
        userid=UserClass.userid
        userName = UserClass.userName
        name = UserClass.name
        passwd = UserClass.passwd
        email=UserClass.email
        phone=UserClass.phone
        #address=UserClass.address
        return userid,userName,name,passwd,email,phone
    
    #Check Whther the File is Present or Not 
    def CheckFilePresent(self,filename,parentFolderId,userid):
        successReturn = self.dbObject.isFileExist(filename,parentFolderId,userid)     
        if successReturn == None:
            return False 
        return True

    #Check Whther the Folder is Present or Not 
    def CheckFolderPresent(self,foldername,parentFolderId,userid):
        successReturn = self.dbObject.isFolderExist(foldername,parentFolderId,userid)     
        if successReturn == None:
            return False 
        return True 
        
    #Remove An Existing File Entry For Every Action of Delete
    #0 : If the File Id is Scussefully Removed From the DataBase
    #-1 : In Case of Other Scenarios  
    def RemoveExisitngFile(self,userid,parentFolderId,fileid,filename):
        successfullyRemoved=-1
        successReturn = self.CheckFilePresent(filename,parentFolderId,userid)
        #Shows File With Same name Does Not Exist for the user      
        if successReturn == True:
            successfullyRemoved = self.dbObject.deleteFile(fileid,userid)
        return successfullyRemoved      

    #Remove An Existing Folder Entry For Every Action of Delete
    #0 : If the Folder Id is Scussefully Removed From the DataBase
    #-1 : In Case of Other Scenarios  
    def RemoveExisitngFolder(self,userid,parentFolderId,folderId,foldername):
        successfullyRemoved=-1
        successReturn = self.CheckFolderPresent(foldername,parentFolderId,userid)
        #Shows File With Same name Does Not Exist for the user      
        if successReturn == True:
            successfullyRemoved = self.dbObject.deleteFolder(folderId,userid)
        return successfullyRemoved  

    #Helper Method 
    def makeFileInfo(self,FileClass):               
        fileid=FileClass.fileid
        filename=FileClass.filename
        filepermission=FileClass.filepermission
        size=FileClass.size
        #with respect to DataBase Onwer is User Id who Own the file
        owner=FileClass.owner
        parentFolderId=FileClass.parentFolderId
        return fileid,filename,filepermission,size,owner,parentFolderId

    #Helper Method 
    def makeFolderInfo(self,Folder):                
        folderid=Folder.folderid
        foldername=Folder.foldername
        folderpermission=Folder.folderpermission
        size=Folder.size
        #with respect to DataBase Onwer is User Id who Own the file
        owner=Folder.owner
        parentFolderId=Folder.parentFolderId
        return folderid,foldername,folderpermission,size,owner,parentFolderId


    #updateParentFolderForFile(fileId,userId,newParentFolderId)
    def setNewParentFolderForFile(self,fileId,userId,newParentFolderId):
        return self.dbObject.updateParentFolderForFile(fileId,userId,newParentFolderId)

B = BusinessLayer()
#print(B.updateParentFolderForFile(60,1,1))
#B.getParentFolderId(1,71)
#// File Id // User ID 
#print(B.getParentFolderForFile(80,4))
# give Folder Id 
#// File Id // User ID 
#print(B.getFolderName(1,16))
#// User ID // File Id //  
#print(B.getParentFolderForFolder(1,16))

#B.RemoveExisitngFolder(8,1,6,"testFolder")
#B.RemoveExisitngFile(23,2,7,"a.out")
# print(B.searchFile(1,"report.pdf"))
#C = ClassStructure.Company('1','','','','')

#userDetailaaaa = B.ValidateUser('nitish11', 'pass3')
#if userDetailaaaa == None:
#   print(' User Not Validated ')
#else:
#   userDetailsa = userDetailaaaa["UserDetails"]
#print(userDetails.currentFolderId,userDetails.HomeFolderId,userDetails.currentFolderName,userDetails.userid,
#userDetails.userName,userDetails.passwd,userDetails.name,userDetails.email,userDetails.phone)

#value = B.isUserExist('user3')
#if value == False:
#   print(' User Does Not Exists in DataBAse ')
#if value == True:
#   print(' User Does Exists in DataBAse ')

#userObj = classObject.UserClass();
#userObj.setUserDetails('','user12', 'pass12', 'Malhotra12', 'paddi12@outlook.com', '9913968498');
#registeredUserdic = B.RegisterUser(userObj)
#print(registeredUserdic)
#print('Fetching User Details')
#UserDetails = registeredUserdic["UserDetails"]
#print(UserDetails.userId)


#if registeredUserId == -1:
#   print(' User Not regsitered in DataBAse ')
#if registeredUserId > 0 :
#   print(' User Regsitered in DataBAse ')

#print("Fecthing All Company Details")

#B.GetAllCompanyDetails()

#print("Fecthing Specific Company Details Based on ID")
#B.GetCompanyDetailsBasedOnID(C)

        
        
        
    



    
    