from channels.routing import route

from DEPRECATED.websockets import ws_connect, ws_message, ws_disconnect

# 路由分发层 Router - Websocket
#


routingtable = [
    route("websocket.receive", ws_message),
    route("websocket.connect", ws_connect),
    route("websocket.disconnect", ws_disconnect),
]