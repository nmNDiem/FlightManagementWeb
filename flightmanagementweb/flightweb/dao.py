import hashlib
from datetime import datetime
from sqlalchemy import and_
from flightweb import db, app
from models import Employee, Admin, Customer, Flight, Airport, FlightRoute


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


if __name__ == '__main__':
    with app.app_context():
        print(get_all_flights())


