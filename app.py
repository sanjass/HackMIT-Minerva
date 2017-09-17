from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
mysql = MySQL()

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'matematika4'
app.config['MYSQL_DATABASE_DB'] = 'letspset_sanja'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
@app.route("/")
def main():
	return render_template('index.html')

@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/signup")
def signup():
	 
	return render_template('signup.html')

@app.route("/signUp",methods=['POST','GET'])
def signUp():
	try:
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']

		# validate the received values
		if _name and _email and _password:
			
			# All Good, let's call MySQL
			
			conn = mysql.connect()
			cursor = conn.cursor()
			_hashed_password = generate_password_hash(_password)
			cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				console.log("user created!")
				return json.dumps({'message':'User created successfully !'})
			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})

	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close() 
		conn.close()

@app.route("/signin")
def signin():
	return render_template('signin.html')


@app.route("/signIn",methods=['POST'])
def signIn():
	# read the posted values from the UI
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
	# validate the received values
	if _email and _password:
		return json.dumps({'html':'<span>All fields good for sign in !!</span>'})
	else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})
@app.route("/profile")
def profile():
	return render_template('profile.html')

if __name__ == "__main__":
	app.run(debug=True, port=2000)