#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "Home page": "Welcome to the SuperHeroes page",
        }
        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response

api.add_resource(Home, '/')

class Heroes(Resource):

    # GET all heroes
    def get(self):
        heroes = Hero.query.all()
        serialized_heroes = [hero.serialize() for hero in heroes]
        response = make_response(
            jsonify(serialized_heroes), 
            200,
        )
        return response
    
    # POST new hero
    def post(self):
        try:
            data = request.get_json()
            new_hero = Hero(
                name=data['name'],
                alias=data['alias']
            )

            db.session.add(new_hero)
            db.session.commit()

            response_dict = {'Message': 'Hero created successfully', 'Data': new_hero.serialize()}
            response = make_response(
                jsonify(response_dict), 
                201,
            )
            return response
        
        except Exception as e:
            response_dict = {'Error': str(e)}
            return make_response(jsonify(response_dict), 400)
        
api.add_resource(Heroes, '/heroes')



class HeroesById(Resource):

    # GET specific Heroes
    def get(self, id):
        hero = Hero.query.get(id)

        if hero:
            response = make_response(
                jsonify(hero), 
                200,
            )
            return response
        else:
            response_dict = {'Error': 'Hero not found'}
            return make_response(jsonify(response_dict), 404)
        
api.add_resource(HeroesById, '/heroes/<int:id>')


class Powers(Resource):

    # GET all powers
    def get(self):
        powers = Power.query.all()
        serialized_powers = [power.serialize() for power in powers]
        response = make_response(
            jsonify(serialized_powers), 
            200,
        )
        return response
    
    # POST new Power
    def post(self):
        try:
            data = request.get_json()
            new_power = Power(
                name=data['name'],
                description=data['description']
            )

            db.session.add(new_power)
            db.session.commit()
            response_dict = {'Message': 'Power created successfully', 'Data': new_power.serialize()}
            return make_response(jsonify(response_dict), 201)
        
        except Exception as e:
            response_dict = {'Error': str(e)}
            return make_response(jsonify(response_dict), 400)
        
api.add_resource(Powers, '/powers')

class PowerById(Resource):

    # GET specific powers
    def get(self, id):
        power = Power.query.get(id)
        if power:
            response = make_response(
                jsonify(power), 
                200,
            )
            return response
        
        else:
            response_dict = {'Error': 'Power not found'}
            return make_response(jsonify(response_dict), 404)
    
    # PATCH a power
    def patch(self, id):
        try:
            data = request.get_json()
            power = Power.query.get(id)

            # if power does not exist
            if power is None:
                response_dict = {"errors": 'Power not found'}
                return make_response(jsonify(response_dict), 404)

            if 'description' in data:
                new_description = data['description']
                if not new_description:
                    response_dict = {'errors': ['Description already exists']}
                    return make_response(jsonify(response_dict), 400)

                if len(new_description) < 20:
                    response_dict = {'errors': ['Not enough characters minimum of 20']}
                    return make_response(jsonify(response_dict), 400)

                power.description = new_description
                db.session.commit()
                response_dict = {'message': 'Power updated successfully', 'data': power.serialize()}
                return make_response(jsonify(response_dict), 200)

            else:
                response_dict = {"errors": ["validation errors"]}
                return make_response(jsonify(response_dict), 400)

        except ValueError as e:
            response_dict = {'errors': [str(e)]}
            return make_response(jsonify(response_dict), 400)
        
api.add_resource(PowerById, '/powers/<int:id>')



class HeroPower(Resource):

    # POST new HeroPower
    def post(self):
        try:
            data = request.get_json()
            strength = data.get('strength')
            power_id = data.get('power_id')
            hero_id = data.get('hero_id')

            power = Power.query.get(power_id)
            hero = Hero.query.get(hero_id)

            if not (power and hero):
                response_dict = {'errors': ["validation errors"]}
                return make_response(jsonify(response_dict), 400)

            hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
            db.session.add(hero_power)
            db.session.commit()

            response_dict = {'message': 'HeroPower created successfully', 'data': hero.serialize()}
            return make_response(jsonify(response_dict), 201)

        except Exception as e:
            response_dict = {'errors': [str(e)]}
            return make_response(jsonify(response_dict), 400)

api.add_resource(HeroPower, '/hero_powers')


if __name__ == '__main__':
    app.run(port=5555)
