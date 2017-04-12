from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from ext import myeppclient
my_epp = myeppclient.MyEpp( ssl_keyfile='client.key', ssl_certfile='client.pem',
                            ssl_validate_hostname=False, ssl_validate_cert=False)

from app import views,models
