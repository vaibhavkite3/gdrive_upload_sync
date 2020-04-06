#!/usr/bin/python

#importing PyDrive libraries
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#other libraries
import commands
import datetime
import time
from os import chdir, listdir, stat, path
import sys

#authenticating the gdrive
#this will read settings.yaml and save authentication token to credentials.json
#settings still require client_secrets.json downloaded from API services
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

#Source folder name where backup files are kept
source_path_file="backup_path.txt"
src_folder_name=commands.getoutput("cat "+source_path_file+"")
target_upload_dir=commands.getoutput("basename "+src_folder_name+"")

#project name
project_name="MKCL"
#server name
server_name = commands.getoutput("/bin/hostname")
#server ip address
server_ip = commands.getoutput("/sbin/ifconfig | grep \"inet addr\" | grep -v \"127.0.0.1\" | awk '{print $2}' | cut -d: -f2 | head -n 1")
#server hostname and ip
server_identity = server_name + "_" + server_ip
#year and month
now = datetime.datetime.now()
c_year = now.strftime("%Y")
c_month = now.strftime("%B")


  
#file list
def ListFolder(parent):
  filelist=[]
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
#PROJECT_NAME -- > SERVER_NAME_IP --> YEAR --> MONTH --> FILES
#Creating complete folder structure
time.sleep(1)	  
CreateFolderStructure('root',project_name)
time.sleep(1)
CreateFolderStructure(getFolderID('root',project_name),server_identity)
time.sleep(1)
CreateFolderStructure(getFolderID(getFolderID('root',project_name),server_identity),c_year)
time.sleep(1)
CreateFolderStructure(getFolderID(getFolderID(getFolderID('root',project_name),server_identity),c_year),c_month)
time.sleep(1)
CreateFolderStructure(getFolderID(getFolderID(getFolderID(getFolderID('root',project_name),server_identity),c_year),c_month),target_upload_dir)
time.sleep(1)


# Enter the source folder
try:
  chdir(src_folder_name)
#Print error if source folder doesn't exist
except OSError:
  print(src_folder_name + 'is missing')
  # Auto-iterate through all files in the folder.
  sys.exit(1)
  
for files in listdir(src_folder_name):

  if path.isfile(files):
    statinfo = stat(files)
    if statinfo.st_size > 0:
      print('uploading ' + files)
      #Upload files to Drive in created path/folder	
      f = drive.CreateFile({ "title" : files, "parents" : [{"id": getFolderID(getFolderID(getFolderID(getFolderID(getFolderID('root',project_name),server_identity),c_year),c_month),target_upload_dir)}]})	
      f.SetContentFile(src_folder_name+files)
      f.Upload()
	  
      #skip the file if it's empty
    else:
      print('file {0} is empty'.format(files))