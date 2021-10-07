import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This filed cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='This filed cannot be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that name already exists"}, 400

        user = UserModel(**data)  # unpacking dict and pass it for each of the keys in data , username = value,
        # password = value, it will always have username and password ( same as (data['username'], data ['password']))
        user.save_to_db()

        return {"message": "User created successfully"}, 201
