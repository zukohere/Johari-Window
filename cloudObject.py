# method to obtain data from mongodb and convert to json file to be read by the word cloud.

def render_cloud_object():
    from flask import Flask, jsonify, request
    from flask_pymongo import PyMongo
    from config import mongodict
    from pymongo import MongoClient
    client = MongoClient()
    from collections import Counter

    # Define Johari adjectives
    Johari_adj = ["Able",
        "Accepting",
        "Adaptable",
        "Bold",
        "Brave",
        "Calm",
        "Caring",
        "Cheerful",
        "Clever",
        "Complex",
        "Confident",
        "Dependable",
        "Dignified",
        "Empathetic",
        "Energetic",
        "Extroverted",
        "Friendly",
        "Giving",
        "Happy",
        "Helpful",
        "Idealistic",
        "Independent",
        "Ingenious",
        "Intelligent",
        "Introverted",
        "Kind",
        "Knowledgeable",
        "Logical",
        "Loving",
        "Mature",
        "Modest",
        "Nervous",
        "Observant",
        "Organized",
        "Patient",
        "Powerful",
        "Proud",
        "Quiet",
        "Reflective",
        "Relaxed",
        "Religious",
        "Responsive",
        "Searching",
        "Self - assertive",
        "Self - conscious",
        "Sensible",
        "Sentimental",
        "Shy",
        "Silly",
        "Spontaneous",
        "Sympathetic",
        "Tense",
        "Trustworthy",
        "Warm",
        "Wise",
        "Witty"]
    # connect to database
    URI = f'mongodb+srv://{mongodict["username"]}:{mongodict["password"]}@cluster0.psrom.mongodb.net/Johari?retryWrites=true&w=majority'
    client = MongoClient(URI)
    db = client.Johari
    collection = db.Matt

    # complete list of records for subject and observers
    subj_list = [item for item in collection.find() if item["role"] == "Subject" ]
    obs_list = [item for item in collection.find() if item["role"] == "Observer"]

    # Aggregate all obs_list adjectives
    agg_obs_adj=[]
    for item in obs_list:
        for adj in item["adj_list"]:
            agg_obs_adj.append(adj)

    # Create Johari quadrants
    subj_adj=subj_list[0]["adj_list"]
    #Known to self, known to observer (Arena)
    Arena_list = [adj for adj in subj_adj if adj in agg_obs_adj]

    #Known to self, not known to observer (Facade)
    Facade_list = [adj for adj in subj_adj if adj not in agg_obs_adj]

    #Not Known to self, Known to observer (BlindSpot)
    BlindSpot_list = [adj for adj in agg_obs_adj if adj not in subj_adj]

    #Not known to self, not known to observer (Unknown)
    Unknown_list = [adj for adj in Johari_adj if adj not in subj_adj and adj not in agg_obs_adj]

    # Create dictionary of record lists to be jsonified for word cloud
    cloudData = {"Arena": [{"Adj": word, "Counts": Counter(Arena_list)[word], "Percent": Counter(Arena_list)[word]/len(obs_list)} for word in Counter(Arena_list).keys()],
             "Facade": [{"Adj": word, "Counts": Counter(Facade_list)[word], "Percent": Counter(Facade_list)[word]/len(obs_list)} for word in Counter(Facade_list).keys()],
             "BlindSpot": [{"Adj": word, "Counts":Counter(BlindSpot_list)[word], "Percent": Counter(BlindSpot_list)[word]/len(obs_list)} for word in Counter(BlindSpot_list).keys()],
             "Unknown": [{"Adj": word, "Counts": Counter(Unknown_list)[word], "Percent": Counter(Unknown_list)[word]/len(obs_list)} for word in Counter(Unknown_list).keys()]}
    return cloudData