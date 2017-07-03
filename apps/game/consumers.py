import re
import logging
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user
from channels.generic.websockets import JsonWebsocketConsumer

from .models import Game, GameSquare


log = logging.getLogger(__name__)


class LobbyConsumer(JsonWebsocketConsumer):
    # set to True to autmatically port users from HTTP cookies
    http_user = True

    def connection_group(self, **kwargs):
        return ["lobby"]

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})
        pass

    def receive(self, content, **kwargs):
        http_user = True

    def disconnect(self, message, **kwargs):
        pass
