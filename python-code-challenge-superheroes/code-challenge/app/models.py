from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)

    powers =db.relationship('Power', secondary='hero_powers')

    def serialize(self):
        serial_powers = [power.serialize() for power in self.powers]
        return {
            'ID': self.id,
            'Name': self.name,
            'Super name': self.super_name,
            'Powers': serial_powers
        }

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String, nullable=False)

    heroes = db.relationship('Hero', secondary='hero_powers')

    def serialize(self):
        return {
            'ID': self.id,
            'Name': self.name,
            'Description': self.description
        }
    
    @validates('description')
    def validates_description(self, key, description):
        if len(description) < 20:
            raise ValueError('Invalid: Description must be atleast 20 characters')
        return description

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    hero =  db.relationship('Hero')
    power = db.relationship('Power')

    def serialize(self):
        return self.hero.serialize()
    
    @validates('strength')
    def validate_strength(self, key, strength):
        allowed_strength = ['Strong', 'Weak', 'Average']
        if strength not in allowed_strength:
            raise ValueError(f"{key} must be one of: {', '.join(allowed_strength)}")
        return strength

