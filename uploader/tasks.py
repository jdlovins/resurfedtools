from __future__ import absolute_import
import os
from resurfedtools.celery import app
from channels import Channel
from .models import Server
from .choices import ActionType
from resurfedtools.helpers import generate_json_response, send_channel_message
import logging
from .helpers import compress

log = logging.getLogger(__name__)


@app.task(name="tasks.upload_file")
def upload_file(reply_channel, file_path, servers, delete_map, replace_map, old_map):
    print("we got called!" + reply_channel)
    base_name = os.path.basename(file_path)
    send_channel_message(reply_channel, generate_json_response(ActionType.MESSAGE, {
        'message': f"Starting to compress {base_name}"
    }))
    compress(reply_channel, file_path)

    pass


@app.task(name="tasks.insert_map_information")
def insert_map_information():
    pass
