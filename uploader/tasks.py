from __future__ import absolute_import
import os
from resurfedtools.celery import app
from .models import Server
from .choices import ActionType, ServerType
from resurfedtools.helpers import generate_json_response, send_channel_message
import logging
from .helpers import compress
from functools import partial
from .uploader import Uploader

log = logging.getLogger(__name__)


@app.task(name="tasks.upload_file")
def upload_file(reply_channel, file_path, servers_ids, delete_map, replace_map, old_map):
    servers = [Server.objects.get(pk=server) for server in servers_ids]
    base_name = os.path.basename(file_path)
    send_message = partial(send_channel_message(reply_channel))

    compressed = False

    for server in servers:

        uploader = Uploader.factory(server.connectioninfo)

        if server.server_type == ServerType.FAST_DL or server.server_type == ServerType.FAST_DL_PUBLIC:
            if not compressed:
                send_message(generate_json_response(ActionType.GENERAL_ERROR, f"Starting to compress {base_name}"))
                try:
                    compress(reply_channel, file_path)
                    compressed = True
                except IOError as ioe:
                    send_message(generate_json_response(ActionType.GENERAL_ERROR, f"An IO error occurred: {ioe}"))
                    return



@app.task(name="tasks.insert_map_information")
def insert_map_information():
    pass
