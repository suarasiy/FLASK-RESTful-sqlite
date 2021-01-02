import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        find_query = "SELECT * FROM users WHERE username = ?"

        result = cursor.execute(find_query, (username,))
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None
        
        # connection.commit() <- we don't have to commit because didn't add any data
        connection.close()
        return user
    
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        find_query = "SELECT * FROM users WHERE id = ?"
        
        result = cursor.execute(find_query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        data_post = UserRegister.parser.parse_args()

        if User.find_by_username(data_post["username"]):
            return {"message" : "A user with that username already exist."}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(insert_query, (data_post["username"], data_post["password"]))

        connection.commit()
        connection.close()

        return {"message" : "User created successfully."}, 201