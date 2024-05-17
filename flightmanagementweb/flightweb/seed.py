from datetime import datetime, timedelta
from flightweb import db, app
from models import Flight


def add_flights():
    with app.app_context():
        # Thông tin về các chuyến bay mới
        flights_data = [
            {'name': 'Flight 102', 'flight_route_id': 1, 'departure_time': datetime.now() + timedelta(hours=2), 'destination_time': datetime.now() + timedelta(hours=4), 'duration': 120, 'flight_schedule_id': 1},
            {'name': 'Flight 103', 'flight_route_id': 1, 'departure_time': datetime.now() + timedelta(hours=6), 'destination_time': datetime.now() + timedelta(hours=8), 'duration': 120, 'flight_schedule_id': 1},
            {'name': 'Flight 104', 'flight_route_id': 1, 'departure_time': datetime.now() + timedelta(days=1), 'destination_time': datetime.now() + timedelta(days=1, hours=2), 'duration': 120, 'flight_schedule_id': 1}
        ]

        # Thêm các chuyến bay vào cơ sở dữ liệu
        for flight_info in flights_data:
            flight = Flight(**flight_info)
            db.session.add(flight)

        db.session.commit()
        print('Added new flights to the database!')


if __name__ == '__main__':
    add_flights()
