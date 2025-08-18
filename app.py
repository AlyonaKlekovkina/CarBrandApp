from flask import Flask, render_template

app = Flask(__name__)

# Sample data: List of car brands
cars = [
    {'name': 'Toyota', 'image': 'images/toyota.png'},
    {'name': 'BMW', 'image': 'images/bmw.png'},
    # Add more car brands here
]

@app.route('/')
def home():
    return render_template('index.html', cars=cars)

if __name__ == '__main__':
    app.run(debug=True)
