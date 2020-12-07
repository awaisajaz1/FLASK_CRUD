from os import environ, getenv

class Configs(object):
    #SECRET_KEY = environ.get('SECRET_KEY') #'iamtoosecret' for linux
    # SECRET_KEY = getenv("SECRET_KEY")
    # assert SECRET_KEY
    
    # database_user = getenv("database_user")#'root'
    # assert database_user
    # database_pwd = getenv("database_pwd")#'admin123'
    # assert database_pwd

    # database = getenv("database")#'target'
    # assert database

    # SECRET_KEY = getenv("SECRET_KEY")
    # assert SECRET_KEY
    SECRET_KEY = 'iamtoosecret'
    database_user = 'root'
    database_pwd = 'admin123'
    database = 'target'    
    SQLALCHEMY_DATABASE_URI = f'mysql://{database_user}:{database_pwd}@192.168.18.3/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
