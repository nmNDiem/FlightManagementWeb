from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect

from flightweb import app, db, dao
from models import (Flight, FlightRoute, FlightRouteType, Airport, Plane, Seat, SeatType,
                    StopPoint, UserRole, Employee, Customer,
                    Passenger, Ticket, ReceiptDetails, Receipt, PaymentMethod)


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class FlightView(AuthenticatedView):
    column_list = ['id', 'name', 'flight_route_id', 'departure_time', 'destination_time', 'duration',
                   'plane_id', 'price_seat1', 'price_seat2', 'stop_points', 'tickets']
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


class FlightRouteView(AuthenticatedView):
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


class FlightRouteTypeView(AuthenticatedView):
    column_list = ['id', 'description', 'flight_routes']
    column_filters = ['description']
    column_labels = {
        'id': 'ID',
        'description': 'Loại tuyến bay',
        'flight_routes': 'Danh sách tuyến bay'
    }


class AirportView(AuthenticatedView):
    column_list = ['id', 'sign', 'name', 'address', 'longitude', 'latitude', 'stop_points',
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
        'flight_routes_destination': 'Danh sách tuyến bay đến đây',
        'stop_points': 'Các điểm dừng'
    }


class PlaneView(AuthenticatedView):
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


class SeatView(AuthenticatedView):
    column_list = ['id', 'name', 'seat_type_id', 'plane_id', 'ticket']
    column_searchable_list = ['id', 'name', 'seat_type_id']
    column_filters = ['name', 'seat_type_id', 'plane_id']
    column_labels = {
        'id': 'ID',
        'name': 'Tên ghế',
        'seat_type_id': 'Hạng ghế',
        'plane_id': 'Máy bay',
        'ticket': 'Vé'
    }


class SeatTypeView(AuthenticatedView):
    column_list = ['id', 'name', 'seats']
    column_filters = ['name']
    column_labels = {
        'id': 'ID',
        'name': 'Hạng ghế',
        'seats': 'Danh sách ghế'
    }


class StopPointView(AuthenticatedView):
    column_list = ['id', 'name', 'airport_id', 'stop_duration', 'flight_schedule_id', 'stop_order']


class MyTicketView(AuthenticatedView):
    column_list = ['id', 'flight_id', 'seat_id', 'passenger_id', 'employee_id', 'note']


class MyPassengerView(AuthenticatedView):
    pass


class MyEmployeeView(AuthenticatedView):
    pass


class MyCustomerView(AuthenticatedView):
    pass


class MyReceiptDetailsView(AuthenticatedView):
    pass


class MyReceiptView(AuthenticatedView):
    pass


class MyPaymentMethodView(AuthenticatedView):
    pass


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue_by_month()
        total_revenue = dao.get_total_revenue()
        return self.render('admin/index.html', stats=stats, total_revenue=total_revenue)


admin = Admin(app, name='Flight Management Website', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(FlightView(Flight, db.session))
admin.add_view(FlightRouteView(FlightRoute, db.session))
admin.add_view(FlightRouteTypeView(FlightRouteType, db.session))
admin.add_view(AirportView(Airport, db.session))
admin.add_view(PlaneView(Plane, db.session))
admin.add_view(SeatView(Seat, db.session))
admin.add_view(SeatTypeView(SeatType, db.session))
admin.add_view(StopPointView(StopPoint, db.session))
admin.add_view(MyPassengerView(Passenger, db.session))
admin.add_view(MyEmployeeView(Employee, db.session))
admin.add_view(MyCustomerView(Customer, db.session))
admin.add_view(MyTicketView(Ticket, db.session))
admin.add_view(MyReceiptDetailsView(ReceiptDetails, db.session))
admin.add_view(MyReceiptView(Receipt, db.session))
admin.add_view(MyPaymentMethodView(PaymentMethod, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))
