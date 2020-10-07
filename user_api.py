import json

from flask import Flask
from flask_restful import abort, reqparse, Api, Resource


spam = Flask(__name__)
api = Api(spam)

parser = reqparse.RequestParser()
parser.add_argument('name')

def load_json():
    with open('storage.json') as json_file:
        USERS = json.load(json_file) or {}
        return USERS

def dump_json(USERS):
    with open('storage.json', 'w') as json_file:
        json.dump(USERS, json_file)

USERS = load_json()

def abort_if_user_doesnt_exist(user_id):
    if user_id not in USERS:
        abort(404, message=f'User {user_id} doesn\'t exist')


class User(Resource):
    def get(self, user_id):
        USERS = load_json()
        abort_if_user_doesnt_exist(user_id)
        return USERS[user_id]

    def put(self, user_id):
        USERS = load_json()
        abort_if_user_doesnt_exist(user_id)
        args = parser.parse_args()
        USERS[user_id] = args['name']
        dump_json(USERS)
        return args['name'], 201

    def delete(self, user_id):
        USERS = load_json()
        abort_if_user_doesnt_exist(user_id)
        USERS.pop(user_id)
        dump_json(USERS)
        return '', 204


class UserList(Resource):
    def get(self):
        USERS = load_json()
        return USERS

    def post(self):
        USERS = load_json()
        args = parser.parse_args()
        user_id = int(max(USERS.keys() or ['user0']).lstrip('user')) + 1
        user_id = f'user{user_id}'
        USERS[user_id] = args['name']
        dump_json(USERS)
        return USERS[user_id], 201


api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')
