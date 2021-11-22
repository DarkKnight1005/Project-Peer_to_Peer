import socket
import datetime
import time
import pickle
import threading

MAX_BYTES = 65535
server_port = 9908
next_client_port = server_port
sock = None;
selfUsername = "SERVER";
global_mp = {}

connectionHost = ('127.0.0.1', server_port);

def initSocket():
    global sock

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(connectionHost)

def server(stop):
    global sock
    global next_client_port

    print('Listening at {}'.format(sock.getsockname()))
    while True:
        if stop():
            break

        data, address = sock.recvfrom(MAX_BYTES)  
        obj = pickle.loads(data)
        print(obj, end="   ---   ")
        print(address)
        
        if obj["messageType"] == "Login" and (not obj["username"] in global_mp):
            next_client_port += 1
            global_mp[obj["username"]] = next_client_port
            print(next_client_port)
            obj = {"message" : next_client_port, "messageType": "Auth"}
        
        if obj["messageType"] == "RecieverPortRequest" and obj["reciever"] in global_mp:
            recieverAdress = getUserAdress(obj["reciever"])
            print("reciever port   ---   ", end="")
            print(recieverAdress)
            obj = {"message" : recieverAdress, "messageType": "RecieverPort"}

        message = pickle.dumps(obj);
        sock.sendto(message, address)


def getDataForCommand(objData):

    _data = ""
    message = objData["messageType"];

    if message[1:] == "show_users":
        _tempUNames = global_mp.keys()
        _tempUNames = list(_tempUNames)
        _tempUNames.remove(objData["username"])
        _data = "\n".join(str(x) for x in _tempUNames)
        _data = "List of online users: \n*************\n" + _data + "\n*************\n"
    elif message[1:] == "end_session":
        global_mp.pop(objData["username"]);
        _data = "\nBye...\n"
    return _data

def getUserAdress(username):
    adress = None

    if username in global_mp:
        adress = global_mp[username]

    return adress
        
        
serverThread = None
stop_threads = False

def inputer():
    global stop_threads
    a = input()
    stop_threads = True;
    serverThread.join();
    exit()

if __name__ == '__main__':
    initSocket()
    serverThread = threading.Thread(target=server, args =(lambda : stop_threads, ))
    serverThread.start()
    inputer()