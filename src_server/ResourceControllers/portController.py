from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from src_server.Helpers import *
from src_server.DatabaseManager import *

parser = Parser().parser
red = RedisController().red

class PortHandler(Resource):
    def post(self):
        request.get_json(force=True)
        args = parser.parse_args()
        username = str(args['username'])
        if red.get(username) != None:
            client_port = int(str(red.get(username))[2:-1])
            return jsonify(port=client_port)
        else:
            response = jsonify(dict(error='User Does not Exist'))
            response.status_code = 404
            return response