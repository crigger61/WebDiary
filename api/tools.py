from flask import make_response, request
from constants import *
import psycopg
import hashlib
import secrets
import re
import jwt
import time

def make_api_response(msg='', data=None, status=200, new_token=None):
    return make_response({
        'msg':msg,
        'data':data,
        'status':status,
        'new_token':new_token,
        '_time': int(time.time()),
        '_path': request.path,
        '_cur_token': request.headers.get(JWT_HEADER, '')
    }), status

def generate_jwt_for_user(username):
    with psycopg.connect(
            host = POSTGRES_HOST,
            user=POSTGRES_USER,
            password=POSTGRES_PASS
    ) as conn:
        cur = conn.cursor()
        cur.execute('SELECT role FROM user_roles WHERE username=%s', (username,))
        result_set = cur.fetchall()
        roles = [row[0] for row in result_set]
    return jwt.encode({
        'username': username,
        'iss': int(time.time()),
        'exp': int(time.time() + JWT_TTE),
        'nonce': secrets.token_urlsafe(32),
        'roles': roles
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)

def register_user(username, first_name, last_name, email, password, roles=[ROLE_USER]):
    try:
        if not check_username(username):
            raise ValueError('Make sure the username matches the required formatting.')
        if not check_name(first_name):
            raise ValueError('Make sure the first name matches the required formatting.')
        if not check_name(last_name):
            raise ValueError('Make sure the last name matches the required formatting.')
        if not check_email(email):
            raise ValueError('Make sure the email matches the required formatting.')
        if not check_password(password):
            raise ValueError('Make sure the password matches the required formatting.')

        with psycopg.connect(
            host = POSTGRES_HOST,
            user=POSTGRES_USER,
            password=POSTGRES_PASS
        ) as conn:
            cur = conn.cursor()
            hashed_password, salt = salt_password(password)
            cur.execute('INSERT INTO users (username, first_name, last_name, email, password, salt) VALUES '
                         '(%s, %s, %s, %s, %s, %s)',
                         (username, first_name, last_name, email, hashed_password, salt))
            for role in roles:
                cur.execute('INSERT INTO user_roles (username, role) VALUES (%s, %s)', (username, role))
        return True, None
    except psycopg.errors.UniqueViolation as e:
        raise ValueError('That username already exists in the system.')
    except Exception as e:
        return False, e

def login_user(username, password):
    try:
        with psycopg.connect(
            host=POSTGRES_HOST,
            user=POSTGRES_USER,
            password=POSTGRES_PASS
        ) as conn:
            cur = conn.cursor()
            if not check_username(username):
                raise ValueError('Make sure the username matches an existing user.')
            cur.execute('SELECT user_id, salt FROM users WHERE username=%s', (username,))
            result_set = cur.fetchall()
            if len(result_set) != 1:
                raise ValueError('Make sure the username matches an existing user.')
            user_id = result_set[0][0]
            salt = result_set[0][1]

            if not check_password(password):
                raise ValueError('Make sure the password matches for an existing user.')
            hashed_password, _ = salt_password(password, salt)
            cur.execute('SELECT 1 FROM users WHERE username=%s AND password=%s', (username, hashed_password))
            result_set = cur.fetchall()
            if len(result_set) != 1:
                raise ValueError('Make sure the password matches for an existing user.')
        return True, None
    except Exception as e:
        return False, e

def salt_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(64)
    hashed_password = hashlib.pbkdf2_hmac(
        'sha3_512',
        password.encode(),
        (salt + SERVER_PEPPER).encode(),
        100000
    ).hex()
    return hashed_password, salt

def check_username(username):
    return re.fullmatch(r'[a-zA-Z0-9\-\_]{4,32}', username) is not None
def check_name(name):
    return re.fullmatch(r'[a-zA-Z0-9\-]{0,32}', name) is not None
def check_email(email):
    return re.fullmatch(r'[a-zA-Z\.\-]+@([a-zA-Z\-]+\.)+[a-zA-Z\-]+', email) is not None and len(email) <= 64
def check_password(password):
    pattern_count = 0
    for pattern in [r'[a-z]', r'[A-Z]', r'[0-9]', r'[!@#$%^&*()_\-+=\[\]{}:;\"\'<>,\.?/\\|`~]']:
        if re.search(pattern, password):
            pattern_count += 1
    return pattern_count >= 3 and (8 <= len(password) <= 128)