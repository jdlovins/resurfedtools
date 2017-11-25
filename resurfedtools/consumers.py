import json
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http
from uploader.choices import ActionType
from .helpers import generate_json_response


@channel_session_user_from_http
def ws_connect(message):
    print("Client connecting")
    if not message.user.is_authenticated:
        print("closing  connection")
        message.reply_channel.send({"close": True})
        return

    message.reply_channel.send({
        "text": generate_json_response(ActionType.REPLY_CHANNEL, {
            'reply_channel': message.reply_channel.name
        })
    })


@channel_session_user_from_http
def ws_receive(message):
    pass
