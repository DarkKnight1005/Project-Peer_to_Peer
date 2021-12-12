from typing import Mapping
from src_server.DatabaseManager import *
from src_server.Globals.globalConsts import GlobalConsts

class MainConfiguration:
    def __init__(self) -> None:
        self.red = RedisController().red
        self.globalConsts = GlobalConsts()

    def configureApp(self):
        self.red.flushdb()
        self.red.set("next_client_port", self.globalConsts.server_port + 1)