import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'supersecretkey'
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
    SESSION_COOKIE_SECURE = False
    DEFAULT_THEME = 'light'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
