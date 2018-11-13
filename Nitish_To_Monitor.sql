------------------------------------------------- For Suraj --------------------------------------------

#	DataBase Methods Needed :   
--Validation
#For UserName Give Details as an object if user is prent otherwise NOne
#listUserDetails = self.dbObject.GetUserDetails(UserName) --Completed

#For User Registratio Input Provided Details
#return User ID as an Output if Inserted Successfully in DB
#registeredUserId = self.dbObject.RegisterUser(name,passwd,email,phone,address) --Completed

#For User Input Provided Details
#return User ID as an Output if Inserted Successfully
#registeredUserId = self.dbObject.UpdateUserDetails(userid,name,passwd,email,phone,address) --Completed

#Get All the Contents of the Logged in User for requested Directory --Completed
#fileList,folderList = self.dbObject.GetContentUnderFolder(userid, CurrentFolder)

#For File it should Give Details with provided filename if existed in Current Folder 
#else empty list is expected -- Completed
#FileObject = self.dbObject.GetFileDetails(filename, parentFolderId, userid)

#Insert New Details of File
#returns newfileId which is inserted  
#self.dbObject.insertNewFileDetails(filename,filepermission,size,parentFolderName,userid) --Completed
--self.dbObject.changeFilePermission(fileid,fileNewpermission,userid) 
--Updating folder permission is not in scope

--List all files for a user completed
--List all public files matching the supplied filename -- Completed 

#Delete File wrt to fileid for specified User
#if file not existed or not deleted then -1 should be returned 
--#successfullyRemoved = self.dbObject.deleteFile(fileid,userid) -- Not in Scope 


#Delete Folder wrt to folderid for specified User
#if folder not existed or not deleted then -1 should be returned 
--#successfullyRemoved = self.dbObject.deleteFolder(folderid,userid) -- Not in Scope

------------------------------------------------- End For Suraj --------------------------------------------

------------------------------------------------- Start For Prakash --------------------------------------------

getPathForFolder and getPathForFile not working

------------------------------------------------- End For Prakash --------------------------------------------

