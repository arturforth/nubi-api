import re

from flask import Flask, request, json, Response
from flask import Flask, request, json, Response, abort
from pymongo import MongoClient
import datetime
from bson import ObjectId

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


@app.route('/')
def base():
    return "status:up"


@app.route('/addAnswer')
def answers_post():
    data = request.json

    if 'poll_id' in data and 'answer' in data:
        if data['answer'] is not '':
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
def polls_get():
    polls = MongoAPI("polls").read()
    answers = MongoAPI("answers").read()
    for poll in polls:
        poll['answers'] = [answer for answer in answers if answer['poll_id'] == poll['_id']]
    return Response(response=json.dumps(polls))


if __name__ == "__main__":
    print('up')
    app.run(host='0.0.0.0', debug=True)
