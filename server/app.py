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
    return jsonify([{'id': bakery.id, 'name': bakery.name} for bakery in bakeries])

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    baked_goods = [{'id': bg.id, 'name': bg.name, 'price': bg.price} for bg in bakery.baked_goods]
    return jsonify({'id': bakery.id, 'name': bakery.name, 'baked_goods': baked_goods})

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([{'id': bg.id, 'name': bg.name, 'price': bg.price, 'bakery_id': bg.bakery_id} for bg in baked_goods])

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return jsonify({'id': most_expensive.id, 'name': most_expensive.name, 'price': most_expensive.price, 'bakery_id': most_expensive.bakery_id})
    return jsonify({'error': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
