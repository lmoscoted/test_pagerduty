from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(path.dirname(basedir), '.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{environ.get('DATABASE_USER')}:{environ.get('DATABASE_PASSWORD')}@" \
                              f"db:{environ.get('DATABASE_PORT')}/{environ.get('MYSQL_DATABASE')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGERDUTY_API_KEY = environ.get('PAGERDUTY_API_KEY')
    REFRESH_DATA_RATE = int(environ.get('REFRESH_DATA_RATE')) 
    PAGER_DUTY_URL = environ.get('BASE_URL') 
    DEBUG_MODE = True if environ.get('FLASK_ENV') == 'development' else False 