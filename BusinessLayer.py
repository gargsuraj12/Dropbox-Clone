#!/usr/bin/python3

import ClassStructure as classObject
import dao as dataaccessobject
import model
import sqlalchemy

class BusinessLayer:
	
	def __init__(self):
		self.dbObject = dataaccessobject

	#sqlite://///home/nitish/IIITH/Semester1/Scripting/Project-DropBox/scripting_project-master/dropbox.db	

	#If User Valid 
	# return Dictionary : 
	# 	Key		Value
	#	userDetails	UserObject with details
	#	FolderDetails	User listofFolderDetails
	#	FileDetails	User listofFileDetails
	#	If user Not Valid 
	#	InvalidLogin	UserObject with details
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
				userclassInstance.currentFolderId=item.pFolderId
			FolderDetails = classObject.FolderClass()
			FolderDetails.setFolderDetails(item.folderId,item.folderName,item.uId,item.pFolderId)
			listofFolderDetails.append(FolderDetails)		
		
		#print(listofFolderDetails[0].foldername)		
		
		UserData["UserDetails"]=userclassInstance
		UserData["FolderDetails"]=listofFolderDetails
		UserData["FileDetails"]=listofFileDetails
		
		#print(UserData)			

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
	# 	Key		Value
	#	userDetails	UserObject with details
	#	FolderDetails	User listofFolderDetails
	#	FileDetails	User listofFileDetails
	#If user is already registered 
	#	Key			Value
	#	UserAlreadyExist	New User Already Exist UserObject with details
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
				if item.folderName != None and item.folderName == userName+'_home':
					UserClass.currentFolderId=item.pFolderId
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
	# 	Key		Value
	#	userDetails	UserObject with details
	#	FolderDetails	User listofFolderDetails
	#	FileDetails	User listofFileDetails
	#If user is already registered 
	#	Key			Value
	#	UserAlreadyExist	New User Already Exist UserObject with details
	def getFolderContents(self,userid,CurrentFolderId):
		#print(userid,CurrentFolderId)
		#print('BakWas')
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
		
		UserData["UserDetails"]=classObject.UserClass()
		UserData["FolderDetails"]=listofFolderDetails
		UserData["FileDetails"]=listofFileDetails
		print(UserData)			
		return UserData	

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
		
		UserData["FileDetails"]=listofFileDetails			
		return UserData	

	#Returns Full Qualified Path For the File 
	#def getPathForFile(self,User,CurrentFolder):
	def getPathForFile(self,userid,currentFolderId):
		fullQualifiedPath = self.dbObject.getPathForFile(currentFolderId)			
		return fullQualifiedPath	

	#Create A New Folder
	#Output:	
	#If Folder is Successfully Created 
	# return Dictionary : 
	# 	Key		Value
	#	userDetails	UserObject with details
	#	FolderDetails	User listofFolderDetails
	#	FileDetails	User listofFileDetails
	#If Folder is not able to create 
	#	Key			Value
	#	Error	Problem In Creating A Folder
	def createfolder(self,userId,currentFolderId,foldername):
		UFiles = self.dbObject.insertFolder(foldername,userId,currentFolderId)
		UserData = {} 
		SuccessCreation=-1
		for item in UFiles: 
			if item.folderId > 0:
				SuccessCreation = 0
				UserData = getFolderContents(userId,currentFolderId)
				return UserData
		if SuccessCreation != 0:
			UserData["Error"]="Problem In Creating A Folder"
	
	#Changes the Permission Details for Particular FileId  
	#Output:	
	#If Folder is Successfully Created 
	# return Dictionary : 
	# 	Key		Value
	#	userDetails	UserObject with details
	#	FolderDetails	User listofFolderDetails
	#	FileDetails	User listofFileDetails
	#If Folder is not able to create 
	#	Key			Value
	#	Error	Problem In Updating Permission Details
	def changePermission(self,userId,fileId,perms,currentFolderId):
		#Not IN DB 
		UFiles = self.dbObject.changePermission(userId,fileId,perms)
		UserData = {} 
		SuccessUpdation=-1
		for item in UFiles: 
			if item.folderId > 0:
				SuccessUpdation = 0
				UserData = getFolderContents(userId,currentFolderId)
				return UserData
		if SuccessUpdation != 0:
			UserData["Error"]="Problem In Updating Right Details"		

	#Obtain the Parent Folder ID for the userid and fileid
	def getParentFolderId(self,userId,fileId):
		#Not IN DB
		parentFolderId = self.dbObject.getParentFolderId(userId,fileId)
		return parentFolderId

	#Output:	
	#If Folder is Successfully Created 
	# return Dictionary : 
	# 	Key		Value
	#	userDetails	UserObject with details
	#	FileDetails	User listofFileDetails
	#If Folder is not able to create 
	#	Key			Value
	#	Error	Problem In Updating Permission Details
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
	def getHomeFolderId(userid):
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

	def makeUserInfo(self,UserClass):				
		userid=UserClass.userid
		userName = UserClass.userName
		name = UserClass.name
		passwd = UserClass.passwd
		email=UserClass.email
		phone=UserClass.phone
		#address=UserClass.address
		return userid,userName,name,passwd,email,phone

	#Un-Used				
	#Remove An Existing File Entry For Every Action of Delete
	#0 : If the File Id is Scussefully Removed From the DataBase
	#-1 : In Case of Other Scenarios  
	def RemoveExisitngFile(self,File,User):
		successfullyRemoved=-1
		listFileDetails,successReturn = GetFileMetaData(self,File,User)
		#Shows File With Same name Does Not Exist for the user		
		if successReturn == 0:
			fileid,filename,filepermission,size,owner,parentFolderId=self.makeFileInfo(File)
			userid,name,passwd,email,phone,address = self.makeUserInfo(User)
			successfullyRemoved = self.dbObject.deleteFile(fileid,userid)
		return successfullyRemoved		
	
	#Un-Used
	#Remove An Existing Folder Entry For Every Action of Delete
	#0 : If the Folder Id is Scussefully Removed From the DataBase
	#-1 : In Case of Other Scenarios  
	def RemoveExisitngFolder(self,File,User):
		successfullyRemoved=-1
		listFileDetails,successReturn = GetFileMetaData(self,File,User)
		#Shows File With Same name Does Not Exist for the user		
		if successReturn == 0:
			folderid,filename,folderpermission,size,owner,parentFolderId=self.makeFolderInfo(File)
			userid,name,passwd,email,phone,address = self.makeUserInfo(User)
			successfullyRemoved = self.dbObject.deleteFolder(folderid,userid)
		return successfullyRemoved		
		
	

	#Helper Method 
	def makeFileInfo(self,File):				
		fileid=File.fileid
		filename=File.filename
		filepermission=File.filepermission
		size=File.size
		#with respect to DataBase Onwer is User Id who Own the file
		owner=File.owner
		parentFolderId=File.parentFolderId
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
		return folderid,filename,folderpermission,size,owner,parentFolderId

		

B = BusinessLayer()
#C = ClassStructure.Company('1','','','','')

#userDetail = B.ValidateUser('nitish11', 'pass3')
#if userDetail == None:
#	print(' User Not Validated ')
#else:
#	userDetails = userDetail["UserDetails"]
	#print(userDetails.userid,userDetails.userName,userDetails.passwd,userDetails.name,userDetails.email,userDetails.phone)

#value = B.isUserExist('user3')
#if value == False:
#	print(' User Does Not Exists in DataBAse ')
#if value == True:
#	print(' User Does Exists in DataBAse ')

#userObj = classObject.UserClass();
#userObj.setUserDetails('','user12', 'pass12', 'Malhotra12', 'paddi12@outlook.com', '9913968498');
#registeredUserdic = B.RegisterUser(userObj)
#print(registeredUserdic)
#print('Fetching User Details')
#UserDetails = registeredUserdic["UserDetails"]
#print(UserDetails.userId)


#if registeredUserId == -1:
#	print(' User Not regsitered in DataBAse ')
#if registeredUserId > 0 :
#	print(' User Regsitered in DataBAse ')

#print("Fecthing All Company Details")

#B.GetAllCompanyDetails()

#print("Fecthing Specific Company Details Based on ID")
#B.GetCompanyDetailsBasedOnID(C)

		
		
		
	



	
	
