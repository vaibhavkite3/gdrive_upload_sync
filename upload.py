#!/usr/bin/python

#importing PyDrive libraries
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#other libraries
import subprocess
import datetime
import socket
import time
import os
from os import chdir, listdir, stat, path
import sys

#authenticating the gdrive
#this will read settings.yaml and save authentication token to credentials.json
#settings still require client_secrets.json downloaded from API services
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

#Source folder name where backup files are kept
source_path_file="./backup_path.txt"
file_data = ""
src_folder_name = ""
target_upload_dir = ""
src_file_name = ""

# Check the file
if path.exists(source_path_file) == True:
  file_data = open(source_path_file, 'r').readline().replace("\n", "")
  if file_data == "":
    print('Source file is Empty OR Incorrect')
    sys.exit(1)

#Print error if source file doesn't exist or empty
else:
  print('Source file is missing OR Incorrect')
  sys.exit(1)


if os.path.isdir(file_data) == True :
    src_folder_name = os.path.dirname(file_data)
    target_upload_dir = os.path.dirname(file_data).split('/')[-1]
    print("We found source folder : " + src_folder_name + " & its Name : " + target_upload_dir + " of which all files will be uploaded")
else:
    src_folder_name = os.path.dirname(file_data)
    src_file_name = os.path.basename(file_data)
    target_upload_dir = os.path.dirname(file_data).split('/')[-1]
    print("We found a file to upload : " + src_file_name + " from folder : " + target_upload_dir + " with path : " +src_folder_name)


#server name
server_identity = socket.gethostname()
#year and month
now = datetime.datetime.now()
c_year = now.strftime("%Y")
c_month = now.strftime("%B")
c_date = now.strftime("%d-%m-%Y")


  
#file list
def ListFolder(parent):
  file_list=[]
  file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
  #print file_list
  for files in file_list:
    print('title: %s, id: %s' % (files['title'], files['id']))


#get folder ID
def getFolderID(req_parent_folder,req_folder):
  f_exists = 0
  folder_list=[]
  folder_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % req_parent_folder}).GetList()
  for folders in folder_list:
    if folders['title'] == req_folder:
      #print('%s' % folders['id'])
      return folders['id']
      f_exists = 1
      break
    else:
      f_exists = 0
	  
  if f_exists == 0:
    #print("NF")
    return 1

#create folder in parent folder	
def CreateFolderStructure(parent_folder,folder_name):
  exists = 0
  file_folder_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent_folder}).GetList()
  if file_folder_list == []:
    #print("Folders is completely empty")
    #print("creating folder")
    d = drive.CreateFile({"title": folder_name, "parents": [{"id": parent_folder}], "mimeType": "application/vnd.google-apps.folder"})
    d.Upload()
  else:
    for file_folders in file_folder_list:
      if file_folders['title'] == folder_name:
        #print("Folder exists")
        exists = 1
        break
      else:
        exists = 0
	
    if exists == 0:	
      #print("creating folder")
      d = drive.CreateFile({"title": folder_name, "parents": [{"id": parent_folder}], "mimeType": "application/vnd.google-apps.folder"})
      d.Upload()

	  
#Folder Structure
#SERVER_NAME_IP --> YEAR --> MONTH --> DATE --> FILES
#Creating complete folder structure
time.sleep(1)	  
CreateFolderStructure('root',server_identity)
time.sleep(1)
CreateFolderStructure(getFolderID('root',server_identity),c_year)
time.sleep(1)
CreateFolderStructure(getFolderID(getFolderID('root',server_identity),c_year),c_month)
time.sleep(1)
CreateFolderStructure(getFolderID(getFolderID(getFolderID('root',server_identity),c_year),c_month),c_date)
time.sleep(1)
CreateFolderStructure(getFolderID(getFolderID(getFolderID(getFolderID('root',server_identity),c_year),c_month),c_date),target_upload_dir)
time.sleep(1)

print("Created a folder structure on GOOGLE DRIVE as : " + server_identity + "/" + c_year + "/" + c_month + "/" + c_date + "/" + target_upload_dir)

# Enter the source folder
try:
  chdir(src_folder_name)
#Print error if source folder doesn't exist
except OSError:
  print(src_folder_name + 'is missing')
  # Auto-iterate through all files in the folder.
  sys.exit(1)
  
if os.path.isdir(file_data) == True:
  #upload all files in a dir
  for files in listdir(src_folder_name):

    if path.isfile(files):
      statinfo = stat(files)
      if statinfo.st_size > 0:
        print('uploading ' + files)
        #Upload files to Drive in created path/folder	
        f = drive.CreateFile({ "title" : files, "parents" : [{"id": getFolderID(getFolderID(getFolderID(getFolderID(getFolderID('root',server_identity),c_year),c_month),c_date),target_upload_dir)}]})	
        f.SetContentFile(src_folder_name + "/" + files)
        f.Upload()
        print("Uploading done for " +files)
        #skip the file if it's empty
      else:
        print('file {0} is empty'.format(files))
else:
  #upload a single file
  if stat(src_file_name).st_size > 0:
    print('uploading ' + src_file_name)
    #Upload files to Drive in created path/folder	
    f = drive.CreateFile({ "title" : src_file_name, "parents" : [{"id": getFolderID(getFolderID(getFolderID(getFolderID(getFolderID('root',server_identity),c_year),c_month),c_date),target_upload_dir)}]})	
    f.SetContentFile(src_folder_name + "/" + src_file_name)
    f.Upload()
    print("Uploading done for " + src_file_name)
    #skip the file if it's empty
  else:
    print('file {0} is empty'.format(src_file_name))
