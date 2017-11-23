import json
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def ws_connect(message):

    if not message.user.is_authenticated:
        message.reply_channel.send({"close": True})
        return

    message.reply_channel.send({
        "text": json.dumps({
            "action": "reply_channel",
            "reply_channel": message.reply_channel.name,
        })
    })


@channel_session_user_from_http
def ws_receive(message):
    pass
