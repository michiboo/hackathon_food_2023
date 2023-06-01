# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    municipality_id = db.Column(db.Integer, db.ForeignKey('municipality.id'), nullable=False)
    emissions = db.relationship('Emission', backref='restaurant', lazy=True)
    
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    
class Emission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emission_value = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Clolum(db.Date, nullable=False)

class Municipality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    emissions = db.relationship('Emission', backref='municipality', lazy=True)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    emissions = db.relationship('Emission', backref='user', lazy=True)


# @app.route('/emission/<userid>', methods=['GET'])
# def get_emission(userid):
#     data = 
# emission_data = [
#     {
#         'userid': 'user1',
#         'restaurant_id': 'restaurant1',
#         'meal_name': 'Chicken Curry',
#         'emission_value': 100,
#         'date': '2023-05-30'
#     }
# ]


@app.route("/", methods=["GET"])
def hello():
    return "hello"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({'message': 'Invalid credentials'})

    return jsonify({'message': 'Login successful'})

if __name__ == '__main__':
    app.run(debug=True)