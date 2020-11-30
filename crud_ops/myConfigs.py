
class Configs(object):
    SECRET_KEY = 'iamtoosecret'
    database_user = 'root'
    database_pwd = 'admin123'
    database = 'target'
    SQLALCHEMY_DATABASE_URI = f'mysql://{database_user}:{database_pwd}@localhost/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
