from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key = "#@^(*&!#)(*)#"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/flightdb?charset=utf8mb4"
db = SQLAlchemy(app)
login = LoginManager(app)

cloudinary.config(cloud_name='dvcawiqmq',
                  api_key='953287585951812',
                  api_secret='NxXA-S3XxWmSCpqTiQVL_JwpYvQ')
