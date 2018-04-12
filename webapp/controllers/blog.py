import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint

from webapp.models import db, Post, Tag, Comment, User, tags
from webapp.forms import CommentForm

'''#自定义一个Jinja过滤器
def count_substring(string, sub):
    return string.count(sub)
#将其添加进jinja_env对象的filter字典：
app.jinja_env.filters['count_substring'] = count_substring
#模板中使用方式：{{ "string" | count_substring("sub") }}

'''
'''#登陆
from flask import g, session, abort
@app.before_request    #处理view请求视图函数前,结束则:@app.teardown_request
def before_request():
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@app.route('/restricted')  #登陆后
def admin():
    if g.user is None:
        abort(403)
    return render_template('admin.html')
#自定义返回错误页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
#通用视图类
from flask.view import View
class GenView(View):
    methods = ['GET', 'POST']
    def __init__(self, template):
        self.template = template
        super(GenView,self).__init__()
    def dispatch_request(self);  #类似于视图函数
        if request.method == 'GET':
            return render_template(self.template)
        elif request.method == 'POST':
            return render_template(...)
app.add_url_rule('/',  #类似于app.route(),将路由绑定到函数
     view_func=GenView.as_view('home', template='home.html'))
#方法视图MethodView解决方案
from flask.views import MethodView
class UserView(MethodView):
    def get(self):
        ...
    def post(self):
        ...
app.add_url_rule('/user', view_func=UserView.as_view('user'))
'''
'''
#蓝图Blueprint,类似于app
from flask import Blueprint
example = Blueprint(
    'example', __name__,template_folder='templates/example',
    static_folder='static/example', url_prefix='/example')
@example.route('/')
def home():
    return render_template('home.html')
@app.register_blueprint(example)  #将蓝图添加到app中，下一步使用
blog_blueprint = Blueprint('blog', __name__, template_folder='templates/blog',
    url_prefix='/blog') #移动模板,@app.route改为@blog_blueprint.route,
#类视图注册到blog_blueprint,模板中也url_for()参数改(前面加句点),文件最后加上一句
#app.register_blueprint(blog_blueprint)
#根路径重定向
@app.route('/')
def index():
    return redirect(url_for('blog.home')) #blog蓝图名
'''

#引入蓝图,新建蓝图,添加蓝图到app,然后定义其视图
Blog = Blueprint(
    'blog', __name__,template_folder='../templates/blog',
    static_folder='../static', url_prefix='/blog')
#prefix会自动将url前缀加在这个蓝图所有路由之前 /blog/

@Blog.route('/')   #路由
@Blog.route('/<int:page>')
def home(page=1):  #视图渲染
    posts = Post.query.order_by(
        Post.publish_date.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()
    return render_template('home.html',posts=posts,recent=recent,top_tags=top_tags)

def sidebar_data():  
    recent = Post.query.order_by(
        Post.publish_date.desc()).limit(5).all()  #根据日期查询出的最新5篇文章
    top_tags = db.session.query(   #最高频的5个标签
        Tag, func.count(tags.c.post_id).label('total')).join(
            tags).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags

@Blog.route('/post/<int:post_id>', methods=('GET', 'POST')) #路由，视图
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        new_comment.date = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()
    
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template('post.html', post=post, tags=tags, comments=comments,
            recent=recent, top_tags=top_tags, form=form)

@Blog.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).frist_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template('tag.html',tag=tag,posts=posts,recent=recent,
                           top_tags=top_tags)
@Blog.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template('user.html',user=user,posts=posts,recent=recent,
                           top_tags=top_tags)

