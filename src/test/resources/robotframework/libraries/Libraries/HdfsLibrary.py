from hdfs import Client
from hdfs.util import HdfsError
from boltons.fileutils import FilePerms
from com.cleo.qa.cloudera.hdfs import WebHDFS

rf_hdfs = None

def connect(host, port=50070, kdc=None, user='hdfs', password=None, proxy=None, root="/", timeout=30):
    global rf_hdfs

    if __checkHDFSStatus(True):
        rf_hdfs = RF_HDFS()
        client = rf_hdfs.connect_and_login(host=host, port=port, kdc=kdc,
            user=user, password=password, proxy=proxy, root=root, timeout=timeout)
        print("Response: Connected")
        return True

def create_directory(directory, permission=None):
    response = "Response: {0} '{1}' = {2}"
    name = 'Create Directory'
    global rf_hdfs

    if __checkHDFSStatus():
        result = None
        try:
            rf_hdfs.mkdir(directory, permission)
            args = (name, directory, 'OK')
            result = True
        except HdfsLibraryError as error:
            args = (name, directory, str(error))
            result = False

        print(response.format(*args))
        return result

def remove_directory(directory):
    response = "Response: {0} '{1}' = {2}"
    name = 'Remove Directory'
    global rf_hdfs

    if __checkHDFSStatus():
        result = None
        args = ()
        try:
            rf_hdfs.rmdir(directory)
            args = (name, directory, 'OK')
            result = True
        except HdfsLibraryError as error:
            args = (name, directory, str(error))
            result = False

        print(response.format(*args))
        return result

def list_directory(directory=None):
    response = "Response: {0} '{1}' = {2}"
    name = 'List Directory'
    global rf_hdfs

    if __checkHDFSStatus():
        list = []
        try:
            list = rf_hdfs.list_dir(directory)
            print("Response: " + str(list))
        except HdfsLibraryError as error:
            args = ()
            if directory == None:
                args = (name, '<cwd>', str(error))
            else:
                args = (name, directory, str(error))
            print(response.format(*args))

        return list

def list_files_in_directory(directory=None):
    response = "Response: {0} '{1}' = {2}"
    name = 'List Files In Directory'
    global rf_hdfs

    if __checkHDFSStatus():
        list = []
        try:
            list = rf_hdfs.list_names(directory)
            print("Response: " + str(list))
        except HdfsLibraryError as error:
            args = ()
            if directory == None:
                args = (name, '<cwd>', str(error))
            else:
                args = (name, directory, str(error))
            print(response.format(*args))

        return list

def upload_file(local_file, remote_file, overwrite=False, permission=None):
    response = "Response: {0} '{1}' as '{2}' = {3}"
    name = 'Upload File'
    global rf_hdfs

    if __checkHDFSStatus():
        path = None
        args = ()
        try:
            path = rf_hdfs.upload(remote_file, local_file, overwrite, permission)
            args = (name, local_file, remote_file, path)
        except HdfsLibraryError as error:
            args = (name, local_file, remote_file, str(error))

        print(response.format(*args))
        return path

def download_file(remote_file, local_file, overwrite=False):
    response = "Response: {0} '{1}' as '{2}' = {3}"
    name = 'Download File'
    global rf_hdfs

    if __checkHDFSStatus():
        path = None
        args = ()
        try:
            path = rf_hdfs.download(remote_file, local_file, overwrite)
            args = (name, remote_file, local_file, path)
        except HdfsLibraryError as error:
            args = (name, remote_file, local_file, str(error))

        print(response.format(*args))
        return path

def rename_file(src_file, dst_file):
    response = "Response: {0} '{1}' to '{2}' = {3}"
    name = 'Rename File'
    global rf_hdfs

    if __checkHDFSStatus():
        result = None
        args = ()
        try:
            rf_hdfs.rename(src_file, dst_file)
            args = (name, src_file, dst_file, 'OK')
            result = True
        except HdfsLibraryError as error:
            args = (name, src_file, dst_file, str(error))
            result = False

        print(response.format(*args))
        return result

def remove_file(file):
    response = "Response: {0} '{1}' = {2}"
    name = 'Remove File'
    global rf_hdfs

    if __checkHDFSStatus():
        result = None
        args = ()
        try:
            rf_hdfs.delete(file)
            args = (name, file, 'OK')
            result = True
        except HdfsLibraryError as error:
            args = (name, file, str(error))
            result = False

        print(response.format(*args))
        return result

def get_file_size(file):
    response = "Response: {0} '{1}' = {2}"
    name = 'Get File Size'
    global rf_hdfs

    if __checkHDFSStatus():
        size = -1
        args = ()
        try:
            size = get_path_status(file)['length']
            args = (name, file, str(size))
        except HdfsLibraryError as error:
            args = (name, file, str(error))

        print(response.format(*args))
        return size

def get_modified_time(file):
    response = "Response: {0} '{1}' = {2}"
    name = 'Get Modified Time'
    global rf_hdfs

    if __checkHDFSStatus():
        mod_time = -1
        args = ()
        try:
            mod_time = get_path_status(file)['modificationTime']
            # Return epoch time in seconds, not milliseconds
            # mod_time = str(int(mod_time)/1000)
            args = (name, file, str(mod_time))
        except HdfsLibraryError as error:
            args = (name, file, str(error))

        print(response.format(*args))
        return mod_time

def set_modified_time(file, mod_time):
    response = "Response: {0} '{1}' '{2}' = {3}"
    name = 'Set Modified Time'
    global rf_hdfs

    if __checkHDFSStatus():
        result = None
        args = ()
        try:
            # Set epoch time in milliseconds, not seconds
            # mod_time = str(int(mod_time)*1000)
            rf_hdfs.set_time(file, mod_time)
            args = (name, file, mod_time, 'OK')
            result = True
        except HdfsLibraryError as error:
            args = (name, file, mod_time, str(error))
            result = False

        print(response.format(*args))
        return result

def set_owner(path, owner, group=None):
    response = "Response: {0} '{1}' owner='{2}' group='{3}' = {4}"
    name = 'Set Owner'
    global rf_hdfs

    if __checkHDFSStatus():
        result = None
        args = ()
        try:
            rf_hdfs.set_owner(path, owner, group)
            args = (name, path, owner, group, 'OK')
            result = True
        except HdfsLibraryError as error:
            args = (name, path, owner, group, str(error))
            result = False

        print(response.format(*args))
        return result

def set_permissions(path, **kwargs):
    response = "Response: {0} '{1}' mode='{2}' = {3}"
    name = 'Set Permissions'
    global rf_hdfs

    mode = oct(int(FilePerms(**kwargs)))[-3:]
    if __checkHDFSStatus():
        result = None
        args = ()
        try:
            rf_hdfs.set_permission(path, mode)
            args = (name, path, mode, 'OK')
            result = True
        except HdfsLibraryError as error:
            args = (name, path, mode, str(error))
            result = False

        print(response.format(*args))
        return result

def set_acl(path, aclspec):
    response = "Response: {0} '{1}' aclspec='{2}' = {3}"
    name = 'Set ACL'
    global rf_hdfs

    if __checkHDFSStatus():
        result = None
        args = ()
        try:
            rf_hdfs.set_acl(path, aclspec)
            args = (name, path, aclspec, 'OK')
            result = True
        except HdfsLibraryError as error:
            args = (name, path, aclspec, str(error))
            result = False

        print(response.format(*args))
        return result

def get_path_status(path):
    response = "Response: {0} '{1}' = {2}"
    name = 'Get Path Status'
    global rf_hdfs

    if __checkHDFSStatus():
        status = None
        args = ()
        try:
            status = rf_hdfs.status(path)
            args = (name, path, str(status))
        except HdfsLibraryError as error:
            args = (name, path, str(error))

        print(response.format(*args))
        return status

#
# This one's a little strange. The checksum returned by checksum() is of the form:
#
# 0000020000000000000000008437ced3acbda21e12240be6509f60ae00000000
#                        ^                                ^
# header................ |..This is the actual checksum...|trailer
#
# with 24 characters of header and 8 characters of trailer. So, we need to slice
# the returned value and only return the 'actual checksum'.
#
def get_checksum(path):
    response = "Response: {0} '{1}' = {2}"
    name = 'Get Checksum'
    global rf_hdfs

    if __checkHDFSStatus():
        checksum = None
        args = ()
        try:
            checksum = rf_hdfs.checksum(path)
            checksum.pop('length')
            bytes = checksum.pop('bytes')
            checksum[u'checksum'] = bytes[24:56].lower()
            args = (name, path, str(checksum))
        except HdfsLibraryError as error:
            args = (name, path, str(error))

        print(response.format(*args))
        return checksum

def close():
    global rf_hdfs
    if __checkHDFSStatus():
        rf_hdfs.close()
    rf_hdfs = None


def __checkHDFSStatus(inverted=False):
    global rf_hdfs

    if inverted:
        if not isinstance(rf_hdfs, RF_HDFS):
            return True
        else:
            raise HdfsLibraryError("Active HDFS connection already exists.")
    else:
        if isinstance(rf_hdfs, RF_HDFS):
            if rf_hdfs.checkConnectionStatus():
                return True
            else:
                errorMsg = "HDFS connection was not established properly."
                rf_hdfs = None
                raise HdfsLibraryError(errorMsg)
        else:
            errorMsg = "No active HDFS connection exists."
            raise HdfsLibraryError(errorMsg)

class RF_HDFS(object):
    def __init__(self):
        self.client = None
        self.directory = None

    def connect_and_login(self, **kwargs):
        import requests

        host = None
        port = None
        user = None
        password = None
        root = None
        timeout = None
        proxy = None

        if 'host' in kwargs:
            host = kwargs['host']
        if 'port' in kwargs:
            port = kwargs['port']
        if 'kdc' in kwargs:
            kdc = kwargs['kdc']
        if 'user' in kwargs:
            user = kwargs['user']
        if 'password' in kwargs:
            password = kwargs['password']
        if 'root' in kwargs:
            root = kwargs['root']
        if 'proxy' in kwargs:
            proxy = kwargs['proxy']
        if 'timeout' in kwargs:
            timeout = kwargs['timeout']

        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_maxsize=0)
        self.session.mount('http://',  adapter)
        self.session.mount('https://', adapter)
        self.session.headers.update({'Connection':'Keep-Alive'})

        self.connectionStatus = False
        try:
            timeout = int(timeout)
            url = "http://" + host + ":" + str(port)

            hdfsLogin = WebHDFS(url, kdc)
            cookieStr = hdfsLogin.authenticate(user, password)
            if cookieStr != None:
                cookieList = cookieStr.split('=', 1)
                cookieDict = {cookieList[0]: cookieList[1]}
                requests.utils.add_dict_to_cookiejar(self.session.cookies, cookieDict)

            self.client = Client(url, root=root, proxy=proxy, timeout=timeout, session=self.session)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))

        self.connectionStatus = True
        return self.client

    def checkConnectionStatus(self):
        return self.connectionStatus

    def list_dir(self, directory):
        output = []
        try:
            if directory != None:
                output = self.client.list(directory, status=True)
            else:
                output = self.client.list(self.client.root, status=True)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))
        return output

    def list_names(self, directory):
        output = []
        try:
            if directory != None:
                output = self.client.list(directory, status=False)
            else:
                output = self.client.list(self.client.root, status=False)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))
        return output

    def upload(self, remote_path, local_path, overwrite=False, permission=None):
        output = None
        try:
            output = self.client.upload(remote_path, local_path, overwrite, permission=permission)
        except HdfsError as hdfsError:
            # For some reason this exception includes the entire stack trace after
            # the error message, so split on '\n' and only return the first line.
            error = str(hdfsError).splitlines()[0]
            raise HdfsLibraryError(error)
        except Exception as exception:
            raise HdfsLibraryError(str(exception))
        return output

    def download(self, remote_path, local_path, overwrite=False):
        output = None
        try:
            output = self.client.download(remote_path, local_path, overwrite)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))
        return output

    def mkdir(self, directory, permission):
        try:
            # no return value
            self.client.makedirs(directory, permission=permission)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))

    def rmdir(self, directory):
        try:
            # no return value
            if self.client.delete(directory, recursive=True) == False:
                raise HdfsLibraryError("Directory does not exist: %r", directory)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))

    def rename(self, src_file, dst_file):
        try:
            # no return value
            self.client.rename(src_file, dst_file)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))

    def delete(self, file):
        try:
            # no return value
            if self.client.delete(file) == False:
                raise HdfsLibraryError("File does not exist: %r", file)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))

    def set_time(self, file, mod_time):
        try:
            # no return value
            self.client.set_times(file, -1, mod_time)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))

    def set_owner(self, file, owner, group):
        try:
            # no return value
            self.client.set_owner(file, owner=owner, group=group)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))

    def set_permission(self, file, permission):
        try:
            # no return value
            self.client.set_permission(file, permission=permission)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))

    def set_acl(self, file, aclspec):
        try:
            # no return value
            self.client.set_acl(file, aclspec=aclspec)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))

    def status(self, path):
        output = ''
        try:
            output = self.client.status(path)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))
        return output

    def checksum(self, path):
        output = ''
        try:
            output = self.client.checksum(path)
        except HdfsError as hdfsError:
            raise HdfsLibraryError(str(hdfsError))
        except Exception as exception:
            raise HdfsLibraryError(str(exception))
        return output

    def close(self):
        self.session.close()

class HdfsLibraryError(Exception):
    def __init__(self, message, *args):
        super(HdfsLibraryError, self).__init__(message % args if args else message)
