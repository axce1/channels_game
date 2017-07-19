from channels.routing import route
from channels.routing import route_class
from channels.staticfiles import StaticFilesConsumer

from apps.game import consumers


channel_routing = [
    route_class(consumers.LobbyConsumer, path=r"^/lobby/"),
]
