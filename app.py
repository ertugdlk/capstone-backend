from flask import Flask
import psycopg2
import repository

app = Flask(__name__)
conn = psycopg2.connect(user='root', password='Capstone2021', port=5432,
                        host='capstone.csmts1kw9sus.eu-central-1.rds.amazonaws.com',
                        database='capstone')

@app.route('/')
def hello_world():
    sql = repository.SqlOperations()
    result = sql.retrieveUploadedVideo()
    print(result)
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
