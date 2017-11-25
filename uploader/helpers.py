import os
import bz2
import json
from django.conf import settings
from .choices import ActionType
from resurfedtools.helpers import send_channel_message, generate_json_response


def handle_uploaded_file(f):
    path = f"{settings.UPLOAD_PATH}/{f}"
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path


def compress(reply_channel, file_path):
    total_size = os.path.getsize(file_path)
    compressed_path = f"{file_path}.bz2"

    with open(file_path, 'rb') as uncompressed_file, bz2.BZ2File(compressed_path, 'wb') as compressed_file:
        for data in iter(lambda: uncompressed_file.read(1000 * 1024), b''):
            compressed_file.write(data)
            percent_complete = round((uncompressed_file.tell() / total_size) * 100)

            send_channel_message(reply_channel, generate_json_response(ActionType.PROGRESS_UPDATE, percent_complete))
