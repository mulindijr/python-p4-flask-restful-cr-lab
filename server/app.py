#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.serialize() for plant in plants])

    def post(self):
        data = request.get_json()
        new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(new_plant)
        db.session.commit()
        response = make_response(jsonify(new_plant.serialize()), 201)
        response.headers['Location'] = f'/plants/{new_plant.id}'
        return response

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant:
            return jsonify(plant.serialize())
        else:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

    def put(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        data = request.get_json()
        plant.name = data['name']
        plant.image = data['image']
        plant.price = data['price']

        db.session.commit()

        return jsonify(plant.serialize())

    def delete(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        db.session.delete(plant)
        db.session.commit()

        return make_response(jsonify({'message': 'Plant deleted successfully'}), 200)

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)