import abc
import ftplib

import ftputil
from .choices import ConnectionType


class Uploader(metaclass=abc.ABCMeta):
    @staticmethod
    def factory(info):
        if info.connection == ConnectionType.FTP:
            return FTPUploader(info)
        if info.connection == ConnectionType.SFTP:
            return SFTPUploader(info)
        if info.connection == ConnectionType.FTPS:
            return FTPSUploader(info)

    def __init__(self, info):
        self.username = info.username
        self.password = info.password
        self.host = info.host
        self.port = info.port


    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def upload(self):
        pass

    @abc.abstractmethod
    def download(self):
        pass

    @abc.abstractmethod
    def delete(self, file):
        pass

    @abc.abstractmethod
    def cd(self, directory):
        pass

    @abc.abstractmethod
    def pwd(self):
        pass

    @abc.abstractmethod
    def exists(self, file):
        pass


class FTPUploader(Uploader):
    def __init__(self, info):
        super().__init__(info)
        self.client = None

    def connect(self):
        self.client = ftputil.FTPHost(self.host, self.username, self.password, self.port,
                                      session_factory=FTPPortSession)

    def upload(self):
        pass

    def download(self):
        pass

    def delete(self, file):
        self.client.remove(file)

    def cd(self, directory):
        self.client.chdir(directory)

    def pwd(self):
        return self.client.pwd()

    def exists(self, file):
        return self.client.exists(file)


class FTPSUploader(FTPUploader):
    def __init__(self, info):
        super().__init__(info)

    def connect(self):
        self.client = ftputil.FTPHost(self.host, self.username, self.password, self.port,
                                      session_factory=FTPTLSPortSession)

class SFTPUploader(Uploader):

    def __init__(self, info):
        super().__init__(info)


class FTPPortSession(ftplib.FTP):
    def __init__(self, host, userid, password, port):
        ftplib.FTP.__init__(self)
        self.connect(host, port)
        self.login(userid, password)


class FTPTLSPortSession(ftplib.FTP_TLS):
    def __init__(self, host, userid, password, port):
        ftplib.FTP_TLS.__init__(self)
        self.connect(host, port)
        self.login(userid, password)
        self.prot_p()
