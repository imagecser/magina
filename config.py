import random
import string


class Config:

    SECRET_KEY = ''.join(random.sample(string.ascii_letters + string.digits, k=20))
    CSRF_SESSION_KEY = ''.join(random.sample(string.ascii_letters + string.digits, k=20))
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 2

    SCHEDULER_TIMER = 60

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    try:
        from config_secret import MAIL_DEFAULT_SENDER, MAIL_PASSWORD, MAIL_USERNAME
    except ImportError:
        MAIL_USERNAME = 'mail_username'
        MAIL_PASSWORD = 'mail_password'
        MAIL_DEFAULT_SENDER = 'default_sender'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # TEMPLATES_AUTO_RELOAD = True
    SERVER_DOMAIN_NAME = 'http://localhost'
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/magina?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config = {
    'dev': DevelopmentConfig
}
