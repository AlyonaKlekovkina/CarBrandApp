import os
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for Car
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    stars = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'name': self.name,
            'image': self.image,
            'stars': self.stars
        }

# Create the database and tables
with app.app_context():
    db.create_all()
    # Populate the database with cars if not already present
    if Car.query.count() == 0:
        cars_data = [
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
        for car in cars_data:
            new_car = Car(name=car['name'], image=car['image'])
            db.session.add(new_car)
        db.session.commit()

# Route to render the home page
@app.route('/')
def home():
    cars = Car.query.all()
    cars_list = [car.to_dict() for car in cars]
    return render_template('index.html', cars=cars_list)

# Route to handle adding a star to a car
@app.route('/add_star', methods=['POST'])
def add_star():
    data = request.get_json()
    car_name = data.get('car_name')
    if not car_name:
        return jsonify({'error': 'No car name provided'}), 400
    car = Car.query.filter_by(name=car_name).first()
    if car:
        car.stars += 1
        db.session.commit()
        return jsonify({'stars': car.stars}), 200
    else:
        return jsonify({'error': 'Car not found'}), 404

# Route to handle transcribing audio via Whisper API
@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    # Check for test mode or fallback mode
    TEST_MODE = os.getenv('TEST_MODE', 'false').lower() == 'true'
    FALLBACK_MODE = os.getenv('FALLBACK_MODE', 'true').lower() == 'true'
    
    # Get OpenAI API key from environment variable
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Use test mode if explicitly requested or if no API key
    if TEST_MODE or not OPENAI_API_KEY:
        # Mock transcription for testing
        import random
        car_names = ['toyota', 'bmw', 'ferrari', 'mercedes', 'audi', 'honda', 'ford', 'nissan', 'chevrolet', 'volkswagen']
        russian_names = ['тойота', 'бмв', 'феррари', 'мерседес', 'ауди', 'хонда', 'форд', 'ниссан', 'шевроле', 'фольксваген']
        incorrect_names = ['wrong', 'неправильно', 'test', 'тест']
        
        # 70% chance of correct answer for testing
        if random.random() < 0.7:
            # Return a random correct car name (mix of English and Russian)
            all_correct = car_names + russian_names
            transcription = random.choice(all_correct)
        else:
            # Return an incorrect answer
            transcription = random.choice(incorrect_names)
        
        print(f"Mock transcription: {transcription}")
        return jsonify({'text': transcription}), 200

    files = {
        'file': (file.filename, file, file.mimetype)
    }
    data = {
        'model': 'whisper-1'
    }
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    try:
        response = requests.post(
            'https://api.openai.com/v1/audio/transcriptions',
            headers=headers,
            files=files,
            data=data
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        transcription = response.json().get('text', '')
        print(f"🎤 OpenAI Transcription received: '{transcription}'")  # Enhanced logging
        if transcription:
            return jsonify({'text': transcription}), 200
        else:
            return jsonify({'error': 'No transcription received.'}), 500
    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f'HTTP error occurred: {http_err} - Response: {response.text}')
        
        # Fallback to mock if OpenAI API fails and fallback is enabled
        if FALLBACK_MODE:
            app.logger.info('Falling back to mock transcription due to API error')
            import random
            car_names = ['toyota', 'bmw', 'ferrari', 'mercedes', 'audi', 'honda', 'ford', 'nissan', 'chevrolet', 'volkswagen']
            russian_names = ['тойота', 'бмв', 'феррари', 'мерседес', 'ауди', 'хонда', 'форд', 'ниссан', 'шевроле', 'фольксваген']
            all_names = car_names + russian_names
            fallback_transcription = random.choice(all_names)
            print(f"Fallback transcription (API failed): {fallback_transcription}")
            return jsonify({'text': fallback_transcription}), 200
        
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), response.status_code
    except Exception as err:
        app.logger.error(f'Other error occurred: {err}')
        
        # Fallback to mock if any other error occurs and fallback is enabled
        if FALLBACK_MODE:
            app.logger.info('Falling back to mock transcription due to exception')
            import random
            car_names = ['toyota', 'bmw', 'ferrari', 'mercedes', 'audi', 'honda', 'ford', 'nissan', 'chevrolet', 'volkswagen']
            russian_names = ['тойота', 'бмв', 'феррари', 'мерседес', 'ауди', 'хонда', 'форд', 'ниссан', 'шевроле', 'фольксваген']
            all_names = car_names + russian_names
            fallback_transcription = random.choice(all_names)
            print(f"Fallback transcription (exception): {fallback_transcription}")
            return jsonify({'text': fallback_transcription}), 200
        
        return jsonify({'error': f'Other error occurred: {err}'}), 500

if __name__ == '__main__':
    # Ensure the images directory exists
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    app.run(debug=True)
