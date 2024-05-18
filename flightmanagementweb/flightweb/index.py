from flask import render_template, redirect, request
import dao
from flask_login import login_user, logout_user
from flightweb import app, admin, login, app
import cloudinary.uploader
from flightweb import app
import hashlib
import urllib.parse
from datetime import datetime, timedelta
app.config.from_object('config.Config')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    airports = dao.get_airports()
    return render_template('searchForm.html', airports=airports)


# @app.route('/admin')
# def admin():
#     return render_template('admin/index.html')


@app.route('/search_flight', methods=['GET', 'POST'])
def search_flight():
    if request.method == 'POST':
        departure = request.form['departure']
        destination = request.form['destination']
        departure_date = request.form['departureDate']
        seat_type = request.form['ticketType']
        flights = dao.search_flights(departure, destination, departure_date)
        return render_template('loadFlight.html', flights=flights, seat_type=seat_type)
    else:
        # Trả về form tìm kiếm nếu là GET
        return render_template('searchForm.html')


@app.route('/select_flight', methods=['GET', 'POST'])
def select_flight():
    flight_id = request.form['flight_id']
    departure_id = request.form['departure_id']
    destination_id = request.form['destination_id']
    seat_type = request.form['seat_type']
    flight = dao.select_flight(flight_id)
    departure = dao.get_airport_id(departure_id)
    destination = dao.get_airport_id(destination_id)
    if seat_type == 'business':
        seat_type_id = 1
    else:
        seat_type_id = 2
    seat = dao.get_seat(flight_id, seat_type_id)
    pay_method = dao.get_paymethod()
    return render_template('infomation.html', flight=flight,
                           departure=departure, destination=destination, seat_type=seat_type,seat_type_id=seat_type_id,
                           seats=seat, pay_method=pay_method)


@app.route('/receipt', methods=['POST'])
def receipt():
    last_name = request.form['last_name']
    first_name = request.form['first_name']
    cccd = request.form['cccd']
    email = request.form['email']
    phone_number = request.form['phone_number']
    birthday = request.form['birthday']
    gender = request.form['gender'] == 'true'  # Chuyển đổi chuỗi thành giá trị Boolean
    pay_method_id = request.form['pay_method']
    flight_id = request.form['flight_id']
    departure_id = request.form['departure_id']
    destination_id = request.form['destination_id']
    seat_id = request.form['seat']
    seat_type = request.form['seat_type']
    seat = dao.get_seat_id(seat_id)
    departure = dao.get_airport_id(departure_id)
    destination = dao.get_airport_id(destination_id)
    flight = dao.select_flight(flight_id)
    pay_method = dao.get_paymethod_id(pay_method_id)

    # Tạo đối tượng Passenger
    passenger = dao.create_passenger(last_name, first_name, cccd, email, phone_number, birthday, gender)

    # Tạo đối tượng Ticket
    ticket = dao.create_ticket(flight_id, seat_id, passenger.id)

    return render_template('receipt.html',last_name=last_name,first_name=first_name,cccd=cccd,email=email,
                           phone_number=phone_number,birthday=birthday,gender=gender,pay_method=pay_method,flight=flight,
                           departure=departure,destination=destination,seat=seat,seat_type=seat_type,ticket=ticket)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        ticket_id = request.form['ticket_id']
        try:
            amount = int(float(request.form['amount']) * 100)
        except ValueError:
            return "Invalid amount format", 400

        # Truy vấn cơ sở dữ liệu để lấy thông tin liên quan đến ticket_id
        ticket = dao.get_ticket_id(ticket_id)
        ipaddr = dao.get_client_ip(request)

        if not ticket:
            return "Invalid ticket ID", 400

        vnp_Params = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': app.config['VNPAY_TMN_CODE'],
            'vnp_Amount': str(amount),  # Ensure amount is a string
            'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
            'vnp_CurrCode': 'VND',
            'vnp_IpAddr': ipaddr,
            'vnp_Locale': 'vn',  # Default language
            'vnp_OrderInfo': 'Payment',
            'vnp_OrderType': 'billpayment',  # Example order type
            'vnp_ReturnUrl': app.config['VNPAY_RETURN_URL'],
            'vnp_ExpireDate': (datetime.now() + timedelta(minutes=30)).strftime('%Y%m%d%H%M%S'),
            'vnp_TxnRef': ticket_id,
            'vnp_SecureHash': 'SHA256'
        }

        vnp_Params = dict(sorted(vnp_Params.items()))
        queryString = urllib.parse.urlencode(vnp_Params)
        secureHash = hashlib.sha256((app.config['VNPAY_HASH_SECRET_KEY'] + queryString).encode('utf-8')).hexdigest()
        vnp_Params['vnp_SecureHashType'] = 'SHA256'
        vnp_Params['vnp_SecureHash'] = secureHash

        vnpay_payment_url = app.config['VNPAY_PAYMENT_URL'] + '?' + urllib.parse.urlencode(vnp_Params)
        return redirect(vnpay_payment_url)
    else:
        return render_template('payment.html', title="Thanh toán")



# @app.route('/')
# def index():
#     airports = get_airports()
#     return render_template('index.html', airports=airports)


@app.route("/admin-login", methods=['post'])
def process_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    return redirect('/admin')


@app.route('/login', methods=['get', 'post'])
def login_my_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)

            next = request.args.get('next')
            return redirect(next if next else '/')
        else:
            err_msg = 'Username hoặc password không đúng!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/logout', methods=['get', 'post'])
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = None
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password == confirm:
            avatar_path = None
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']

            dao.add_customer(
                name=request.form.get('name'),
                username=request.form.get('username'),
                password=password,
                avatar=avatar_path,
                email=request.form.get('email'),
                phone=request.form.get('phone'),
                birthday=request.form.get('birthday')
            )

            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@login.user_loader
def load_user(user_id):
    user = dao.get_employee_by_id(user_id)
    if user:
        return user

    user = dao.get_customer_by_id(user_id)
    if user:
        return user

    user = dao.get_admin_by_id(user_id)
    if user:
        return user

    return None


if __name__ == '__main__':
    with app.app_context():
        app.run(port=5001, debug=True)
