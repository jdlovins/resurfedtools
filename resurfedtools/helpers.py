import json

from channels import Channel


def generate_json_response(action, data):
    return json.dumps({
        "action": action,
        "data": data
    })


def send_channel_message(reply_channel, data):
    Channel(reply_channel).send({
        "text": data
    })
