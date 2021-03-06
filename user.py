from flask_restful import Resource
from flask_restful import Resource, Api, reqparse
from models.user import UserModel

import sqlite3

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument(
		'username',
		type=str,
		required=True,
		help="This field cannot be left blank!"		
	)
	parser.add_argument(
		'password',
		type=str,
		required=True,
		help="This field cannot be left blank!"		
	)

	def post(self):
		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {'message':"A user with name '{}' already exists".format(data['username'])}, 400

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()	

		query = "INSERT INTO users VALUES (NULL, ?, ?)"
		cursor.execute(query, (data['username'], data['password']))

		connection.commit()
		connection.close()

		return {'message':'User created successfully.'}, 201
		