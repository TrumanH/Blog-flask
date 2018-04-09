from sqlalchemy import func
from flask import Flask, render_template
from config import DevConfig

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(DevConfig)
db = SQLAlchemy(app)

class CommentForm(Form):
    name = StringField(
        'Name', validators=[DataRequired(), Length(max=255)])
    text = TextAreaField(u'Comment', validators=[DataRequired()])

@app.route('/')   #视图
@app.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(
        Post.publish_date.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()
    return render_template('home.html',posts=posts,recent=recent,top_tags=top_tags)

def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()).limit(5).all()  #根据日期查询出的最新5篇文章
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')).join(
            tags).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags

@app.route('/post/<int:post_id>') #视图
def post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template('post.html',
        post=post,tags=tags,comments=comments,recent=recent,top_tags=top_tags)
@app.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag,query.filter_by(title=tag_name).frist_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template('tag.html',tag=tag,posts=posts,recent=recent,
                           top_tags=top_tags)
@app.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template('user.html',user=user,posts=posts,recent=recent,
                           top_tags=top_tags)
    
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

tags = db.Table('post_tags',
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')), #虚拟列
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                )

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
        
'''
@app.route('/')
def home():
    return '<h1>Hello World!</h1>'
'''

if __name__ == "__main__":
    app.run()
