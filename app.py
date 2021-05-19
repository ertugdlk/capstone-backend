import datetime
import json

from flask import Flask, jsonify, Response
import psycopg2
import repository
import decimal

app = Flask(__name__)
conn = psycopg2.connect(user='root', password='Capstone2021', port=5432,
                        host='capstone.csmts1kw9sus.eu-central-1.rds.amazonaws.com',
                        database='capstone')
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/videorecords')
def videoRecords():
    sql = repository.VideoSqlOperations()
    result = sql.retrieveUploadedVideo()
    jsontype = result.to_json()
    return json.loads(jsontype)

if __name__ == '__main__':
    app.run()

