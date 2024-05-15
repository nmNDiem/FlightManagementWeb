from models import Flight, Airport
from flightweb import db


def search_flights(departure, destination, departure_date):
    query = db.session.query(Flight)

    if departure_date:
        query = query.filter(db.func.date(Flight.departure_time) == departure_date)

    if departure:
        query = query.filter(Flight.departure_airport.has(name=departure))

    if destination:
        query = query.filter(Flight.destination_airport.has(name=destination))

    return query.all()


def get_airports():
    return Airport.query.all()

