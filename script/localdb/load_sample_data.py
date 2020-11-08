"""Creates sample data for 2 products at 2 stores"""
from sharedmodels.db import get_session_scope
from sharedmodels.models import (
    Product
)
import json,os


def get_json_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, 'products.json')
    with open(path) as json_file:
        data = json.load(json_file)
    return data


def parse_product_attributes(product):
    attributes = {
        'name': product['name'],
        'brand': product['brand'],
        'price': product['price'],
        'in_stock_quantity': product['in_stock_quantity']
    }
    return attributes


def save_product(session, product):
    attributes = parse_product_attributes(product)
    Product.create_or_update(session, product['id'], **attributes)


with get_session_scope() as session:
    products = get_json_data()
    for product in products:
        save_product(session, product)
    session.commit()
    session.close()
