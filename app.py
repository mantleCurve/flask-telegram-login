from flask import Flask, render_template, request,jsonify,redirect
from flask_login import LoginManager, UserMixin
import hashlib
import hmac
import base64

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']


@app.route('/')
def index():
	data = {'bot_name': app.config['BOT_NAME'], 'bot_domain': app.config['BOT_DOMAIN']}
	return render_template('index.html',data = data)

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

def string_generator(data_incoming):
	data = data_incoming.copy()
	del data['hash']
	keys = sorted(data.keys())
	string_arr = []
	for key in keys:
		string_arr.append(key+'='+data[key])
	string_cat = '\n'.join(string_arr)
	return string_cat

@app.route('/login')
def login():
	tg_data = {
		"id" : request.args.get('id',None),
		"first_name" : request.args.get('first_name',None),
		"last_name" : request.args.get('last_name', None),
		"username" : request.args.get('username', None),
		"auth_date":  request.args.get('auth_date', None),
		"hash" : request.args.get('hash',None)
	}
	data_check_string = string_generator(tg_data)
	secret_key = hashlib.sha256(app.config['BOT_TOKEN'].encode('utf-8')).digest()
	secret_key_bytes = secret_key
	data_check_string_bytes = bytes(data_check_string,'utf-8')
	hmac_string = hmac.new(secret_key_bytes, data_check_string_bytes, hashlib.sha256).hexdigest()
	if hmac_string == tg_data['hash']:
		return redirect('/dashboard')
	
	return jsonify({
				'hmac_string': hmac_string,
				'tg_hash': tg_data['hash'],
				'tg_data': tg_data
	})


if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True, port=8080)