import logging
from os import path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from db.db_login.login_data_manage import init_login_info, get_admin

log = logging.getLogger(__name__)


def db_create():
    if not path.isfile('db_login/credentials/key.key'):
        if not init_login_info():
            log.exception('No key file!')
    admin_login_data = get_admin()
    u = admin_login_data['user']
    pd = admin_login_data['passwd']
    h = admin_login_data['host']
    pt = admin_login_data['port']
    dbs = admin_login_data['db']
    url = f"postgresql://{u}:{pd}@{h}:{pt}/{dbs}"
    if database_exists(url):
        log.exception('Database already exists!')
    else:
        create_database(url)
        log.info("Database created")


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
    admin_login_data = get_admin()
    if not all(key in keys for key in admin_login_data.keys()):
        log.exception('Bad config file')
    return get_engine(
        admin_login_data['user'],
        admin_login_data['passwd'],
        admin_login_data['host'],
        admin_login_data['port'],
        admin_login_data['db'],
        )


def get_engine(user, passwd, host, port, dbs):
    # get sqlalchemy engine
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{dbs}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


db = get_database()
Base = declarative_base()
