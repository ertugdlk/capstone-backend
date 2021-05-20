import datetime
import json

from flask import Flask, jsonify, Response
import psycopg2
import repository
import decimal

app = Flask(__name__)
conn = psycopg2.connect(user='root', password='', port=5432,
                        host='',
                        database='capstone')

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

