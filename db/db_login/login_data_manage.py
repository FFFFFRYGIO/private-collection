import os
import pickle
from cryptography.fernet import Fernet
from decouple import config

def write_key(key_file):
    key = Fernet.generate_key()
    with open(key_file, "wb") as kf:
        kf.write(key)


def load_key(key_file):
    with open(key_file, "rb") as kf:
        key = kf.read()
    return key


def export_login_data(login_data, file, key_file):
    with open(file, "wb") as f:
        fer = Fernet(load_key(key_file))
        enc = fer.encrypt(login_data['passwd'].encode()).decode()
        login_data['passwd'] = enc
        pickle.dump(login_data, f)  # read dict from file


def import_login_data(file, key_file):
    with open(file, "rb") as f:
        login_data = pickle.load(f)  # read dict from file
        fer = Fernet(load_key(key_file))
        dec = fer.decrypt(login_data['passwd'].encode()).decode()
        login_data['passwd'] = dec
    return login_data


def init_login_info(admin_file="db/db_login/admin", user_file="db/db_login/user", key_file="db/db_login/key.key"):
    if config('radek'):
        base_login = {
            'user': None,
            'passwd': None,
            'host': config('host', default='localhost'),
            'port': config('port', cast=int),
            'db': config('db'),
        }

        admin_login = base_login.copy()
        admin_login['user'] = config('admin_user')
        admin_login['passwd'] = config('admin_password')

        user_login = base_login.copy()
        user_login['user'] = config('user_user')
        user_login['passwd'] = config('user_password')
    else:
        raise EnvironmentError("Can't find proper .env file")

    try:
        write_key(key_file)
        export_login_data(user_login, user_file, key_file)
        export_login_data(admin_login, admin_file, key_file)
        return True
    except Exception as e:
        print(e)
        return False


def get_user(user_file="db/db_login/user", key_file="db/db_login/key.key"):
    user_data = import_login_data(user_file, key_file)
    return user_data


def get_admin(admin_file="db/db_login/admin", key_file="db/db_login/key.key"):
    admin_data = import_login_data(admin_file, key_file)
    return admin_data
