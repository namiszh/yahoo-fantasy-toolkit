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
from matplotlib import font_manager

app = Flask(__name__)

# read configuration from file config.py
app.config.from_object('config')

# Initialize a Yahoo OAuth object
yOauth = YOAuth(app.config['CREDENTIALS_FILE'])
yHandler = YHandler(yOauth)

print(app.config['CHINESE_FONT_FILE'])
cnFontProp = font_manager.FontProperties(fname=app.config['CHINESE_FONT_FILE'])
# cnFontProp.set_family('SimHei')
# cnFontProp.set_size(8)

# db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# run application
# if __name__ == "__main__": 
    # app.run(ssl_context=('./cert/cert.pem', './cert/key.pem'), debug=True)
    # app.run()


from routes import views, auth