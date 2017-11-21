import urllib.request
from urllib.error import HTTPError
from django.conf import settings


def get_live_maps():

    maps = []
    count = 1

    maps.append((0, "--- N/A ---"))

    for url in settings.LIVE_MAP_URLS:
        try:
            for line in urllib.request.urlopen(url):
                m = line.decode('ascii').split('\n')[0]
                if len(m) > 0:
                    maps.append((count,m))
                    count += 1
        except HTTPError as e:
            pass

    return maps