from flask import make_response
from constants import *
import psycopg
import hashlib
import secrets

def make_api_response(msg='', data=None, status=200, new_token=None):
    return make_response({
        'msg':msg,
        'data':data,
        'status':status,
        'new_token':new_token
    }), status

def register_user(username, first_name, last_name, email, password, roles=[ROLE_USER]):
    try:
        with psycopg.connect(
            host = POSTGRES_HOST,
            user=POSTGRES_USER,
            password=POSTGRES_PASS
        ) as conn:
            hashed_password, salt = salt_password(password)
            conn.execute('INSERT INTO users (username, first_name, last_name, email, password, salt) VALUES '
                         '(%s, %s, %s, %s, %s, %s)',
                         (username, first_name, last_name, email, hashed_password, salt))
        return True, None
    except Exception as e:
        return False, e

def salt_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(64)
    hashed_password = hashlib.pbkdf2_hmac(
        'sha3_512',
        password.encode(),
        salt.encode(),
        100000
    ).hex()
    return hashed_password, salt