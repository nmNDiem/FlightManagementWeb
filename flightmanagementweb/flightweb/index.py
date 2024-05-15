from flask import Flask, render_template, request
from flightweb import db, app
from dao import search_flights, get_airports


@app.route('/')
def index():
    airports = get_airports()
    return render_template('searchForm.html', airports=airports)


# @app.route('/admin')
# def admin():
#     return render_template('admin/index.html')

@app.route('/search_flight', methods=['GET'])
def search_flight():
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    departure_date = request.args.get('departure_date')

    flights = search_flights(departure, destination, departure_date)

    return render_template('loadFlight.html', flights=flights)


# @app.route('/')
# def index():
#     airports = get_airports()
#     return render_template('index.html', airports=airports)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
