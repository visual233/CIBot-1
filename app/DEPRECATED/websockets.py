import json
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.sessions import channel_session, http_session

# for Channels app use - Websocket endpoint
#

@channel_session_user_from_http
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Add them to the right group
    Group("QID0").add(message.reply_channel)

@channel_session_user
def ws_message(message):
    message.reply_channel.send({"text": "direct??"})
    Group("QID0").send({
        "text": message['text'] + "asdasd",
        # "bytes": b'12354'
    })

@channel_session_user
def ws_disconnect(message):
    Group("QID0").discard(message.reply_channel)