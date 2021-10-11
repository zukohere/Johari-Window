def johari_dict(username, users):
        subject_user = users.find_one({'name' : session['username']})
        johariadj_consol = [ adj for adj in subject_user["guests"][i]["guest_adj"] for i in len(subject_user["guests"])-1  ]
        return Counter(johariadj_consol)