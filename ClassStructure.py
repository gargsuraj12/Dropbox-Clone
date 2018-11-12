#!/usr/bin/python3

class UserClass:
	def __init__(self):
	#def __init__(self,userid,userName,passwd,name,email,phone):
		self.userid=None
		self.userName = ''
		self.passwd=''	
		self.name=''
		self.email=''
		self.phone=''
		#self.address=address
		self.currentFolderId=None
		self.currentFolderName=None
		self.HomeFolderId=None
		

	def setUserDetails(self,userid,userName,passwd,name,email,phone):
		self.userid=userid
		self.userName = userName
		self.passwd=passwd	
		self.name=name
		self.email=email
		self.phone=phone

	def setCurrentFolderId(self,currentFolderId):
		self.currentFolderId = currentFolderId	

	def setCurrentFolderName(self,currentFolderName):
		self.currentFolderName=currentFolderName

	def setHomeFolderId(self,HomeFolderId):
		self.HomeFolderId=HomeFolderId

	
class FileClass:
	def __init__(self):
	#def __init__(self,fileid,filename,filepermission,size,owner,parentFolderId):
		self.fileid=None
		self.filename=''
		self.filepermission=''
		self.size=''
		#with respect to DataBase Onwer is User Id who Own the file
		self.owner=''
		self.parentFolderId=None	

	def setFileDetails(self,fileid,filename,filepermission,size,owner,parentFolderId):
		self.fileid=fileid
		self.filename=filename
		self.filepermission=filepermission
		self.size=size
		#with respect to DataBase Onwer is User Id who Own the file
		self.owner=owner
		self.parentFolderId=parentFolderId	


class FolderClass:
	
	def __init__(self):
	#def __init__(self,folderid,foldername,folderpermission,uId,parentFolderId):
		self.folderid=None
		self.foldername=''
		self.folderpermission=''
		#with respect to DataBase Onwer is User Id who Own the file
		self.uId=None
		self.parentFolderId=None

	def setFolderDetails(self,folderid,foldername,uId,parentFolderId):
		self.folderid=folderid
		self.foldername=foldername
		#self.folderpermission=folderpermission
		#with respect to DataBase Onwer is User Id who Own the file
		self.uId=uId
		self.parentFolderId=parentFolderId



#Dummy
class Company:
	def __init__(self,ID,name,age,salary,address):
		self.ID=ID
		self.age=age
		self.name=name
		self.salary=salary
		self.address=address



	
	