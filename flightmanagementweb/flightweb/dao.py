import hashlib
from datetime import datetime
from sqlalchemy import and_, func
from flightweb import db, app
from models import (Employee, Admin, Customer, Flight, Airport, FlightRoute, ReceiptDetails, Ticket,
                    Receipt, Seat)


def get_employee_by_id(id):
    return Employee.query.get(id)


def get_customer_by_id(id):
    return Customer.query.get(id)


def get_admin_by_id(id):
    return Admin.query.get(id)


def auth_user(username, password):
    hashed_password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

    admin = Admin.query.filter(Admin.username == username.strip(),
                               Admin.password == hashed_password).first()
    if admin:
        return admin

    employee = Employee.query.filter(Employee.username == username.strip(),
                                     Employee.password == hashed_password).first()
    if employee:
        return employee

    customer = Customer.query.filter(Customer.username == username.strip(),
                                     Customer.password == hashed_password).first()
    if customer:
        return customer

    return None


def add_customer(name, username, password, avatar, email, phone, birthday):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    customer = Customer(
        name=name,
        username=username,
        password=password,
        avatar=avatar,
        email=email,
        phone_number=phone,
        birthday=birthday
    )
    db.session.add(customer)
    db.session.commit()


def search_flights(departure_sign, destination_sign, departure_date):
    # Chuyển đổi chuỗi ngày thành đối tượng datetime
    departure_date = datetime.strptime(departure_date, '%Y-%m-%d')

    flights = Flight.query.join(FlightRoute, Flight.flight_route_id == FlightRoute.id) \
        .join(Airport, FlightRoute.departure_airport_id == Airport.id) \
        .filter(Airport.sign == departure_sign,
                FlightRoute.destination_airport.has(sign=destination_sign),
                Flight.departure_time >= departure_date).all()
    return flights


def get_all_flights():
    return Flight.query.all()


def get_airports():
    return Airport.query.all()


def count_flights_by_route_by_month(year=datetime.now().year, month=datetime.now().month):
    return (db.session.query(func.extract('month', Flight.departure_time), FlightRoute.name, func.count(Flight.id))
            .join(FlightRoute, FlightRoute.id.__eq__(Flight.flight_route_id))
            .group_by(func.extract('month', Flight.departure_time), FlightRoute.name)
            .filter(func.extract('month', Flight.departure_time).__eq__(month)).all())


def stats_revenue_by_route():
    return (db.session.query(FlightRoute.id, FlightRoute.name,
                             func.sum(ReceiptDetails.unit_price * ReceiptDetails.quantity))
            .join(Flight, Flight.flight_route_id.__eq__(FlightRoute.id), isouter=True)
            .join(Ticket, Ticket.flight_id.__eq__(Flight.id), isouter=True)
            .join(ReceiptDetails, ReceiptDetails.ticket_id.__eq__(Ticket.id), isouter=True)
            .group_by(FlightRoute.id)).all()


def stats_revenue_by_month(year=datetime.now().year, month=datetime.now().month):
    return db.session.query()


def get_total_revenue_by_month(year=datetime.now().year, month=datetime.now().month):
    query = (db.session.query(func.extract('year', Receipt.payment_time),
                              func.extract('month', Receipt.payment_time),
                              func.sum(ReceiptDetails.unit_price * ReceiptDetails.quantity))
             .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id))
             .filter(func.extract('year', Receipt.payment_time).__eq__(year)
                     .__and__(func.extract('month', Receipt.payment_time).__eq__(month))))
    return query.group_by(func.extract('year', Receipt.payment_time),
                          func.extract('month', Receipt.payment_time)).all()


if __name__ == '__main__':
    with app.app_context():
        print(get_total_revenue_by_month(month=3))
