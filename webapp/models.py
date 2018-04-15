from flask_sqlalchemy import SQLAlchemy
from webapp.extensions import bcrypt #user里密码检验用

db = SQLAlchemy() #app不在，导入则会循环导入，所以在__init__.py中实现导入

tags = db.Table('post_tags',
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')), #虚拟列
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                )

class User(db.Model):  #主表
    #__tabelname__ = 'user_tabel_name' #设置表名(则默认user类名小写)或用已有的表
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship( #虚拟列，关联从表(Post)对象中的db.ForeignKey
        'Post',
        backref='user',  #(回调字)使从表可通过Post.user对User对象进行读取,修改
        lazy = 'dynamic')  #动态加载关联对象(使用时加载),如子查询方式subquery(立即加载)

    def __init__(self, username):
        self.username = username
    def __repr__(self):
        return "<User '{}'>".format(self.username)
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
class Post(db.Model):  #User的从表
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id')) #外键约束,值必须存在于user.id中
    comments = db.relationship(
        'Comment',
        backref='post', #回调方式：Comment.post
        lazy='dynamic',) #动态加载
    tags = db.relationship(
        'Tag',
        secondary=tags, #次级，表明该关联保存在tags表里(而不是Tag模型的表)
        backref=db.backref('posts',lazy='dynamic'),
        )

    def __init__(self, title):
        self.title = title
    def __repr__(self):
        return "<Post '{}'>".format(self.title)

class Comment(db.Model):  #Post的从表
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())

    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id')) #外键约束

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    def __init__(self, title):
        self.title = title
    def __repr__(self):
        return "<Tag '{}'>".format(self.title)


