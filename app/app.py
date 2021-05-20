# compose_flask/app.py
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask import jsonify
import json
import logging

config = {
    'host' : 'db',
    'port' : '3306',
    'user' : 'root',
    'password' : 'root',
    'database' : 'classicmodels',
}
app = Flask(__name__)

db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

# connection_str = 'mysql+pymysql://{db_user}:{db_pwd}@db:3306/{db_name}'
connection_str = 'mysql+pymysql://root:root@db:3306/classicmodels'
engine = create_engine(connection_str)
connection = engine.connect()
metadata = MetaData(bind=engine)
metadata.reflect(only=['customers','employees','offices', 'orderdetails','orders','payments','productlines','products'])

Session = sessionmaker(bind=engine)

Base = automap_base()
Base.prepare(engine, reflect=True)

Customer = Base.classes.customers
Employee = Base.classes.employees
Offices = Base.classes.offices
OrderDetail = Base.classes.orderdetails
Order = Base.classes.orders
Payment = Base.classes.payments
ProductLine = Base.classes.productlines
Product = Base.classes.products

def print_table():
    tab=[]
    logging.info(' - - - ✅ Tables into database - - - \n')
    for t in metadata.sorted_tables:
        print("\t\t - {}".format(t.name))
        tab.append(t.name)
    return tab 

@app.route('/connection_db')
def index():
    return ' - - - MYSQL Database `classicmodels` connection ok - - - '

@app.route('/')
def hello():
    session = Session()
    result = []
    for instance in session.query(Customer).order_by(Customer.customerNumber):
        print(instance.customerName)
        result.append(instance.customerName)

    return jsonify(result)

@app.route('/tables')
def tables() -> str:
    return json.dumps({'Tables ': print_table()})

def check_if_null_to_str(value):
    value = value if value is not None else ''
    return value

# Préparez une liste de buraeaux triés par pays, état, ville.
@app.route('/1')
def offices():
    session = Session()
    result = []
    qs = session.query(Offices).order_by(Offices.country)
    for instance in qs:
        # logging.error(instance)
        country = check_if_null_to_str(instance.country)
        state = check_if_null_to_str(instance.state)
        city = check_if_null_to_str(instance.city)
        office = {
                  'country': country,
                  'state': state, 
                  'city': city
                  }
        result.append(office)

    return jsonify(result)

# Combien d'employés y a-t-il dans l'entreprise
@app.route('/2')
def all_employes():
    session = Session()
    employees = {}
    qs = session.query(Employee).all()
    employees= {'employes_qt' : len(qs)}
    return jsonify(employees)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

