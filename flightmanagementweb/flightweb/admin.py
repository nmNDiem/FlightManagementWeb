from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flightweb import app, db
from models import (Flight, FlightRoute, FlightRouteType, Airport, Plane, Seat, SeatType,
                    FlightSchedule, StopPoint)


class FlightView(ModelView):
    column_list = ['id', 'name', 'flight_route_id', 'departure_time', 'duration', 'planes']
    column_searchable_list = ['id', 'name']
    column_filters = ['flight_route_id', 'departure_time', 'duration']
    column_labels = {
        'id': 'ID',
        'name': 'Tên chuyến bay',
        'flight_route_id': 'Tuyến bay',
        'departure_time': 'Thời gian khởi hành',
        'duration': 'Thời gian bay',
        'planes': 'Máy bay sử dụng'
    }


class FlightRouteView(ModelView):
    column_list = ['id', 'name', 'flight_route_type_id', 'departure_airport_id', 'destination_airport_id']
    column_searchable_list = ['departure_airport_id', 'destination_airport_id']
    column_filters = ['flight_route_type_id', 'departure_airport_id', 'destination_airport_id']
    column_labels = {
        'id': 'ID',
        'name': 'Tên tuyến bay',
        'flight_route_type_id': 'Loại tuyến bay',
        'departure_airport_id': 'Sân bay khởi hành',
        'destination_airport_id': 'Sân bay đến'
    }


class FlightRouteTypeView(ModelView):
    column_list = ['id', 'description', 'flight_routes']
    column_filters = ['description']
    column_labels = {
        'id': 'ID',
        'description': 'Loại tuyến bay',
        'flight_routes': 'Danh sách tuyến bay'
    }


class AirportView(ModelView):
    column_list = ['id', 'sign', 'name', 'address', 'longitude', 'latitude',
                   'flight_routes_departure', 'flight_routes_destination']
    column_searchable_list = ['id', 'name', 'address']
    column_labels = {
        'id': 'ID',
        'sign': 'Mã sân bay',
        'name': 'Tên sân bay',
        'address': 'Địa chỉ',
        'longitude': 'Kinh độ',
        'latitude': 'Vĩ độ',
        'flight_routes_departure': 'Danh sách tuyến bay khởi hành tại đây',
        'flight_routes_destination': 'Danh sách tuyến bay đến đây'
    }


class PlaneView(ModelView):
    column_list = ['id', 'name', 'aircraft_license_plate', 'seats_1', 'seats_2', 'seats', 'flights']
    column_searchable_list = ['id', 'name', 'aircraft_license_plate']
    column_filters = ['name', 'seats_1', 'seats_2']
    column_labels = {
        'id': 'ID',
        'name': 'Tên máy bay',
        'aircraft_license_plate': 'Biển số',
        'seats_1': 'Số lượng ghế hạng 1',
        'seats_2': 'Số lượng ghế hạng 2',
        'seats': 'Danh sách ghế',
        'flights': 'Danh sách chuyến bay'
    }


class SeatView(ModelView):
    column_list = ['id', 'name', 'seat_type_id', 'plane_id']
    column_searchable_list = ['id', 'name', 'seat_type_id']
    column_filters = ['name', 'seat_type_id', 'plane_id']
    column_labels = {
        'id': 'ID',
        'name': 'Tên ghế',
        'seat_type_id': 'Hạng ghế',
        'plane_id': 'Máy bay'
    }


class SeatTypeView(ModelView):
    column_list = ['id', 'name', 'seats']
    column_filters = ['name']
    column_labels = {
        'id': 'ID',
        'name': 'Hạng ghế',
        'seats': 'Danh sách ghế'
    }


class FlightScheduleView(ModelView):
    column_list = ['id', 'flight_route_id', 'description', 'stop_points', 'flights']


class StopPointView(ModelView):
    column_list = ['id', 'name', 'airport_id', 'stop_duration', 'flight_schedule_id', 'stop_order']


admin = Admin(app, name='Flight Management Website', template_mode='bootstrap4')
admin.add_view(FlightView(Flight, db.session))
admin.add_view(FlightRouteView(FlightRoute, db.session))
admin.add_view(FlightRouteTypeView(FlightRouteType, db.session))
admin.add_view(AirportView(Airport, db.session))
admin.add_view(PlaneView(Plane, db.session))
admin.add_view(SeatView(Seat, db.session))
admin.add_view(SeatTypeView(SeatType, db.session))
admin.add_view(FlightScheduleView(FlightSchedule, db.session))
admin.add_view(StopPointView(StopPoint, db.session))
