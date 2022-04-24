from tools import *
from flask import Flask, request
from flask_cors import CORS


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
        for u, f, l, e, p, rs in [('admin','admin','admin','admin@localhost.com','password123',[ROLE_SUPER])]:
            r,e  = register_user(u,f,l,e,p,rs)
            if not r:
                raise ValueError(f'Could not set up user ({u}): '+ str(e))
    except Exception as e:
        return make_api_response('Failed to setup system: '+str(e), status=500)
    return make_api_response('Successfully setup system.')



@app.route('/auth/register', methods=['POST'])
def api_auth_register():

    return {}




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
