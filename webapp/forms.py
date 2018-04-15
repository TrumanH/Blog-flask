from flask_wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL


#评论表单
class CommentForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    text = TextAreaField(u'Comment', validators=[DataRequired()])

#登陆表单
class LoginForm(Form):
    username = StringField('Username',[DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    def validate(self):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:  #如果验证没通过
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not user:  #检查是否有该用户
            self.username.errors.append('Invalid username or password')
            return False
        #检查密码匹配,用了user的哈希匹配检测check_password()
        if not self.user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False
        return True
    
#注册表单
class RegisterForm(Form):
    username = StringField('Username',[DataRequired(), Length(max=255)])
    password = PasswordField('Password',[DataRequired(),Length(min=8)])
    confirm = PasswordField('Confirm Password',[DataRequired(),
            EqualTo('password')])
    #recaptcha = RecaptchaField() #google的网页表单验证码机制,还没注册不能用
    def validate(self): #验证
        check_validate = super(RegisterForm, self).validate()
        if not check_validate: #如果验证没通过
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user: #该用户名已存在（已被使用）
            self.username.errors.append('User with that name already exists')
            return False
        return True

#创建文章表单
class PostForm(Form):
    title = StringField('Title', [DataRequired(),Length(255)])
    text = TextAreaField('Content', [DataRequired()])
    
        
