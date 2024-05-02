from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flightweb import app, db
from models import FlightRoute, Airport


class FlightRouteView(ModelView):
    column_list = ['id', 'name', 'departure_airport_id', 'destination_airport_id']


admin = Admin(app, name='Flight Management Website', template_mode='bootstrap4')
admin.add_view(FlightRouteView(FlightRoute, db.session))
admin.add_view(ModelView(Airport, db.session))

