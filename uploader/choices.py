import urllib
from urllib.error import HTTPError

from django.conf import settings
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


class MapType(DjangoChoices):
    LINEAR = ChoiceItem('Linear')
    STAGED = ChoiceItem('Staged')


class ActionType(DjangoChoices):
    GENERAL_ERROR = ChoiceItem("general_error")
    STARTED_TASK = ChoiceItem("started_task")
    FORM_ERROR = ChoiceItem("form_error")
    PROGRESS_UPDATE = ChoiceItem("progress_update")
    REPLY_CHANNEL = ChoiceItem("reply_channel")
    MESSAGE = ChoiceItem("message")


MapTypeChoices = (
    (0, MapType.STAGED),
    (1, MapType.LINEAR)
)


def get_live_maps():

    maps = []
    count = 1

    maps.append(["", "Map"])

    for url in settings.LIVE_MAP_URLS:
        try:
            for line in urllib.request.urlopen(url):
                m = line.decode('ascii').split('\n')[0]
                if len(m) > 0:
                    maps.append((count,m))
                    count += 1
        except HTTPError as e:
            pass

    print("We are collecting maps")
    return maps
