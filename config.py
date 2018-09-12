import random
import string


class Config:
    SECRET_KEY = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    CSRF_SESSION_KEY = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 2

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # TEMPLATES_AUTO_RELOAD = True
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/magina?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config = {
    'dev': DevelopmentConfig
}
