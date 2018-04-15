from flask import Flask, redirect, url_for
from webapp.config import Config, DevConfig

from webapp.models import db
from webapp.controllers.blog import Blog
from webapp.controllers.main import Main
'''
#构造app的工厂函数，并添加了Bcrypt哈希算法加密
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app(name):  #config对象作为参数
    app = Flask(__name__)
    app.config.from_object(name)
    
    db.init_app(app)
    bcrypt.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('blog.home'))
    app.register_blueprint(Blog)

    return app
'''
#将哈希加密Bcrypt添加到app中
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

app = Flask(__name__)

app.config.from_object(DevConfig)

db.init_app(app)
bcrypt.init_app(app)

#根路径重定向
@app.route('/')
def index():
    return redirect(url_for('blog.home'))

app.register_blueprint(Blog)  #将Blog蓝图注册到app
app.register_blueprint(Main)  #注册Main蓝图

if __name__ == "__main__":
    app.run()
