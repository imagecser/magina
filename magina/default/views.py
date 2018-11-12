import random
import string
from datetime import timedelta
from functools import wraps

from flask import render_template, request, current_app, redirect, flash, url_for
from flask_login import login_required, login_user, current_user, logout_user
from flask_mail import Message

from magina import mail
from magina.models import User, EmailActive
from . import blueprint
from .forms import LoginForm, SignupForm, KeywordForm


@blueprint.route('/test/')
def test():
    return ""


def anonymous_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You have logged-in.')
            return redirect(url_for('default.index'))
        else:
            return func(*args, **kwargs)

    return decorated_view


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    keyword_form = KeywordForm()
    words_to_show = [keyword.word for keyword in current_user.keywords]
    if keyword_form.validate_on_submit():
        _keyword = keyword_form.keyword.data
        if _keyword in words_to_show:
            flash('You have added the keyword before.')
        else:
            current_user.save_keyword(_keyword)

    return render_template('home.html', is_login=True, keyword_form=keyword_form,
                           enumerate_words=enumerate(words_to_show))


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
            flash('Login failed.')
        elif not user.email_active.is_active:
            flash('Your account has not been activated.')
        else:
            login_user(user, remember=login_form.remember_me.data, duration=timedelta(hours=2))
            if next_page is not None:
                return redirect(next_page)
            else:
                return redirect(url_for('default.index'))
    return render_template('login.html', is_login=False, login_form=login_form)


@blueprint.route('/signup/', methods=['GET', 'POST'])
@anonymous_required
def signup():
    signup_form = SignupForm()
    on_active = False
    if signup_form.is_submitted():
        current_app.logger.info(signup_form.email.data)
        email = signup_form.email.data
        username = signup_form.username.data
        password = signup_form.password.data

        current_app.logger.info('signup: %s %s %s' % (email, username, password))
        if User.query.filter_by(email=email).first() is None:
            # noinspection PyArgumentList
            user_id = User.save_user(User(email=email, username=username, password=password))
            active_code = ''.join(random.sample(string.ascii_letters + string.digits, k=24))
            User.save_email_active(EmailActive(user_id=user_id, is_active=False, active_code=active_code))
            message = Message(
                subject='Activate Your E-mail#%s' % ''.join(random.sample(string.ascii_letters, k=3)),
                body='Your activate link: %s%s?id=%s&code=%s' % (
                    current_app.config['SERVER_DOMAIN_NAME'], url_for('default.activate'), user_id, active_code),
                recipients=[email]
            )
            # noinspection PyBroadException
            try:
                mail.send(message=message)
                on_active = True
            except Exception:
                User.delete_user(user_id)
                flash('Send verification email failed.')
                pass
        else:
            flash('E-mail has been registered.')
    return render_template('signup.html', signup_form=signup_form, on_active=on_active)


@blueprint.route('/keyword/<string:word>', methods=['DELETE', 'POST'])
@login_required
def remove_keyword(word):
    if request.method == 'DELETE':
        current_user.delete_keyword_by_word(word)
        return ''
    elif request.method == 'POST':
        current_app.logger.info("post %s" % word)
        if not current_user.save_keyword(word):
            return 'err'
        else:
            return ''


@blueprint.route('/activate/')
@anonymous_required
def activate():
    user_id = request.args.get('id')
    active_code = request.args.get('code')
    if user_id is None or active_code is None:
        flash('Invalid url.')
    else:
        email_active_row = EmailActive.query.filter_by(user_id=user_id, active_code=active_code).first()
        if email_active_row is None:
            flash('Url not matches.')
        elif email_active_row.is_active:
            flash('Account has been activated before.')
        else:
            email_active_row.set_active(True)
            email_active_row.user.save_keyword('通知')
            flash('You have active your account: %s' % email_active_row.user.email)

    return render_template('active.html')


@blueprint.route('/password/')
@anonymous_required
def set_password():
    pass


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('default.login'))
