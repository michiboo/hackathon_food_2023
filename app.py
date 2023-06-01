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
    emission_value = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    
class Consumption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

class Municipality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    emissions = db.relationship('Emission', backref='municipality', lazy=True)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    emissions = db.relationship('Emission', backref='user', lazy=True)



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

@app.route('/consumption/<userid>', methods=['GET'])
def get_previous_menu(userid):
    menu_data = Consumption.query.filter_by(user_id=userid).all()
    output = []
    for menu in menu_data:
        menu_data = {}
        menu_data['menu_id'] = menu.menu_id
        menu_data['user_id'] = menu.user_id
        menu_data['date'] = menu.date
        output.append(menu_data)
    return jsonify({'menu_data': output})    

@app.route('/consumption', methods=['POST'])
def add_consumption():
    data = request.get_json()
    menu_id = data['menu_id']
    user_id = data['user_id']
    date = data['date']
    new_consumption = Consumption(menu_id=menu_id, user_id=user_id, date=date)
    db.session.add(new_consumption)
    db.session.commit()

    return jsonify({'message': 'Consumption added successfully'})
    

@app.route('/emission', methods=['POST'])
def add_emission():
    data = request.get_json()
    userid = data['userid']
    restaurant_id = data['restaurant_id']
    meal_name = data['meal_name']
    emission_value = data['emission_value']
    date = data['date']
    new_emission = Consumption(userid=userid, restaurant_id=restaurant_id, meal_name=meal_name, emission_value=emission_value, date=date)
    db.session.add(new_emission)
    db.session.commit()

    return jsonify({'message': 'Emission added successfully'})


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
    app.run(debug=True, port=5000)