from flask import Flask, request, json, Response, abort, jsonify
from pymongo import MongoClient
from bson import ObjectId
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import datetime
import re


print("connecting database...")
client = MongoClient(host='db')
print("connection established with Mongo")


class MongoAPI:
    def __init__(self, document):
        cursor = client["polls"]
        self.collection = cursor[document]

    def read(self):
        documents = self.collection.find()
        output = [{item: str(data[item]) for item in data} for data in documents]
        return output

    def find_byid(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def write(self, data):
        new_document = data
        new_document["CreatedDate"] = datetime.datetime.today()
        result = self.collection.insert_one(new_document)
        return str(result.inserted_id)


app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'key-for-jwt'


@app.route('/registration')
def registration():
    data = request.json
    users = MongoAPI('users').read()

    user_list = [user['user'] for user in users]

    if data['user'] in user_list:
        return abort(404, description='Error: User already exists')
    else:
        res = MongoAPI("users").write(data)
        return Response(response=json.dumps(res), status=200, mimetype='application/json')


@app.route('/login', methods=['POST'])
def login():
    data = request.json

    if 'user' not in data or 'passw' not in data:
        abort(400, description='Error: Must provide username and password for login')

    username = data['user']
    password = data['passw']

    users = MongoAPI('users').read()

    for user in users:
        if user['user'] == username and user['passw'] == password:
            access_token = create_access_token(identity=username)
            return jsonify(message='Login OK', access_token=access_token)
    return jsonify(message='incorrect user or password')


@app.route('/')
def base():
    return "status:up"


@app.route('/addAnswer')
@jwt_required()
@limiter.limit('1 per second')
def answers_post():
    data = request.json

    if 'poll_id' in data and 'answer' in data:
        if data['answer'] != '':
            polls = MongoAPI("polls").read()
            polls_ids = [poll['_id'] for poll in polls]
            if data['poll_id'] not in polls_ids:
                return abort(400, description='Error: There is no poll with id {}'.format(data['poll_id']))
            res = MongoAPI("answers").write(data)
            return Response(response=json.dumps(res), status=200, mimetype='application/json')
        else:
            return abort(400, description='Error: Answer cannot be left blank')
    else:
        return abort(400, description='Error: Answer has an incorrect format')


@app.route('/addPoll')
@jwt_required()
@limiter.limit('1 per second')
def polls_post():
    data = request.json
    if 'question' in data:
        pattern = '\\¿(.*?)\\?'
        substring = re.search(pattern, data['question'])
        if substring is not None:
            res = MongoAPI("polls").write(data)
            return Response(response=json.dumps(res), status=200, mimetype='application/json')
        else:
            return abort(400, description='Error: Question has an incorrect format')
    else:
        return abort(400, description='Error: Question has an incorrect format')


@app.route('/getPolls')
@jwt_required()
@limiter.limit('1 per second')
def polls_get():
    polls = MongoAPI("polls").read()
    answers = MongoAPI("answers").read()
    for poll in polls:
        poll['answers'] = [answer for answer in answers if answer['poll_id'] == poll['_id']]
    return Response(response=json.dumps(polls))


if __name__ == "__main__":
    print('up')
    app.run(host='0.0.0.0', debug=True)
