
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand
from webapp import app
from webapp.models import db, User, Post, Comment, Tag  #导入models.py里的定义的数据模型

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment, Tag=Tag)
    #新建的表模型都要在这里传进去

if __name__ == "__main__":
    manager.run()
'''
#工厂模式的写法：
import os
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand
from webapp import create_app
from webapp.models import db, User, Post, Comment, Tag

#默认使用dev配置
env = os.envirron.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig'% env.capitalize())
#migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('server', Server())
#manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment, Tag=Tag)
    #新建的表模型都要在这里传进去

if __name__ == "__main__":
    manager.run()
'''
