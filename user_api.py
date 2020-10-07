from flask import Flask
from flask_restful import abort, reqparse, Api, Resource


spam = Flask(__name__)
api = Api(spam)

USERS = {}

parser = reqparse.RequestParser()
parser.add_argument('name')

def abort_if_user_doesnt_exist(user_id):
    if user_id not in USERS:
        abort(404, message=f'User {user_id} doesn\'t exist')


class User(Resource):
    def get(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        return USERS[user_id]

    def put(self, user_id):
        args = parser.parse_args()
        USERS[user_id] = args['name']
        return args['name'], 201

    def delete(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        USERS.pop(user_id)
        return '', 204


class UserList(Resource):
    def get(self):
        return USERS

    def post(self):
        args = parser.parse_args()
        user_id = int(max(USERS.keys() or ['user0']).lstrip('user')) + 1
        user_id = f'user{user_id}'
        USERS[user_id] = args['name']

        return USERS[user_id], 201


api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')
