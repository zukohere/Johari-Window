from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
import bcrypt
from collections import Counter
from Johari_full_list import full_list

app = Flask(__name__)
app.secret_key = 'mysecret'
app.config['MONGO_DBNAME'] = 'Johari'
app.config["MONGO_URI"] = f'mongodb+srv://user:GjOlEBYy62570D2d@cluster0.psrom.mongodb.net/Johari?ssl=true&ssl_cert_reqs=CERT_NONE'

mongo_client = PyMongo(app)
db = mongo_client.db
@app.route('/')
def index():
    if 'username' in session:
        return render_template('joharidsplay.html')
    return render_template("index.html")
    

@app.route('/login', methods=['POST'])
def login():
    users = db.users
    login_user = users.find_one({'name' : request.form['username']})
    

    if login_user:
        # subject_user = users.find_one({'name' : session['username']})
        
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return render_template('joharidsplay.html')
    
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
            })
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
            if 'guests' not in subject_user.keys():
                users.find_one_and_update({'name' : request.form['username'], 'share_key' : request.form['sharekey']}, 
                                 {"$set": {"guests": [{"name": guest_name, "guest_adj": datalist}]}})
            else:
                users.find_one_and_update({'name' : request.form['username'], 'share_key' : request.form['sharekey']}, 
                                 {"$push": {"guests": {"name": guest_name, "guest_adj": datalist}}})
            return "Data submitted! Thank you."
    return render_template('guestform.html')

@app.route('/get_johari_data/')
def johari():
    username = session['username']
    users = db.users
    subject_user = users.find_one({'name' : session['username']})
    they_see = [ ]
    if subject_user['guests']=={}:
            return f"""You are logged in as but there is nothing to visualize! 
            Share your uasername/key and have others fill out the form about you to get data.
            Username: {session['username']}
            Key: {subject_user['share_key']}"""
    else: 
        for i in range(len(subject_user["guests"])):
            for adj in subject_user["guests"][i]["guest_adj"]:
                they_see.append(adj)
    
        you_see = subject_user['user_adj']

        Arena = [{"adj": adj,"obsCount": Counter(they_see)[adj], "obsPercent": Counter(they_see)[adj]/len(subject_user["guests"])} for adj in you_see if adj in they_see]
        Facade = [{"adj": adj,"obsCount": len(subject_user["guests"]), "obsPercent": 1} for adj in you_see if adj not in they_see]
        Blindspot = [{"adj": adj,"obsCount": Counter(they_see)[adj], "obsPercent": Counter(they_see)[adj]/len(subject_user["guests"])} for adj in they_see if adj not in you_see]
        Unknown = [{"adj": adj,"obsCount": len(subject_user["guests"]), "obsPercent": 1} for adj in full_list if adj not in you_see if adj not in they_see]
        # Facade and unknown have different counts for every one that didn't see it.


        visdata = {"Username": username, 
                    "num_obs": len(subject_user["guests"]),
                    "Arena": Arena, 
                    "Facade": Facade, 
                    "Blindspot": Blindspot,
                    "Unknown": Unknown}
        return jsonify(visdata)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)