from flask import render_template, request, redirect, Flask
import dao
from flask_login import login_user, logout_user
from flightweb import app, admin, login, app
import cloudinary.uploader



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


@login.user_loader
def load_user(user_id):
    user = dao.get_employee_by_id(user_id)
    if user:
        return user

    # user = get_customer_by_id(user_id)
    # if user:
    #     return user
    #
    # user = get_admin_by_id(user_id)
    # if user:
    #     return user

    return None


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


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
