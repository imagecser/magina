import random
import string


class Config:
    CANDIDATE_WORDS = ['通知', '考试', '六级', '悦读经典', '大类', '创新创业', '停调课', '推免生', '社会实践', '社团']

    SECRET_KEY = ''.join(random.sample(string.ascii_letters + string.digits, k=20))
    CSRF_SESSION_KEY = ''.join(random.sample(string.ascii_letters + string.digits, k=20))
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 2

    SCHEDULER_TIMER = 60 * 30

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
    DEBUG = False
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/magina?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    SERVER_DOMAIN_NAME = 'http://114.212.238.98'
    SQLALCHEMY_ECHO = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/magina?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ContextConfig(DevelopmentConfig):
    SERVER_DOMAIN_NAME = 'http://magina.zsuun.com'
    DEBUG = False


config = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
    'ctx': ContextConfig
}
