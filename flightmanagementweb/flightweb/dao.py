import hashlib
from flightweb import db
from models import Employee, Admin, Customer


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

