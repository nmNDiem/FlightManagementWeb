
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean, Enum
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
    flight_schedules = relationship('FlightSchedule', backref='flight_route', lazy=True)

    def __str__(self):
        return self.name


class Plane(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    aircraft_license_plate = Column(String(7), nullable=False)
    seats_1 = Column(Integer)
    seats_2 = Column(Integer)
    seats = relationship('Seat', backref='plane', cascade='all, delete-orphan', lazy=True)
    flights = relationship('Flight', secondary='flight_plane', lazy='subquery',
                           backref=backref('planes_list', lazy=True))

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


class FlightSchedule(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    flight_route_id = Column(Integer, ForeignKey(FlightRoute.id), nullable=False)
    description = Column(String(30))
    stop_points = relationship('StopPoint', backref='flight_schedule', lazy=True)
    flights = relationship('Flight', backref='flight_schedule', lazy=True)

    def __str__(self):
        return self.description


class StopPoint(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(30))
    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    stop_duration = Column(Integer, nullable=False)
    flight_schedule_id = Column(Integer, ForeignKey(FlightSchedule.id), nullable=False)
    stop_order = Column(Integer, nullable=False)

    def __str__(self):
        return self.name


class Flight(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    flight_route_id = Column(Integer, ForeignKey(FlightRoute.id), nullable=False)
    departure_time = Column(DateTime)
    duration = Column(Integer)
    flight_schedule_id = Column(Integer, ForeignKey(FlightSchedule.id))
    planes = relationship('Plane', secondary='flight_plane', lazy='subquery',
                          backref=backref('flights_list', lazy=True))
    tickets = relationship('Ticket', backref='flight', lazy=True)

    def __str__(self):
        return self.name


flight_plane = db.Table('flight_plane',
                        Column('flight_id', Integer, ForeignKey(Flight.id), primary_key=True),
                        Column('plane_id', Integer, ForeignKey(Plane.id), primary_key=True))


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
    phone_number = Column(Integer, nullable=False)
    CCCD = Column(Integer, nullable=False)
    birthday = Column(DateTime, nullable=False)
    gender = Column(Boolean, nullable=False)
    tickets = relationship('Ticket', backref='employee', lazy=True)

    def __str__(self):
        return self.name


class Customer(User):
    phone_number = Column(Integer)
    birthday = Column(DateTime)
    gender = Column(Boolean, nullable=True)
    receipts = relationship('ReceiptUser', backref='customer', lazy=True)

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
    CCCD = Column(Integer, nullable=False)
    phone_number = Column(Integer, nullable=False)
    email = Column(String(35), nullable=False)
    tickets = relationship('Ticket', backref='passenger', lazy=True)

    def __str__(self):
        return self.name


class Ticket(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    price = Column(Float)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    seat_id = Column(Integer, ForeignKey(Seat.id), unique=True, nullable=False)
    passenger_id = Column(Integer, ForeignKey(Passenger.id))
    employee_id = Column(Integer, ForeignKey(Employee.id))
    note = Column(String(200))
    receipt_details = relationship('ReceiptDetails', backref='ticket', lazy=True)


class PaymentMethod(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(30), nullable=False)
    receipts_user = relationship('ReceiptUser', backref='user_payment_method', lazy=True)
    receipts_guest = relationship('ReceiptGuest', backref='guest_payment_method', lazy=True)

    def __str__(self):
        return self.name


class Receipt(db.Model):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    booking_time = Column(DateTime, default=datetime.now(), nullable=False)
    payment_time = Column(DateTime)


class ReceiptUser(Receipt):
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    payment_method = Column(Integer, ForeignKey(PaymentMethod.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt_user', lazy=True)


class ReceiptGuest(Receipt):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    phone_number = Column(Integer, nullable=False)
    email = Column(String(35), nullable=False)
    payment_method = Column(Integer, ForeignKey(PaymentMethod.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt_guest', lazy=True)


class ReceiptDetails(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Integer, default=0)
    ticket_id = Column(Integer, ForeignKey(Ticket.id), nullable=False)
    receipt_user_id = Column(Integer, ForeignKey(ReceiptUser.id))
    receipt_guest_id = Column(Integer, ForeignKey(ReceiptGuest.id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()