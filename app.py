from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from config import mongodict
from cloudObject import render_cloud_object

# Flask Setup
app = Flask(__name__, static_url_path='/static')

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = f'mongodb+srv://{mongodict["username"]}:{mongodict["password"]}@cluster0.psrom.mongodb.net/Johari?retryWrites=true&w=majority'
mongo_client = PyMongo(app)
db = mongo_client.db


# app routes
@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        datalist=request.form.getlist("JohariAdj")
    
        # try:
        mongo_data_push = {"name": datalist[0],
                        "role": datalist[1],
                        "adj_list": datalist[2:]}
        # except:
        #     mongo_data_push = {"name": datalist[0],
        #                     "role": datalist[1],
        #                     "adj_list": []}
        print(mongo_data_push)
        db.Matt.insert_one(mongo_data_push)
        print("done")
    return render_template("index.html")

# @app.route('/get_cloud_data/')
# def get_cloud_data():
#     # render a json file from the mongodb data. using a function defined elsewhere.
#     return(jsonify(render_cloud_object))
if __name__ == "__main__":
    app.run(debug=True)
