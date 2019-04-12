from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
import mongo

app = Flask(__name__)


app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_database'

mongo = PyMongo(app) 

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index_user.html',user_name = session['email'])

    return render_template('index.html',message = '')

    
@app.route('/dashboard/<user_hash>')
def personal_dashboard_route(user_hash):
    return render_template('dashboard.html', user_hash=user_hash)


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    user = users.find_one({'user_email': request.form['email']})
    
    if user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), user['user_password']) == user['user_password']:
            session['email'] = request.form['email']
            return redirect(url_for('personal_dashboard_route',user_hash=user['hash_id']))

    return render_template('index.html',message = 'Identifiants inconnus, inscrivez-vous !',test= user)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'user_email' : request.form['email']})

        if existing_user is None:
            DB = mongo.Mongo()
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            DB.add_user(request.form['email'])
            
            users.insert_one({'name':request.form['username'], 'password': hashpass})
            session['username'] =  request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)