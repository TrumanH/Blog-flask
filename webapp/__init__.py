
from flask import Flask, redirect, url_for
from webapp.config import DevConfig

from webapp.models import db
from webapp.controllers.blog import Blog

app = Flask(__name__)

app.config.from_object(DevConfig)

db.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('blog.home'))

app.register_blueprint(Blog)  #将Blog蓝图注册到app

if __name__ == "__main__":
    app.run()
