from flask import Flask, request
from flask_cors import CORS
import json
from config import ConfigStorage
from data_base_model import DataBaseAdaptor
import tokenizer

app = Flask(__name__)
# Allow cross domain
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


crawler_config = ConfigStorage('/var/www/html/VHFind/Backend/app.ini')
db_adaptor = DataBaseAdaptor(crawler_config.get_config_section('postgresql'))


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def empty_request():
    return json.dumps(
        {
            'status': 200,
            'data': 'REST API IS WORKING'
        }
    )


@app.route('/find', methods=['GET', 'POST', 'OPTIONS'])
def find():
    if request.method == 'POST':
        tokens = request.json['query'].split()
        return json.dumps(
            {
                'status': 200,
                'data': db_adaptor.find_query(tokens)
            }
        )
    return ''


@app.route('/<access_token>/find', methods=['GET', 'POST', 'OPTIONS'])
def find_signed(access_token):
    if request.method == 'POST':
        user = db_adaptor.get_user_by_token(access_token)
        print(user)
        tokens = request.json['query'].split()
        db_adaptor.save_history(user, request.json['query'])
        return json.dumps(
            {
                'status': 200,
                'data': db_adaptor.find_query(tokens)
            }
        )
    return ''


@app.route('/sign/in', methods=['GET', 'POST', 'OPTIONS'])
def sign_in():
    if request.method == 'POST':
        uid, email, password, salt = db_adaptor.get_by_email(request.json['email'])
        if tokenizer.get_hash(request.json['password'], salt) == password:
            token = db_adaptor.new_session(uid, tokenizer.generate_token(100))
            return json.dumps(
                {
                    'status': 200,
                    'data': token
                }
            )
    return ''


@app.route('/sign/up', methods=['GET', 'POST', 'OPTIONS'])
def sign_up():
    if request.method == 'POST':
        salt = tokenizer.gen_salt(10)
        user_id = db_adaptor.sign_up(
            request.json['name'],
            request.json['last_name'],
            request.json['email'],
            request.json['age'],
            tokenizer.get_hash(request.json['password'], salt),
            salt
        )
        if user_id == 0:
            return {
                'status': 400,
                'data': ''
            }
        return json.dumps(
            {
                'status': 200,
                'data': ''
            }
        )
    return ''


@app.route('/<access_token>/sign/out', methods=['POST', 'OPTIONS'])
def sign_out(access_token):
    return json.dumps(
        {
            'status': 200,
            'data': ''
        }
    )


@app.route('/<access_token>/history', methods=['GET', 'OPTIONS'])
def history(access_token):
    return json.dumps(
        {
            'status': 200,
            'data': ''
        }
    )


if __name__ == '__main__':
    app.run()
