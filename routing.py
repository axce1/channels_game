from channels.routing import route, route_class
from channels.staticfiles import StaticFilesConsumer
from apps.game import consumenrs

channel_routing = [
    route_class(consumenrs.LobbyConsumer, path=r"^/lobby/"),
]
