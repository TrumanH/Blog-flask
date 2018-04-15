from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

'''
#添加到app对象中
from webapp.extensions import bycrypt

def create_app(name):
    app = Flask(__name__)
    app.config.from_object(name)

    db.init_app(app)
    bcrypt.init_app(app)
'''
