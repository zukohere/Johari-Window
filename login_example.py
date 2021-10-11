from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
import bcrypt
from collections import Counter
from johari_dict import johari_dict

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Johari'
app.config["MONGO_URI"] = f'mongodb+srv://user:GjOlEBYy62570D2d@cluster0.psrom.mongodb.net/Johari?ssl=true&ssl_cert_reqs=CERT_NONE'

mongo_client = PyMongo(app)
db = mongo_client.db
@app.route('/')
def index():
    if 'username' in session:
        # return 'You are logged in as ' + session['username']
        return render_template('draft_index.html')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            datalist=request.form.getlist("JohariMongo")
            users.insert({'name' : request.form['username'], 
            'password' : hashpass, 
            'share_key': request.form['sharekey'], 
            'user_adj': datalist,
            'guests': {}})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')
@app.route('/guestform', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        users = db.users
        subject_user = users.find_one({'name' : request.form['username'], 'share_key' : request.form['sharekey']})
        datalist=request.form.getlist("JohariMongo")
        guest_name = request.form['guestname']
        if subject_user is None:
            return 'Invalid username/key combination.'
        else:
            subject_user["guests"]
            users.find_one_and_update({'name' : request.form['username'], 'share_key' : request.form['sharekey']}, 
                                 {"$set": {"guests": [subject_user["guests"],{"name": guest_name, "guest_adj": datalist}]}})
            return "Data submitted! Thank you."
    return render_template('guestform.html')

@app.route('/get_johari_data/')
@app.route('/get_johari_data/<username>')
def johari(username=None):
    username = session['username']
    users = db.users
    subject_user = users.find_one({'name' : session['username']})
    johariadj_consol = [ ]
    for i in range(len(subject_user["guests"])):
        for adj in subject_user["guests"][i]["guest_adj"]:
            johariadj_consol.append(adj)
    return jsonify(Counter(johariadj_consol))



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)