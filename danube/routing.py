from channels.routing import ProtocolTypeRouter, URLRouter

from danube.chat import routing

application = ProtocolTypeRouter({
    'websocket':
        URLRouter(
            routing.websocket_urlpatterns
        ),
})
