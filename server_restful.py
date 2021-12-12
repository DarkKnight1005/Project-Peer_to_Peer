import socket
import datetime
import time
import pickle
import threading
import redis
from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from src_server import *

app = Flask(__name__)
api = Api(app)
endpointBuilder = EnpointBuilder()
globalConsts = GlobalConsts()
mainConfiguration = MainConfiguration()

mainConfiguration.configureApp();

api.add_resource(Auth, endpointBuilder.addParam("auth").build())
api.add_resource(PortHandler, endpointBuilder.addParam("recieverPort").build())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=globalConsts.server_port ,debug=True)