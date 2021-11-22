import socket
import datetime
import time
import pickle
import threading
import sys

MAX_BYTES = 65535
server_port = 9908
selfUsername = "";

connectionHostToServer = ('127.0.0.1', server_port);

connectionHostToPeer = ('127.0.0.1', server_port)

connectionSelfHost = ('127.0.0.1', server_port)

server_sock = None
client_sock = None
reciever = ""
message_to_send = ""

def initUser():

    global selfUsername
    global server_sock

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    username = input("Input your username to enter to the chat: ")
    selfUsername = username
    data = {"username": selfUsername, "messageType": "Login"}
    message = pickle.dumps(data);
    server_sock.sendto(message, connectionHostToServer)

def self_server():
    global client_sock
    global connectionSelfHost
    global peerListenerThread

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.bind(connectionSelfHost)
    peerListenerThread.start()


def client(stop):
    
    global selfUsername
    global server_sock
    global reciever
    global message_to_send

    while True:
        inp = input()
        try:
            inp = inp.strip()
            if checkIfCommand(inp):
                if inp[1:] == "show_users" or inp[1:] == "end_session":
                    data = {"username": selfUsername, "reciever": None, "messageType": inp}
                else:
                    print("\nERROR: Invalid Command!\n")
                    continue
            else:
                lst = inp.split(":")
                reciever = lst[0].strip()
                message_to_send = lst[1].strip()
                data = {"username": selfUsername, "reciever": reciever, "messageType": "RecieverPortRequest"}
            
            message = pickle.dumps(data)
            server_sock.sendto(message, connectionHostToServer)
            handleMessage(inp)
        except IndexError:
            print("\nERROR: Invalid Format!\n")
        except:
            print("\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")

        if stop():
            break

def serverListener(stop):

    global server_sock
    global client_sock

    while True:
        data, address = server_sock.recvfrom(MAX_BYTES)
        processMessage(data)

        if stop():
            break

def peerListener(stop):

    global client_sock

    while True:
        data, address = client_sock.recvfrom(MAX_BYTES)
        processMessage(data)

        if stop():
            break


def processMessage(data):

    global server_sock
    global client_sock
    global connectionHostToPeer
    global connectionSelfHost

    obj = pickle.loads(data)

    try:    
        if obj["messageType"] == "Auth":
            processMessageAuth(obj)
                
        if obj["messageType"] == "RecieverPort":
            processMessageRecieverPort(obj)

        if obj["messageType"] == "Message":
            displayMessage(obj)
    except:
        displayExcpetionMessage(obj)


def processMessageAuth(obj):
    global connectionSelfHost

    lst = list(connectionSelfHost)
    lst[1] = int(obj["message"])
    connectionSelfHost = tuple(lst)
    self_server()

def processMessageRecieverPort(obj):
    global connectionHostToPeer

    new_obj = {"username": selfUsername, "message": message_to_send, "messageType": "Message"}
    message = pickle.dumps(new_obj)
    lst = list(connectionHostToPeer)
    lst[1] = int(obj["message"])
    connectionHostToPeer = tuple(lst)
    client_sock.sendto(message, connectionHostToPeer)

def displayMessage(obj):
    print(">>> " + obj["username"] + ": " + obj["message"])

def displayExcpetionMessage(obj):
    print("--------> Exception")
    print("--------> OnException Message -----> " + str(obj))

def logMessage(obj, func_name):
    print("[LOG] Message From --> " + str(func_name))
    print("[LOG] [TIME] >>> " + obj)

def checkIfCommand(message):
    if message[0] == ":":
        return True
    return False

def handleMessage(message):
    global clientListenerThread
    global clientThread
    global stop_threads

    if message == ":end_session":
        stop_threads = True
        serverListenerThread.join()
        peerListenerThread.start()
        clientThread.join()
        # sock.close()
        sys.exit()

serverListenerThread = None
peerListenerThread = None
clientThread = None
stop_threads = False

if __name__ == '__main__':
    initUser();
    stop_threads = False
    try:
        serverListenerThread = threading.Thread(target=serverListener, args =(lambda : stop_threads, ))
        peerListenerThread = threading.Thread(target=peerListener, args =(lambda : stop_threads, ))
        clientThread = threading.Thread(target=client, args =(lambda : stop_threads, ))

        serverListenerThread.start()
        clientThread.start()
    except:
        print ("Error: unable to start thread")