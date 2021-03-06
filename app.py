from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
import bcrypt
from collections import Counter
from Johari_full_list import full_list

# set up flask app and MongoDB connections.
app = Flask(__name__)
app.secret_key = 'mysecret'
app.config['MONGO_DBNAME'] = 'Johari'
app.config["MONGO_URI"] = f'mongodb+srv://user:GjOlEBYy62570D2d@cluster0.psrom.mongodb.net/Johari?ssl=true&ssl_cert_reqs=CERT_NONE'

mongo_client = PyMongo(app)
db = mongo_client.db
@app.route('/')
def index():
    # if user is logged in, bring up the Johari window display page. Otherwise, bring up the login page.
    if 'username' in session:
        users = db.users
        subject_user=users.find_one({'name' : session['username']})
        return render_template('joharidsplay.html',username= session["username"], key= subject_user["share_key"])
    return render_template("index.html")
    

@app.route('/login', methods=['POST'])
def login():
    # check credentials to log the user in or return page with message about invalid credentials.
    users = db.users
    login_user = users.find_one({'name' : request.form['username']})
    
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            subject_user=users.find_one({'name' : session['username']})
            # if the user has no data to display from guest observers, let them know to share they're key. Otherwise, proceed to the window display.
            if 'guests' not in subject_user.keys():
                return render_template("newuser.html", new_username= session["username"], new_key= subject_user["share_key"]) 
            return render_template('joharidsplay.html',username= session["username"], key= subject_user["share_key"])
    
    error='Invalid username/password combination.'
    return render_template("message.html", message=error)

@app.route('/register', methods=['POST', 'GET'])
def register():
    # For when new user clicks to create an account. Check if username is in database, if not, create document for the new user.
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
            subject_user=users.find_one({'name' : session['username']})
            if 'guests' not in subject_user.keys():
                              
                return render_template("newuser.html", new_username= session["username"], new_key= subject_user["share_key"])

            return redirect(url_for('index'))
        
        error= 'That username already exists!'
        return render_template("message.html", message=error)

    return render_template('register.html')

@app.route('/guestform', methods=['POST', 'GET'])
def submit():
    # For when guests select option to submit data about a user. Check if user/key combo is good (subject_user will be None).
    # Obtain list JohariMongo from the form. and a  
    if request.method == 'POST':
        users = db.users
        subject_user = users.find_one({'name' : request.form['username'], 'share_key' : request.form['sharekey']})
        datalist=request.form.getlist("JohariMongo")
        guest_name = request.form['guestname']
        if subject_user is None:
            error = "Invalid username/key combination. Use your browser back button so you don't lose your data, and try again."
            return render_template("message.html", message=error)
        else:
            if 'guests' not in subject_user.keys():
                users.find_one_and_update({'name' : request.form['username'], 'share_key' : request.form['sharekey']}, 
                                 {"$set": {"guests": [{"name": guest_name, "guest_adj": datalist}]}})
            else:
                users.find_one_and_update({'name' : request.form['username'], 'share_key' : request.form['sharekey']}, 
                                 {"$push": {"guests": {"name": guest_name, "guest_adj": datalist}}})
            message='Data submitted! Thank you.'
            return render_template("message.html", message=message)
    return render_template('guestform.html')

@app.route('/get_johari_data/')
def johari():
    username = session['username']
    users = db.users
    subject_user = users.find_one({'name' : session['username']})
    they_see = []

    for i in range(len(subject_user["guests"])):
        for adj in subject_user["guests"][i]["guest_adj"]:
            they_see.append(adj)

    you_see = subject_user['user_adj']

    Arena = [{"adj": adj,"obsCount": Counter(they_see)[adj], "obsPercent": Counter(they_see)[adj]/len(subject_user["guests"])} for adj in you_see if adj in they_see]
    Facade = [{"adj": adj,"obsCount": len(subject_user["guests"]), "obsPercent": 1} for adj in you_see if adj not in they_see]
    Blindspot = [{"adj": adj,"obsCount": Counter(they_see)[adj], "obsPercent": Counter(they_see)[adj]/len(subject_user["guests"])} for adj in list(set(they_see)) if adj not in you_see]
    Unknown = [{"adj": adj,"obsCount": len(subject_user["guests"]), "obsPercent": 1} for adj in full_list if adj not in you_see if adj not in they_see]
    # Facade and unknown have different counts for every one that didn't see it.


    visdata = {"Username": username, 
                "Key": subject_user['share_key'],
                "num_obs": len(subject_user["guests"]),
                "Arena": Arena, 
                "Facade": Facade, 
                "Blindspot": Blindspot,
                "Unknown": Unknown}
    return jsonify(visdata)

@app.route("/guestremove", methods=['POST', 'GET'])
def remove_obs():
    username = session['username']
    users = db.users
    subject_user = users.find_one({'name' : session['username']})
    they_see = [] # this list will have duplicate entries since mult guests may choose same adj (trimmed for blindspot)
    allguests = []

    for i in range(len(subject_user["guests"])):
        allguests.append((i,subject_user["guests"][i]["name"],len(subject_user["guests"][i]["guest_adj"])))

    if request.method == 'POST':
        remove_list=[int(i) for i in request.form.getlist("removeList")]
        trimmed_guest_list = [subject_user["guests"][i] for i in range(len(subject_user["guests"])) if i not in remove_list]
        users.update({'name' : session['username']},{"$set": {"guests": trimmed_guest_list}})
        return render_template("message.html", message="Removal complete. Log out and Log back in to continue.")

    return render_template('guestremove.html',allGuests=allguests)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)