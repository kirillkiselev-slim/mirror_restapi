from datetime import datetime, date, timedelta

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_number = db.Column(db.Integer, nullable=False)
    pet_name = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    walk_time = db.Column(db.DateTime, nullable=False)
    walker = db.Column(db.String(10), nullable=False)

    def __str__(self):
        return f'<Order {self.apartment_number}, {self.pet_name}>'


with app.app_context():
    db.create_all()


@app.route('/orders/<string:date>', methods=['GET'])
def get_orders(date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    orders = Order.query.filter(
        db.func.date(Order.walk_time) == date_obj).all()
    result = [
        {
            'apartment_number': order.apartment_number,
            'pet_name': order.pet_name,
            'breed': order.breed,
            'walk_time': order.walk_time.strftime('%Y-%m-%d %H:%M'),
            'walker': order.walker
        } for order in orders
    ]
    return jsonify(result)


@app.route('/order', methods=('POST',))
def create_order():
    if not request.is_json:
        return (jsonify({'error': 'Content-Type must be application/json'}),
                415)
    today_date = datetime.today()

    data = request.get_json()

    required_fields = ('apartment_number', 'pet_name', 'breed', 'walk_time',
                       'walker')
    apt_number = data['apartment_number']
    walker = data['walker']
    breed = data['breed']
    pet_name = data['pet_name']

    if not isinstance(data, dict):
        return jsonify({'error': 'Needs to be dictionaries.'}), 400

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields.'}), 400

    if not all(isinstance(field, str) for field in (walker, breed, pet_name)):
        return jsonify({'error': 'walker, breed, pet_name'
                                 ' must be strings'}), 400

    if not isinstance(apt_number, int) or apt_number <= 0:
        return jsonify({'error': 'Apartment number cannot be'
                                 ' less or equal to zero.'}), 400
    try:
        walk_time = datetime.strptime(data['walk_time'], '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid datetime format.'
                                 ' Use YYYY-MM-DD HH:MM.'}), 400

    if walk_time < today_date:
        return jsonify({'error': 'Cannot book in the past.'}), 400
    # print(walk_time.hour)
    if (walk_time.hour < 7 or walk_time.hour >= 23 or
            (walk_time.minute not in {0, 30})):
        return jsonify({'error': 'Invalid walk time.'
                                 ' Allowed time: 07:00-23:30, '
                                 'every 30 minutes.'}), 400

    if walker.lower() not in {'petr', 'anton'}:
        return jsonify({'error': 'Only Anton or Petr can be dog walkers.'
                                 ' You can use letter "e" in петр'}), 400

    time = db.func.strftime(
            '%H:%M', Order.walk_time)
    pet_is_taken = Order.query.filter(
        db.func.date(Order.walk_time) == walk_time.date(),
        Order.pet_name == pet_name,
        time == walk_time.strftime('%H:%M')
    ).first()

    if pet_is_taken:
        return jsonify({'error': 'This pet is already taken at that time.'}), 400

    dog_walker_taken = Order.query.filter(
        db.func.date(Order.walk_time) == walk_time.date(),
        Order.walker == walker,
        time == walk_time.strftime('%H:%M')
    ).first()

    if dog_walker_taken:
        return jsonify({'error': 'This dog walker is already taken'
                                 ' at that time.'}), 400

    new_order = Order(
        apartment_number=apt_number,
        pet_name=pet_name,
        breed=breed,
        walk_time=walk_time,
        walker=walker
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order created successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)

