import ftplib
import os
import socket
import time

rf_ftp = None

def connect(host, port=21, user='anonymous', password='anonymous@', timeout=30):
    global rf_ftp
    output_msg = ""

    if __checkFTPStatus(True):
        rf_ftp = RF_HDFS()
        output_msg = rf_ftp.connect_and_login(host=host, port=port,
            user=user, password=password, timeout=timeout)
        print("Response: " + output_msg)
        return output_msg

def get_current_directory():
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        output_msg = rf_ftp.pwd()
        print("Response: " + output_msg)
        return output_msg

def change_directory(directory):
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        output_msg = rf_ftp.cwd(directory)
        print("Response: " + output_msg)
        return output_msg

def create_directory(newDirName):
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        output_msg = rf_ftp.mkd(newDirName)
        print("Response: " + output_msg)
        return output_msg

def remove_directory(directory):
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        output_msg = rf_ftp.rmd(directory)
        print("Response: " + output_msg)
        return output_msg

def list_directory(path=None):
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        rf_ftp.send_cmd('TYPE A')
        dirList = rf_ftp.dir(path)
        rf_ftp.send_cmd('TYPE I')
        for d in dirList:
            output_msg += d + "\n"
        print(output_msg)
        return dirList

def list_files_in_directory(path=None):
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        rf_ftp.send_cmd('TYPE A')
        nameList = rf_ftp.nlst(path)
        rf_ftp.send_cmd('TYPE I')
        for d in nameList:
            output_msg += d + "\n"
        print(output_msg)
        return nameList

def upload_file(localFileName,remoteFileName=None):
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        output_msg = rf_ftp.storbinary('STOR', localFileName,remoteFileName)
        print("Response: " + output_msg)
        return output_msg

def append_to_file(localFileName,remoteFileName=None):
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        output_msg = rf_ftp.storbinary('APPE', localFileName,remoteFileName)
        print("Response: " + output_msg)
        return output_msg

def download_file(remoteFilename,localFileName=None):
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        output_msg = rf_ftp.retrbinary(remoteFilename,localFileName)
        print("Response: " + output_msg)
        return output_msg

def rename_file(targetFile,newName):
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        output_msg = rf_ftp.rename(targetFile,newName)
        print("Response: " + output_msg)
        return output_msg

def remove_file(targetFile):
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        output_msg = rf_ftp.delete(targetFile)
        print("Response: " + output_msg)
        return output_msg

def get_file_size(fileToCheck):
    global rf_ftp
    sizeOfFile = 0
    output_msg = ""
    if __checkFTPStatus():
        sizeOfFile = rf_ftp.size(fileToCheck)
        print("Response: " + str(sizeOfFile))
        return sizeOfFile

def get_modified_time(file):
    global rf_ftp
    mdtm_string = ""
    if __checkFTPStatus():
        mdtm_string = rf_ftp.send_cmd('MDTM ' + file)
        #
        # MDTM output is of the form: '213 20151111144708' which would be 11/11/2015 14:47:08 GMT
        #
        # Unfortunately, Harmony is returning the result in server local time not GMT.
        #
        print("Response: " + mdtm_string)
        pattern = '%Y%m%d%H%M%S%Z'
        epoch = int(time.mktime(time.strptime(mdtm_string[4:] + 'UTC', pattern)))
        return str(epoch)

def get_welcome_message():
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        output_msg = rf_ftp.welcome()
        print("Response: " + output_msg)
        return output_msg

def send_command(command):
    global rf_ftp
    output_msg = ""
    if __checkFTPStatus():
        output_msg = rf_ftp.send_cmd(command)
        print("Response: " + output_msg)
        return output_msg

def close():
    global rf_ftp
    if __checkFTPStatus():
        rf_ftp.close()
    rf_ftp = None

def __checkFTPStatus(inverted=False):
    global rf_ftp
    if inverted:
        if not isinstance(rf_ftp,RF_HDFS):
            return True
        else:
            raise FtpLibraryError("Active FTP connection already exists.")
    else:
        if isinstance(rf_ftp,RF_HDFS):
            if(rf_ftp.checkConnectionStatus()):
                return True
            else:
                errorMsg = "FTP connection was not established properly."
                rf_ftp = None
                raise FtpLibraryError(errorMsg)
        else:
            errorMsg = "No active FTP connection exists."
            raise FtpLibraryError(errorMsg)

class RF_HDFS(object):
    def __init__(self):
        self.f = ftplib.FTP()

    def connect_and_login(self, **kwargs):
        output_msg = ""
        host = ""
        port = -1
        timeout = -1
        user = ""
        password = ""

        if 'host' in kwargs:
            host = kwargs['host']
        if 'port' in kwargs:
            port = kwargs['port']
        if 'timeout' in kwargs:
            timeout = kwargs['timeout']
        if 'user' in kwargs:
            user = kwargs['user']
        if 'password' in kwargs:
            password = kwargs['password']
        self.connectionStatus = False
        try:
            timeout = int(timeout)
            port = int(port)
            if host!= "" and port>0 and timeout>0:
                output_msg += self.f.connect(host,port,timeout)
            elif host!= "" and port>0:
                output_msg += self.f.connect(host,port)
            elif host!= "" and timeout>0:
                output_msg += self.f.connect(host,21,timeout)
            else:
                output_msg += self.f.connect(host)
            output_msg += self.f.login(user,password)
        except socket.error as se:
            raise FtpLibraryError('Socket error exception occured.')
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        self.connectionStatus = True
        return output_msg

    def checkConnectionStatus(self):
        return self.connectionStatus

    def welcome(self):
        output_msg = ""
        try:
            output_msg += self.f.getwelcome()
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return output_msg

    def pwd(self):
        output_msg = ""
        try:
            output_msg += self.f.pwd()
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return output_msg

    def dir(self, path):
        dirList = []
        try:
            if path != None:
                self.f.dir(path, dirList.append)
            else:
                self.f.dir(dirList.append)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return dirList

    def nlst(self, path):
        nameList = []
        try:
            if path != None:
                nameList = self.f.nlst(path)
            else:
                nameList = self.f.nlst()
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return nameList

    def cwd(self,directory):
        output_msg = ""
        try:
            output_msg += self.f.cwd(directory)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return output_msg

    def mkd(self,newDirName):
        output_msg = ""
        try:
            output_msg += self.f.mkd(newDirName)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return output_msg

    def rmd(self,directory):
        output_msg = ""
        try:
            output_msg += self.f.rmd(directory)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return output_msg

    def retrbinary(self,ftpFileName,localFileName=None):
        output_msg = ""
        localPath = ""
        if localFileName==None:
            localPath = ftpFileName
        else:
            localPath = os.path.normpath(localFileName)
            if os.path.isdir(localPath):
                localPath = os.path.join(localPath,ftpFileName)
        try:
            with open(localPath, 'wb') as localFile:
                output_msg += self.f.retrbinary("RETR " + ftpFileName, localFile.write)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return output_msg

    def storbinary(self, cmd, localFileName,ftpFileName=None):
        output_msg = ""
        remoteFileName = ""
        localPath = os.path.normpath(localFileName)
        if not os.path.isfile(localPath):
            raise FtpLibraryError("Valid file path should be provided.")
        else:
            if ftpFileName==None:
                fileTuple = os.path.split(localFileName)
                if len(fileTuple)==2:
                    remoteFileName = fileTuple[1]
                else:
                    remoteFileName = 'defaultFileName'
            else:
                remoteFileName = ftpFileName
            try:
                with open(localPath, "rb") as localFile:
                    output_msg += self.f.storbinary(cmd + " " + remoteFileName, localFile)
            except ftplib.all_errors as e:
               raise FtpLibraryError(str(e))
        return output_msg

    def size(self,ftpFileName):
        sizeOfFile = -1
        try:
            sizeOfFile = self.f.size(ftpFileName)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return sizeOfFile

    def rename(self, srcFile, dstFile):
        output_msg = ""
        try:
            output_msg += self.f.rename(srcFile,dstFile)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return output_msg

    def delete(self,srcFile):
        output_msg = ""
        try:
            output_msg += self.f.delete(srcFile)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return output_msg

    def send_cmd(self,cmd):
        output_msg = ""
        try:
            output_msg += self.f.sendcmd(cmd)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        return output_msg

    def close(self):
        try:
            self.f.close()
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))

class FtpLibraryError(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return self.msg
