from flask import render_template, Blueprint

from flask import Flask, redirect, url_for, flash
from webapp.forms import LoginForm, RegisterForm

Main = Blueprint('main', __name__, template_folder='../templates/main')

@Main.route('/')
def index():
    return redirect(url_for('blog.home'))

@Main.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('You have been logged in.', category='success')
        return redirect(url_for('blog.home'))
    return render_template('login.html', form = form)

@Main.route('/logout', methods=['GET','POST'])
def logout():
    flash('You hava been logged out.', category='success')
    return redirect(url_for('.home'))

@Main.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User()
        new_user.name = form.username.data
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()
        flash('Your user has been created, please login.', category='success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)
    

