from functools import wraps

from flask import render_template, request, current_app, redirect, flash, url_for
from flask_login import login_required, login_user, current_user, logout_user

from . import blueprint
from .forms import LoginForm, SignupForm
from ..models import User, db


def anonymous_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You have logged-in.')
            return redirect(url_for('default.index', is_login=False))
        else:
            return func(*args, **kwargs)

    return decorated_view


@blueprint.route('/')
@login_required
def index():
    # if 'is_login' not in session:
    #     return redirect('/login')
    return render_template('home.html', is_login=True, enumerate_words=enumerate(['教务', '通知', '补考', '四六级']))


@blueprint.route('/login/', methods=['GET', 'POST'])
@anonymous_required
def login():
    next_page = request.args.get('next')

    login_form = LoginForm()
    if login_form.validate_on_submit():
        current_app.logger.info(
            'login: %s %s %s' % (login_form.email.data, login_form.password.data, login_form.remember_me.data))
        user = User.query.filter_by(email=login_form.email.data, password=login_form.password.data).first()
        if user is None:
            flash('Login failed')
        else:
            login_user(user, remember=login_form.remember_me.data)
            if next_page is not None:
                return redirect(next_page)
            else:
                return redirect(url_for('default.index', is_login=True))
    return render_template('login.html', is_login=False, login_form=login_form)


@blueprint.route('/signup/', methods=['GET', 'POST'])
@anonymous_required
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        email = signup_form.email.data
        username = signup_form.username.data
        password = signup_form.password.data

        current_app.logger.info('signup: %s %s %s' % (email, username, password))
        if User.query.filter_by(email=signup_form.email.data).first() is None:
            # noinspection PyArgumentList
            user = User(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('You have registered.')
            return redirect(url_for('default.login'))
        else:
            flash('E-mail has been registered.')
    return render_template('signup.html', signup_form=signup_form)


@blueprint.route('/keyword/<string:word>', methods=['DELETE'])
@login_required
def remove_keyword(word):
    if request.method == 'DELETE':
        current_app.logger.info(word)
    return ""


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('default.login'))
