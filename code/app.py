from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = "suara"
api = Api(app)

jwt = JWT(app, authenticate, identity) # create new endpoint /auth

