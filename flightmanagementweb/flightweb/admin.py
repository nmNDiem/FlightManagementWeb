from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flightweb import app, db
from models import FlightRoute, FlightRouteType, Airport, Plane, Flight, Seat, SeatType


# class FlightRouteView(ModelView):
#     column_list = ['id', 'name', 'departure_airport_id', 'destination_airport_id']


admin = Admin(app, name='Flight Management Website', template_mode='bootstrap4')
# admin.add_view(FlightRouteView(FlightRoute, db.session))
admin.add_view(ModelView(FlightRoute, db.session))
admin.add_view(ModelView(FlightRouteType, db.session))
admin.add_view(ModelView(Flight, db.session))
admin.add_view(ModelView(Airport, db.session))
admin.add_view(ModelView(Plane, db.session))
admin.add_view(ModelView(Seat, db.session))
admin.add_view(ModelView(SeatType, db.session))

