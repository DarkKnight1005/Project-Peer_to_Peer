from src.Displayers.displayer import Displayer
import pickle

class Processor:
    def __init__(self) -> None:
        self.Displayer = Displayer
    
    def processMessage(self, data):

        obj = pickle.loads(data)

        try:    
            Displayer.displayMessage(obj)
        except:
            Displayer.displayExcpetionMessage(obj)
    
    def processMessageAuth(selfd, selfport, connectionData, self_server):

        lst = list(connectionData.connectionSelfHost)
        lst[1] = int(selfport)
        connectionData.connectionSelfHost = tuple(lst)
        self_server(connectionData.connectionSelfHost)

    def processSendMessageToPort(self, client_sock, connectionData, recieverPort, new_obj):

        # new_obj = {"username": selfUsername, "message": message_to_send}
        message = pickle.dumps(new_obj)
        lst = list(connectionData.connectionHostToPeer)
        lst[1] = int(recieverPort)
        connectionHostToPeer = tuple(lst)
        client_sock.sendto(message, connectionHostToPeer)
