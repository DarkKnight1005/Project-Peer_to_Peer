from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource

class Parser:
    
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('message', type=str)
        self.parser.add_argument('reciever', type=str)