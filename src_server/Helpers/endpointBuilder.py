from src_server.Globals import *

class EnpointBuilder:

    def __init__(self) -> None:
        self._globalConsts = GlobalConsts()
        self._persistentPath = self._globalConsts.persistentApiPath
        self.__path = self._persistentPath
        pass

    def addParam(self, param):
        self.__path += ("/" + param)
        return self

    def build(self):
        tmpPath = self.__path
        self.__path = self._persistentPath
        return tmpPath