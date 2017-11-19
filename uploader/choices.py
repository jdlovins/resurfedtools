from djchoices import DjangoChoices, ChoiceItem


class UploadType(DjangoChoices):
    FTP = ChoiceItem()
    FTPS = ChoiceItem()
    SFTP = ChoiceItem()


class ServerType(DjangoChoices):
    FAST_DL = ChoiceItem()
    FAST_DL_PUBLIC = ChoiceItem()
    SERVER = ChoiceItem()
    SERVER_PUBLIC = ChoiceItem()