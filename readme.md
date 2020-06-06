# Google Drive Upload

 [![PyDrive](https://pypi.org/static/images/logo-small.6eef541e.svg)](https://pypi.org/project/PyDrive/)
 ### based on PyDrive 1.3.1

This script can push a file or all files within a folder to google drive.

### Features!

  - Uploading is a one way push
  - No need to authenticate to drive api everytime manually.



#### Requirements

Install the dependencies

```sh
$ sudo apt install python3-pip
$ sudo pip3 install pydrive
```

For Ubuntu 16 , you will need Python 3.6

```sh
$ sudo pip3 install pydrive
$ sudo sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo sudo apt-get update
$ sudo sudo apt-get install python3.6
$ sudo curl https://bootstrap.pypa.io/get-pip.py | sudo python3.6
$ sudo pip3.6 install --upgrade google-auth-oauthlib
$ sudo pip install httplib2==0.15.0
$ sudo pip install google-api-python-client==1.6
```

### How to Authenticate

Follow this guideline (https://pythonhosted.org/PyDrive/quickstart.html#authentication)

### Usage

```sh
$ git clone -b master https://github.com/vaibhavkite3/gdrive_upload_sync.git
$ cd gdrive_upload_sync
$ python3 upload.py
OR
$ python3.6 upload.py
```

### Todos

 - Adding support to Windows OS
 - Two Way sync

License
----

[MIT]