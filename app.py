import app
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
# import os
#
# @app.route('/')
# def home():
#     return render_template('index.html', cars=cars)
#
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))  # Elastic Beanstalk sets the PORT environment variable
#     app.run(host='0.0.0.0', port=port, debug=False)  # Set debug to False for production

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, default=0)

# Create the database
with app.app_context():
    db.create_all()

# Sample data: List of car brands
cars = [
    {'name': 'Toyota', 'image': 'images/toyota.png'},
    {'name': 'BMW', 'image': 'images/bmw.png'},
    {'name': 'Ferrari', 'image': 'images/ferrari.png'},
    {'name': 'Mercedes-Benz', 'image': 'images/mercedes.png'},
    {'name': 'Audi', 'image': 'images/audi.png'},
    {'name': 'Honda', 'image': 'images/honda.png'},
    {'name': 'Ford', 'image': 'images/ford.png'},
    {'name': 'Chevrolet', 'image': 'images/chevrolet.png'},
    {'name': 'Nissan', 'image': 'images/nissan.png'},
    {'name': 'Volkswagen', 'image': 'images/volkswagen.png'},
    # Add more as needed
]
@app.route('/')
def home():
    # For simplicity, use the first user (adjust as needed)
    user = UserProgress.query.first()
    if not user:
        user = UserProgress()
        db.session.add(user)
        db.session.commit()
    return render_template('index.html', cars=cars, stars=user.stars)

@app.route('/add_star', methods=['POST'])
def add_star():
    user = UserProgress.query.first()
    if user:
        user.stars += 1
        db.session.commit()
        return jsonify({'stars': user.stars}), 200
    return jsonify({'error': 'User not found'}), 404


@app.route('/dashboard')
def dashboard():
    user = UserProgress.query.first()
    if not user:
        user = UserProgress()
        db.session.add(user)
        db.session.commit()
    return render_template('dashboard.html', stars=user.stars)


if __name__ == '__main__':
    app.run(debug=True)
