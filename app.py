from flask import Flask
from flask_cors import CORS
import requests
from flask import request
import sqlite3
import json
import uuid

app = Flask(__name__)
try:
    conn = sqlite3.connect('shoppingDB.db', check_same_thread=False)
    cursor = conn.cursor()
    print("Database created and Successfully Connected to SQLite")
    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    cursor.execute('Drop table orders')
    print("SQLite Database Version is: ", record)
    sqlite_select_Query = "CREATE TABLE orders ( order_id varchar(50) primary key, order_json json)"
    cursor.execute(sqlite_select_Query)
    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

CORS(app)

@app.route("/product")
def activity():
    product = request.args.get('product')
    params = {
        'engine': 'google',
        'q': product,
        'api_key': '429fe90a451b5bceff72f03727737047e14774b2282978950f366a7687571fd2',
    }    
    response = requests.get('https://serpapi.com/search', params=params)
    data = response.json()
    if data.get('shopping_results'):
        return {
            "shopping_results": data['shopping_results']
        }
    else:
        next_link = data.get('serpapi_pagination').get("next_link")
        response = requests.get(next_link, params={'api_key': '429fe90a451b5bceff72f03727737047e14774b2282978950f366a7687571fd2'})
        data = response.json()        
        return {
            "shopping_results": data['shopping_results']
        }

@app.route("/order", methods=['POST'])
def order():   
    order = request.json['params']['order']
    print(order)
    os = OrderService()
    order_id = os.insert_order(order)
    return {
        'order_id': order_id
    }

@app.route("/orders", methods=['GET'])
def orders():
    os = OrderService()
    orders = os.get_orders()
    return {
        'orders': orders
    }    

class OrderService:
    def insert_order(self, order):
        cursor = conn.cursor()
        order_json = json.dumps(order)
        order_id = str(uuid.uuid4())
        cursor.execute(f"INSERT INTO orders (order_id, order_json) VALUES ('{order_id}', '{order_json}')")
        conn.commit()
        cursor.close()
        return order_id

    def get_orders(self):
        cursor = conn.cursor()
        res = cursor.execute("Select * from orders")        
        orders = res.fetchall()
        cursor.close()
        return orders

