import logging
from os import path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db.db_login.login_data_manage import get_user

log = logging.getLogger(__name__)


def get_database():
    # connect to db
    try:
        engine = get_engine_from_settings()
        log.info("Connected to db")
    except IOError:
        log.exception("Failed connection")
        return None, 'fail'
    return engine


def get_engine_from_settings():
    keys = ['user', 'passwd', 'host', 'port', 'db']
    user_login_data = get_user()
    if not all(key in keys for key in user_login_data.keys()):
        log.exception('Bad config file')
    return get_engine(
        user_login_data['user'],
        user_login_data['passwd'],
        user_login_data['host'],
        user_login_data['port'],
        user_login_data['db'],
        )


def get_engine(user, passwd, host, port, dbs):
    # get sqlalchemy engine
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{dbs}"
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


def get_session():
    # creates user session
    engine = get_engine_from_settings()
    new_session = sessionmaker(bind=engine)()
    return new_session


db = get_database()
session = get_session()
Base = declarative_base()
