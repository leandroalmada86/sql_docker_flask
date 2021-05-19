# compose_flask/app.py
from flask import Flask
# import flask_sqlalchemy
from sqlalchemy import create_engine

config = {
    'host' : 'localhost',
    'port' : '3320',
    'user' : 'newuser',
    'password' : 'newpassword',
    'database' : 'classicmodels',
}

db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('user')
db_port = config.get('host')
db_name = config.get('database')

app = Flask(__name__)

def create_app():
    connection_str = 'mysql+mysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(connection_str)
    connection = engine.connect()

@app.route('/')
def index():
    return ' - - - MYSQL Database `classicmodels` connection ok - - - '


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

