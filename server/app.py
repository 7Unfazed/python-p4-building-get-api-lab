#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = [{
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "updated_at": bakery.updated_at
    } for bakery in bakeries]

    return make_response(jsonify(bakeries_list), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery is None:
        return make_response(jsonify({"error": "Bakery not found"}), 404)
    
    bakery_data = {
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "updated_at": bakery.updated_at,
        "baked_goods": [{
            "id": bg.id,
            "name": bg.name,
            "price": bg.price,
            "bakery_id": bg.bakery_id,
            "created_at": bg.created_at,
            "updated_at": bg.updated_at
        } for bg in bakery.baked_goods]
    }

    return make_response(jsonify(bakery_data), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [{
        "id": bg.id,
        "name": bg.name,
        "price": bg.price,
        "created_at": bg.created_at,
        "updated_at": bg.updated_at,
        "bakery": {
            "id": bg.bakery.id if bg.bakery else None,
            "name": bg.bakery.name if bg.bakery else None,
            "created_at": bg.bakery.created_at if bg.bakery else None,
            "updated_at": bg.bakery.updated_at if bg.bakery else None
        }
    } for bg in baked_goods]

    return make_response(jsonify(baked_goods_list), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive is None:
        return make_response(jsonify({"error": "No baked goods found"}), 404)
    
    most_expensive_data = {
        "id": most_expensive.id,
        "name": most_expensive.name,
        "price": most_expensive.price,
        "created_at": most_expensive.created_at,
        "updated_at": most_expensive.updated_at,
        "bakery": {
            "id": most_expensive.bakery.id if most_expensive.bakery else None,
            "name": most_expensive.bakery.name if most_expensive.bakery else None,
            "created_at": most_expensive.bakery.created_at if most_expensive.bakery else None,
            "updated_at": most_expensive.bakery.updated_at if most_expensive.bakery else None
        }
    }

    return make_response(jsonify(most_expensive_data), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
