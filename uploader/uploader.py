import abc
import ftplib

import ftputil


class Uploader(metaclass=abc.ABCMeta):

    user_name = None
    password = None
    host = None
    port = -1

    def factory(type):
        pass

    @abc.abstractmethod
    def upload(self):
        pass

    @abc.abstractmethod
    def download(self):
        pass

    @abc.abstractmethod
    def delete(self):
        pass

    @abc.abstractmethod
    def cd(self):
        pass

    @abc.abstractmethod
    def pwd(self):
        pass

    @abc.abstractmethod
    def exists(self):
        pass



class FTPUploader(Uploader):

    def __init__(self):
        pass




class SFTPUploader(Uploader):
    def test(self):
        pass


class FTPSUploader(FTPUploader):

    def __init__(self):
        super().__init__()
        print("Before" + self.val)

    def test(self):
        print("Test from FTPS")
        pass


class FtpPortSession(ftplib.FTP_TLS):

    def __init__(self, host, userid, password, port):
        """Act like ftplib.FTP's constructor but connect to another port."""
        ftplib.FTP_TLS.__init__(self)
        self.connect(host, port)
        self.login(userid, password)
        self.prot_p()
