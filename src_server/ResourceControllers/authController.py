from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from src_server.Helpers import *
from src_server.DatabaseManager import *

parser = Parser().parser
red = RedisController().red

class Auth(Resource):
    def post(self):
        request.get_json(force=True)
        args = parser.parse_args()
        username = str(args['username'])  
        if red.get(username) == None:
            client_port = int(str(red.get('next_client_port'))[2:-1])
            red.set(username, client_port)
            red.set("next_client_port", client_port + 1)
            return jsonify(port=client_port)
        else:
            response = jsonify(dict(error='User Already Logged In'))
            response.status_code = 409
            return response
