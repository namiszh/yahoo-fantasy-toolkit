# -*- coding: utf-8 -*-
"""
    Yahoo fantasy basketball data analysis display

    copyright: (c) 2022 by Shaozuo Huang
"""

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from yahoo.oauth import YOAuth
from yahoo.yhandler import YHandler


app = Flask(__name__)

# read configuration from file config.py
app.config.from_object('config')

# Initialize a Yahoo OAuth object
yOauth = YOAuth(app.config['CREDENTIALS_FILE'])
yHandler = YHandler(yOauth)

# db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# run application
if __name__ == "__main__": 
    app.run(ssl_context=('./cert/cert.pem', './cert/key.pem'), debug=True)


from routes import views, auth