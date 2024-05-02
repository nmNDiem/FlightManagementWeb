from flask import render_template

from flightweb import app, admin


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/admin')
# def admin():
#     return render_template('admin/index.html')


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
