from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from flightweb import db, app


class Airport(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), unique=True, nullable=False)
    longitude = Column(Float)
    latitude = Column(Float)
    sign = Column(String(50))
    flight_routes_departure = relationship('FlightRoute', foreign_keys='[FlightRoute.departure_airport_id]',
                                           back_populates='departure_airport')
    flight_routes_destination = relationship('FlightRoute', foreign_keys='[FlightRoute.destination_airport_id]',
                                             back_populates='destination_airport')

    def __str__(self):
        return self.name


class FlightRouteType(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(String(25), nullable=False)
    flight_routes = relationship('FlightRoute', backref='flight_route_type', lazy=True)

    def __str__(self):
        return self.description


class FlightRoute(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(30))
    flight_route_type_id = Column(Integer, ForeignKey(FlightRouteType.id), nullable=False)
    departure_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    destination_airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    departure_airport = relationship('Airport', foreign_keys=[departure_airport_id],
                                     back_populates='flight_routes_departure')
    destination_airport = relationship('Airport', foreign_keys=[destination_airport_id],
                                       back_populates='flight_routes_destination')
    flights = relationship('Flight', backref='flight_route', lazy=True)

    def __str__(self):
        return self.name


class Plane(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(20))
    aircraft_license_plate = Column(String(7), nullable=False)
    seats_1 = Column(Integer)
    seats_2 = Column(Integer)
    seats = relationship('Seat', backref='plane', cascade='all, delete-orphan', lazy=True)
    flights = relationship('Flight', secondary='flight_plane', lazy='subquery',
                           backref=backref('planes_list', lazy=True))

    def __str__(self):
        return self.name


class SeatType(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(10), nullable=False)
    seats = relationship('Seat', backref='seat_type', lazy=True)

    def __str__(self):
        return self.name


class Seat(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    seat_type_id = Column(Integer, ForeignKey(SeatType.id))
    plane_id = Column(Integer, ForeignKey(Plane.id))

    def __str__(self):
        return self.id


class Flight(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    flight_route_id = Column(Integer, ForeignKey(FlightRoute.id), nullable=False)
    departure_time = Column(DateTime)
    flight_time = Column(Integer)
    planes = relationship('Plane', secondary='flight_plane', lazy='subquery',
                          backref=backref('flights_list', lazy=True))

    def __str__(self):
        return self.id


flight_plane = db.Table('flight_plane',
                        Column('flight_id', Integer, ForeignKey(Flight.id), primary_key=True),
                        Column('plane_id', Integer, ForeignKey(Plane.id), primary_key=True))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
