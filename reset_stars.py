from app import app, db, Car

with app.app_context():
    cars = Car.query.all()
    for car in cars:
        car.stars = 0
    db.session.commit()
    print(f"Reset stars for {len(cars)} cars to 0")