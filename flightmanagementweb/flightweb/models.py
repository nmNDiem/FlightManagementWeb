
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean, Enum, BigInteger
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flightweb import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin


class UserRole(RoleEnum):
    ADMIN = 1,
    EMPLOYEE = 2,
    CUSTOMER = 3


class Airport(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    sign = Column(String(3), nullable=False)
    name = Column(String(50), nullable=False)
    address = Column(String(100), unique=True, nullable=False)
    longitude = Column(Float)
    latitude = Column(Float)
    flight_routes_departure = relationship('FlightRoute', foreign_keys='[FlightRoute.departure_airport_id]',
                                           back_populates='departure_airport')
    flight_routes_destination = relationship('FlightRoute', foreign_keys='[FlightRoute.destination_airport_id]',
                                             back_populates='destination_airport')
    stop_points = relationship('StopPoint', backref='airport', lazy=True)

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
    name = Column(String(30), nullable=False)
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
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    aircraft_license_plate = Column(String(7))
    seats_1 = Column(Integer)
    seats_2 = Column(Integer)
    seats = relationship('Seat', backref='plane', cascade='all, delete-orphan', lazy=True)
    flights = relationship('Flight', backref='plane', lazy=True)

    def __str__(self):
        return self.aircraft_license_plate


class SeatType(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(10), nullable=False)
    seats = relationship('Seat', backref='seat_type', lazy=True)

    def __str__(self):
        return self.name


class Seat(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(3), nullable=False)
    seat_type_id = Column(Integer, ForeignKey(SeatType.id), nullable=False)
    plane_id = Column(Integer, ForeignKey(Plane.id), nullable=False)
    ticket = relationship('Ticket', backref='seat', uselist=False, lazy=True)

    def __str__(self):
        return self.name


class Flight(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    flight_route_id = Column(Integer, ForeignKey(FlightRoute.id), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    destination_time = Column(DateTime, nullable=False)
    duration = Column(Float, nullable=False)
    plane_id = Column(Integer, ForeignKey(Plane.id), nullable=False)
    price_seat1 = Column(Float)
    price_seat2 = Column(Float)
    stop_points = relationship('StopPoint', backref='flight', lazy=True)
    tickets = relationship('Ticket', backref='flight', lazy=True)

    def __str__(self):
        return self.name


class StopPoint(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(30))
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    stop_duration = Column(Integer, nullable=False)
    stop_order = Column(Integer, nullable=False)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(35), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.CUSTOMER)


class Admin(User):
    statistical_reports = relationship('StatisticalReport', backref='admin', lazy=True)

    def __str__(self):
        return self.name


class Employee(User):
    phone_number = Column(String(10), nullable=False)
    CCCD = Column(String(12), nullable=False)
    birthday = Column(DateTime, nullable=False)
    gender = Column(Boolean, nullable=False)
    tickets = relationship('Ticket', backref='employee', lazy=True)

    def __str__(self):
        return self.name


class Customer(User):
    phone_number = Column(String(10))
    birthday = Column(DateTime)
    gender = Column(Boolean, nullable=True)
    receipts = relationship('Receipt', backref='customer', lazy=True)

    def __str__(self):
        return self.name


class StatisticalReport(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(30), nullable=False)
    statistical_date = Column(DateTime, default=datetime.now(), nullable=False)
    link_statistical = Column(Integer)
    admin_id = Column(Integer, ForeignKey(Admin.id), nullable=False)

    def __str__(self):
        return self.name


class Passenger(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(30), nullable=False)
    birthday = Column(DateTime, nullable=False)
    gender = Column(Boolean, nullable=False)
    CCCD = Column(String(12), nullable=False)
    phone_number = Column(String(10), nullable=False)
    email = Column(String(35), nullable=False)
    tickets = relationship('Ticket', backref='passenger', lazy=True)

    def __str__(self):
        return self.name


class Ticket(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    seat_id = Column(Integer, ForeignKey(Seat.id), unique=True, nullable=False)
    passenger_id = Column(Integer, ForeignKey(Passenger.id))
    employee_id = Column(Integer, ForeignKey(Employee.id))
    note = Column(String(200))
    receipt_details = relationship('ReceiptDetails', backref='ticket', lazy=True)


class Receipt(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    booking_time = Column(DateTime, default=datetime.now(), nullable=False)
    payment_time = Column(DateTime)
    payment_method = Column(String(30), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Integer, default=0)
    ticket_id = Column(Integer, ForeignKey(Ticket.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import json
        # with open('data/airports.json', encoding='utf-8') as f1:
        #     airports = json.load(f1)
        #     for a in airports:
        #         ap = Airport(**a)
        #         db.session.add(ap)
        # db.session.commit()
        #
        # with open('data/flightRouteTypes.json', encoding='utf-8') as f2:
        #     flight_route_types = json.load(f2)
        #     for f in flight_route_types:
        #         frt = FlightRouteType(**f)
        #         db.session.add(frt)
        # db.session.commit()
        #
        # with open('data/flightRoutes.json', encoding='utf-8') as f3:
        #     flight_routes = json.load(f3)
        #     for f in flight_routes:
        #         fr = FlightRoute(**f)
        #         db.session.add(fr)
        # db.session.commit()
        #
        # with open('data/planes.json', encoding='utf-8') as f4:
        #     planes = json.load(f4)
        #     for p in planes:
        #         pl = Plane(**p)
        #         db.session.add(pl)
        # db.session.commit()
        #
        # with open('data/seatTypes.json', encoding='utf-8') as f5:
        #     seatTypes = json.load(f5)
        #     for s in seatTypes:
        #         st = SeatType(**s)
        #         db.session.add(st)
        # db.session.commit()
        #
        # with open('data/seats.json', encoding='utf-8') as f6:
        #     seats = json.load(f6)
        #     for s in seats:
        #         se = Seat(**s)
        #         db.session.add(se)
        # db.session.commit()
        #
        # with open('data/flights.json', encoding='utf-8') as f7:
        #     flights = json.load(f7)
        #     for f in flights:
        #         fl = Flight(**f)
        #         db.session.add(fl)
        # db.session.commit()

        # with open('data/tickets.json', encoding='utf-8') as f8:
        #     tickets = json.load(f8)
        #     for t in tickets:
        #         tk = Ticket(**t)
        #         db.session.add(tk)
        # db.session.commit()



        # import hashlib
        # from datetime import datetime
        #
        # # Create an Admin user
        # admin = Admin(
        #     id=1,
        #     name='Admin User',
        #     username='admin',
        #     avatar='https://i.pinimg.com/236x/5f/40/6a/5f406ab25e8942cbe0da6485afd26b71.jpg',
        #     password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
        #     email='admin@example.com',
        #     user_role=UserRole.ADMIN
        # )
        #
        # # Create an Employee user
        # employee = Employee(
        #     id=2,
        #     name='Employee User',
        #     username='employee',
        #     avatar='https://i.pinimg.com/564x/c5/7f/8a/c57f8ab01f88c9ac40b4724179fc1c54.jpg',
        #     password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
        #     email='employee@example.com',
        #     user_role=UserRole.EMPLOYEE,
        #     phone_number=123456789,
        #     CCCD=123456789012,
        #     birthday=datetime(1990, 1, 1),
        #     gender=True  # True for male, False for female
        # )
        #
        # # Create a Customer user
        # customer = Customer(
        #     id=4,
        #     name='Customer User',
        #     username='customer',
        #     avatar='https://i.pinimg.com/564x/5a/54/cf/5a54cfdb6320b05029b8fafb6fdb5f4e.jpg',
        #     password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
        #     email='customer@example.com',
        #     user_role=UserRole.CUSTOMER,
        #     phone_number=987654321,
        #     birthday=datetime(2003, 5, 5),
        #     gender=False  # True for male, False for female
        # )
        #
        # # Add all users to the session and commit
        # db.session.add_all([admin, employee, customer])
        # db.session.commit()

