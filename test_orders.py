import pytest
from app import OrderService
import sqlite3
import json

def test_insert_order():
    order = [{'block_position': 'top', 'extensions': ['$300 off $3,000+'], 'extracted_price': 1999.99, 'link': 'https://www.havertys.com/products/product-page/martin-s-landing-executive-desk#0-4000-2975', 'position': 1, 'price': '$1,999.99', 'source': 'Havertys Furniture', 'thumbnail': 'https://serpapi.com/searches/63bf5f19ada54b8fed5bf9c0/images/130b9773f91aaef775a93b4eeed3424742a297f06776cf7db5a65ca50d6787db.png', 'title': 'Havertys Martin Landing Executive Desk in Cherry | Wood'}, {'block_position': 'top', 'extracted_price': 1079, 'link': 'https://www.belson.com/E-Series-Steel-Picnic-Table-Square?utm_source=google&utm_medium=cpc&utm_campaign=SHOPPING%20-%20All&utm_keyword=358-EV', 'position': 1, 'price': '$1,079.00', 'source': 'Belson Outdoors', 'thumbnail': 'https://serpapi.com/searches/63bf5f27272aa5200b23eb95/images/d1d3811ef04e8ac3d03ff397e82c476066c1f354718f54b99d1fec16c77dcf02.png', 'title': 'E Series 46" Square Steel Commercial Commercial Picnic Table Diamond Pattern | Belson Outdoors - Model 358-EV'}]
    os = OrderService()
    order_id = os.insert_order(order)
    conn = sqlite3.connect('shoppingDB.db', check_same_thread=False)
    cursor = conn.cursor()
    res = cursor.execute(f"select * from orders where order_id = '{order_id}'")
    order_res = res.fetchone()
    if order_res[0] != order_id:
        assert False
    order_res = json.loads(order_res[1])
    for idx, item in enumerate(order):
        if item['link'] != order_res[idx]['link']:
            assert False
    assert True