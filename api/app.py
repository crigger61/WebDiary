from tools import *
from flask import Flask, request
from flask_cors import CORS
from flask.app import BadRequest

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def api_index():
    return make_api_response('Success.', {'API_Version':API_VERSION, 'Application_Name':'WebDiary'})



@app.route('/system/setup', methods=['GET'])
def api_system_setup():
    try:
        with psycopg.connect(
                host=POSTGRES_HOST,
                user=POSTGRES_USER,
                password=POSTGRES_PASS
        ) as conn:
            conn.execute(open('make_db.sql','r').read())
        r, e = register_user('admin','admin','admin','admin@localhost.com',SERVER_DEFAULT_ADMIN_PASSWORD,[ROLE_SUPER])
        if not r:
            raise e

    except Exception as e:
        return make_api_response('Failed to setup system: '+str(e), status=500)
    return make_api_response('Successfully setup system.')



@app.route('/auth/register', methods=['POST'])
def api_auth_register():
    user_json = None
    try:
        user_json = request.json
        for req in ['username', 'first_name', 'last_name', 'email', 'password', 'password_confirm']:
            if req not in user_json:
                raise SyntaxError(f'Missing {req} in user json.')
        user_username = user_json['username']
        user_first_name = user_json['first_name']
        user_last_name = user_json['last_name']
        user_email = user_json['email']
        user_password = user_json['password']
        user_password_confirm = user_json['password_confirm']

        if user_password != user_password_confirm:
            raise ValueError('Make sure the passwords match.')

        result, exc = register_user(user_username, user_first_name, user_last_name, user_email, user_password)
        if not result:
            raise exc
        else:
            return make_api_response('Successfully created user.', data=user_json, new_token='abc')
    except BadRequest as e:
        return make_api_response('There was an error creating the user: '
                                 'Make sure to include a json object with the required fields.', status=400)
    except (SyntaxError, ValueError) as e:
        return make_api_response('There was an error creating the user: ' + str(e), status=400)
    except Exception as e:
        return make_api_response('There was an error creating the user: ' + repr(e), status=400)




@app.route('/echo')
def echo():
    return {'args':request.args}
@app.route('/test')
def test():
    with psycopg.connect(
        host=POSTGRES_HOST,
        user=POSTGRES_USER,
        password=POSTGRES_PASS
    ) as conn:
        return {'t1':len(secrets.token_hex(64))}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
