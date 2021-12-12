from .globalConsts import *


class ConnectionData:

    def __init__(self) -> None:

        self._GlobalConsts = GlobalConsts()

        self.connectionHostToServer = ('127.0.0.1', self._GlobalConsts.server_port);

        self.connectionHostToPeer = ('127.0.0.1', self._GlobalConsts.server_port)

        self.connectionSelfHost = ('127.0.0.1', self._GlobalConsts.server_port)

