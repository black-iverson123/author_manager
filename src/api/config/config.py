class config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(config):
    SQLALCHEMY_DATABASE_URI = "Production DB URL"

class DevelopmentConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:csb_005813@localhost:3306/testdb"
    SECRET_KEY = 'TdyTf-GeiAP523DL1hFKtBcFKFReX-GmNWe1mk0tudo8TsNqhu6yaHD2Ud-axkYArqkZ13-KxKOTn5OjiH5v1g'
    JWT_SECRET_KEY = 'TdyTf-GeiAP523DL1hFKtBcFKFReX-GmNWe1mk0tudo8TsNqhu6yaHD2Ud-axkYArqkZ13-KxKOTn5OjiH5v1g'
    SECURITY_PASSWORD_SALT = '?/#'
    MAIL_DEFAULT_SENDER = "maxwelladebowale6@gmail.com"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "maxwelladebowale6@gmail.com"
    MAIL_PASSWORD = "pduy ebud itaz hdta"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    UPLOAD_FOLDER = 'images'

class TestingConfig(config):
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = "Testing DB URL"
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = "JWT-SECRET"
    SECRET_KEY = "SECRET-KEY"
    SECURITY_PASSWORD_SALT = "SECURITY-PASSWORD-SALT"
    MAIL_DEFAULT_SENDER = ""
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    UPLOAD_FOLDER = 'images'