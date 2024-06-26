import hashlib
from datetime import datetime
from sqlalchemy import and_, func, cast, Date
from flightweb import db, app

from models import SeatType, \

 UpdateDatve
from models import Employee, Admin, Customer, Flight, Airport, FlightRoute, ReceiptDetails, Ticket, Seat, SeatType, \

    PaymentMethod, Passenger

from models import (Employee, Admin, Customer, Flight, Airport, FlightRoute, ReceiptDetails, Ticket,
                    Receipt, Seat) main



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


def add_customer(name, username, password, avatar, email, phone, cccd, birthday):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    customer = Customer(
        name=name,
        username=username,
        password=password,
        avatar=avatar,
        email=email,
        phone_number=phone,
        CCCD=cccd,
        birthday=birthday
    )
    db.session.add(customer)
    db.session.commit()


def search_flights(departure_sign, destination_sign, departure_date):
    # Chuyển đổi chuỗi ngày thành đối tượng date
    departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()

    flights = Flight.query.join(FlightRoute, Flight.flight_route_id == FlightRoute.id) \
        .join(Airport, FlightRoute.departure_airport_id == Airport.id) \
        .filter(
            Airport.sign == departure_sign,
            FlightRoute.destination_airport.has(sign=destination_sign),
            cast(Flight.departure_time, Date) == departure_date
        ).all()
    return flights


def select_flight(id):
    return Flight.query.get(id)


def get_airport_id(id):
    return Airport.query.get(id)


def get_all_flights():
    return Flight.query.all()


def get_airports():
    return Airport.query.all()


def get_seat(flight_id, seat_type_id):
    # Tìm plane_id từ flight_id
    plane_id = db.session.query(Flight.plane_id).filter(Flight.id == flight_id).scalar()

    # Lấy danh sách ghế trống
    seats = db.session.query(Seat).join(
        SeatType, Seat.seat_type_id == SeatType.id
    ).outerjoin(
        Ticket, Seat.id == Ticket.seat_id
    ).filter(
        SeatType.id == seat_type_id,
        Seat.plane_id == plane_id,
        Ticket.passenger_id.is_(None)
    ).all()

    return seats


def get_paymethod():
    return PaymentMethod.query.all()


def get_paymethod_id(id):
    return PaymentMethod.query.get(id)


def get_seat_id(id):
    return Seat.query.get(id)


def create_passenger(last_name, first_name, cccd, email, phone_number, birthday, gender):
    passenger = Passenger(
        name=f"{last_name} {first_name}",
        birthday=birthday,
        gender=gender,
        CCCD=cccd,
        phone_number=phone_number,
        email=email
    )
    db.session.add(passenger)
    db.session.commit()
    return passenger


def create_ticket(flight_id, seat_id, passenger_id):
    ticket = Ticket(
        flight_id=flight_id,
        seat_id=seat_id,
        passenger_id=passenger_id
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket


def count_flights_by_route(year=datetime.now().year, month=datetime.now().month):
    return (db.session.query(FlightRoute.id, FlightRoute.name, func.count(Flight.id))
            .join(Flight, Flight.flight_route_id.__eq__(FlightRoute.id), isouter=True)
            .group_by(FlightRoute.id).all())



def stats_revenue_by_route():
    return (db.session.query(FlightRoute.id, FlightRoute.name,
                             func.sum(ReceiptDetails.unit_price * ReceiptDetails.quantity))
            .join(Flight, Flight.flight_route_id.__eq__(FlightRoute.id), isouter=True)
            .join(Ticket, Ticket.flight_id.__eq__(Flight.id), isouter=True)
            .join(ReceiptDetails, ReceiptDetails.ticket_id.__eq__(Ticket.id), isouter=True)
            .group_by(FlightRoute.id)).all()


# def count_flights_by_route_by_month(year=datetime.now().year, month=datetime.now().month):
#     return (db.session.query(func.count(Flight.id))
#             .join(FlightRoute, FlightRoute.id.__eq__(Flight.flight_route_id))
#             .group_by(func.extract('month', Flight.departure_time), FlightRoute.id)
#             .filter(func.extract('month', Flight.departure_time).__eq__(month)).all())
#
#
# def get_total_revenue_by_month(year=datetime.now().year, month=datetime.now().month):
#     query = (db.session.query(func.extract('year', Receipt.payment_time),
#                               func.extract('month', Receipt.payment_time),
#                               func.sum(ReceiptDetails.unit_price * ReceiptDetails.quantity))
#              .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id))
#              .filter(func.extract('year', Receipt.payment_time).__eq__(year)
#                      .__and__(func.extract('month', Receipt.payment_time).__eq__(month))))
#
#     return query.group_by(func.extract('year', Receipt.payment_time),
#                           func.extract('month', Receipt.payment_time)).all()




def stats_revenue_by_month(year=datetime.now().year, month=datetime.now().month):
    # Truy vấn để tính tổng doanh thu theo tuyến bay trong tháng
    report_data = db.session.query(
        FlightRoute.name.label('route_name'),
        func.sum(ReceiptDetails.unit_price * ReceiptDetails.quantity).label('total_revenue'),
        func.count(Flight.id).label('total_flights')
    ).join(Flight).join(Ticket).join(ReceiptDetails).join(Receipt) \
        .filter(func.extract('month', Receipt.payment_time).__eq__(month)) \
        .group_by(FlightRoute.id) \
        .all()

    # Tính tổng doanh thu
    total_revenue = sum([data.total_revenue for data in report_data])

    return report_data


def get_total_revenue(year=datetime.now().year, month=datetime.now().month):
    # Truy vấn để tính tổng doanh thu theo tuyến bay trong tháng
    report_data = db.session.query(
        FlightRoute.name.label('route_name'),
        func.sum(ReceiptDetails.unit_price * ReceiptDetails.quantity).label('total_revenue'),
        func.count(Flight.id).label('total_flights')
    ).join(Flight).join(Ticket).join(ReceiptDetails).join(Receipt) \
        .filter(func.extract('month', Receipt.payment_time).__eq__(month)) \
        .group_by(FlightRoute.id) \
        .all()

    # Tính tổng doanh thu
    total_revenue = sum([data.total_revenue for data in report_data])

    return total_revenue


def get_ticket_id(id):
    return Ticket.query.get(id)


def get_client_ip(request):
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        ip = request.remote_addr
    return ip


if __name__ == '__main__':
    with app.app_context():
        print(get_seat_id(2))

