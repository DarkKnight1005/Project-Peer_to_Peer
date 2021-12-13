import socket
import datetime
import time
import pickle
import threading
import sys
from src import *
import aiohttp
import asyncio


client_sock = None

connectionData = ConnectionData()
globalConsts = GlobalConsts()
processor = Processor()

async def initUser():

    global selfUsername
    username = input("Input your username to enter to the chat: ")
    selfUsername = username
    data = {"username": selfUsername}
    async with aiohttp.ClientSession(headers={"Content-Type":"application/json"}) as session:

        authUrl = globalConsts.apiPath + "/auth"
        async with session.post(authUrl, json=data) as resp:
            selfPort = await resp.json()
            selfPort = selfPort["port"]
            processor.processMessageAuth(selfPort, connectionData, self_server)


def self_server(connectionSelfHost):
    global client_sock

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.bind(connectionSelfHost)
    peerListenerThread.start()

def peerListener(stop):

    global client_sock

    while True:
        data, address = client_sock.recvfrom(globalConsts.MAX_BYTES)
        processor.processMessage(data)

        if stop():
            break

def client_async(stop_threads):
    asyncio.run(client(stop_threads))

async def client(stop):
    
    global selfUsername
    global client_sock

    while True:
        inp = input()
        try:
            inp = inp.strip()
            lst = inp.split(":")
            reciever = lst[0].strip()
            message_to_send = lst[1].strip()
            data = {"username": reciever}
            async with aiohttp.ClientSession(headers={"Content-Type":"application/json"}) as session:
                portRequest = globalConsts.apiPath + "/recieverPort"
                async with session.post(portRequest, json=data) as resp:
                    recieverPort = await resp.json()
                    recieverPort = recieverPort["port"]
                    new_obj = {"username": selfUsername, "message": message_to_send}
                    processor.processSendMessageToPort(client_sock, connectionData, recieverPort, new_obj)
        except IndexError:
            print("\nERROR: Invalid Format!\n")
        except Exception as err:
            print("\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n" + str(err) + "\n")

        if stop():
            break


peerListenerThread = None
clientThread = None
stop_threads = False

async def main():

    global stop_threads
    global peerListenerThread
    global clientThread

    stop_threads = False
    peerListenerThread = threading.Thread(target=peerListener, args =(lambda : stop_threads, ))
    clientThread = threading.Thread(target=client_async, args =(lambda : stop_threads, ))
    await initUser();
    try:
        clientThread.start()
    except:
        print ("Error: unable to start thread")

asyncio.run(main())