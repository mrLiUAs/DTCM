import os
import datetime
import random
import requests
from PIL import Image
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort
from flask import render_template, url_for, redirect, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from mail import send_mail
import dia
# from AI import diagnose

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

ccs = dict(mongo.db.cc.find_one({"_id": ObjectId(os.getenv("CC"))}))
ccs.pop("_id")

ccs_dict = {}
for v in ccs.values():
    for name, ins in v.items():
        ccs_dict[name] = ins

def gen_naming(l: list) -> dict:
    naming = {}
    num = 1
    for i in l:
        naming[i] = "sick-" + str(num)
        num += 1

    return naming

def generate_room():
    room = str(random.randint(0, 99999))
    room = '0'*(5-len(room)) + room
    return room

@app.route("/", methods=["GET", "POST"])
def index():
    room = request.args.get("room")
    name = request.args.get("name")
    doc = request.args.get("doctor")
    if name != None and doc == None:
        mongo.db.users.update_one({"username": name}, {"$set": {"oncall": False}})
    if room == None:
        return redirect(url_for("login"))
    else:
        if name != None and doc != None:
            return render_template("index.html", room=room, patientName=name, doctorName=doc)
        return render_template("index.html", room=room, patientName="None", doctorName="None")

@app.route("/data", methods=["POST"])
def data():
    if request.method == "POST":
        print(request.get_json())
    return "ok"

@app.route("/ttt", methods=["GET", "POST"])
def ttt():
    return render_template("ttt.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/api/login", methods=["POST"])
def api_login():
    username = request.json.get("username")

    user = mongo.db.users.find_one({"username": username})
    if user:
        return jsonify({"message": "Login successful"})
        
    else:
        return jsonify({"message": "Invalid credentials"})

@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")

@app.route("/api/signup", methods=["POST"])
def api_signup():
    try:
        req = dict(request.get_json())
        data = {}
        data["username"] = req["username"]
        req.pop("username")
        data["email"] = req["email"]
        req.pop("email")
        data["info"] = req

        data["oncall"] = False
        data["doctor"] = "None"
        data["room"] = "None"

        data["cc"] = []
        data["dcc"] = []

        mongo.db.users.insert_one(data)

        print("User added", data)

        return jsonify({"message": "ok"})
    except:
        return abort(404)


@app.route("/mode", methods=["GET", "POST"])
def mode():
    return render_template("mode.html", patientName=request.args.get("name"))

@app.route("/ai", methods=["GET", "POST"])
def ai():
    return render_template("ai.html", patientName=request.args.get("name"))
    
@app.route("/doctor", methods=["GET", "POST"])
def doctor():
    if request.args.get("name") == None:
        return redirect(url_for("doctor_login"))
    return render_template("doctor.html", doctorName=request.args.get("name"))

@app.route("/doctor_login", methods=["GET", "POST"])
def doctor_login():
    return render_template("doctor_login.html")

@app.route("/api/doctor_login", methods=["POST"])
def api_doctor_login():
    username = request.json.get("username")

    user = mongo.db.doctors.find_one({"username": username})
    if user:
        return jsonify({
            "message": "Login successful",
            "doctorName": user["username"]
            })
        
    else:
        return jsonify({"message": "Invalid credentials"})
    
@app.route("/api/get_patient", methods=["GET"])
def api_get_patient():
    try:
        doc = mongo.db.doctors.find_one({"username": request.args.get("name")})
        return jsonify({
            "patients": list(doc["patients"]),
            "online": doc["online"]
                        })
    except:
        return abort(404)

@app.route("/api/delete_patient", methods=["GET"])
def api_delete_patient():
    try:
        patient = request.args.get("patient")
        # doctor = request.args.get("doctor")
        # mongo.db.doctors.update_one({"username": doctor}, {"$set": {"patients": patient}})
        doctor = mongo.db.users.find_one({"username": patient})["doctor"]
        pp = mongo.db.doctors.find_one({"username": doctor})["patients"]

        for p in pp:
            if p["name"] == patient:
                pp.remove(p)
                break
        print(pp)
        mongo.db.doctors.update_one({"username": doctor}, {"$set": {"patients": pp}})
        mongo.db.users.update_one({"username": patient}, {"$set": {"doctor": "None"}})
        return jsonify({"message": "ok"})
    except:
        return abort(404)

@app.route("/api/online", methods=["GET"])
def api_online():
    try:
        mongo.db.doctors.update_one({"username": request.args.get("name")}, {"$set": {"online": (request.args.get("online") == 'true')}})
        return jsonify({"message": "ok"})
    except:
        return abort(404)
    
@app.route("/api/match_doctor", methods=["GET"]) # match and get doctor
def api_match_doctor():
    name = request.args.get("name")
    pat = mongo.db.users.find_one({"username": name})
    cc = request.args.get("cc")
    doctor = pat["doctor"]
    if doctor != "None":
        return jsonify({"doctor": doctor})
    try:
        doctor = mongo.db.doctors.find_one({"online": True})
        if doctor and not mongo.db.users.find_one({"username": name})["oncall"]:
            mongo.db.users.update_one({"username": name}, {"$set": {"doctor": doctor["username"]}})
            mongo.db.doctors.update_one({"username": doctor["username"]}, {"$push": {"patients": {"name": name, "time": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "cc": cc}}})
            return jsonify({"doctor": doctor["username"], "room": pat["room"], "oncall": pat["oncall"]})
        else:
            return jsonify({"doctor": "None", "room": pat["room"], "oncall": pat["oncall"]})
    except:
        return abort(404)

@app.route("/wait", methods=["GET", "POST"])
def wait():
    return render_template("wait.html", patientName=request.args.get("name"))

@app.route("/api/call_patient", methods=["GET"])
def api_call_patient():
    try:
        room = generate_room()
        mongo.db.users.update_one({"username": request.args.get("name")}, {"$set": {"room": room, "oncall": True}})
        requests.get("http://localhost:3000/api/delete_patient", params={"patient": request.args.get("name")})
        return jsonify({"room": room})
    except:
        return abort(404)
    
@app.route("/med", methods=["GET", "POST"])
def med():
    if request.args.get("name") == None:
        return redirect(url_for("doctor_login"))
    return render_template("med.html", patientName=request.args.get("name"), doctorName=request.args.get("doctor"))
    
@app.route("/api/med", methods=["POST"])
def api_med():
    # try:
        name = request.json.get("name")
        med = request.json.get("med")
        doc = request.json.get("doc")

        if name is not None and med is not None and doc is not None:
            send_mail(med=med, doc=doc, email=mongo.db.users.find_one({"username": name})["email"])
            return jsonify({"message": "ok"})
        else:
            return abort(404)
    # except:
    #     return abort(404)
        
pulse = {}
        
@app.route("/api/upload", methods=["POST"])
def api_upload():
    try:
        room = request.json.get("room")
        data = request.json.get("data")

        if room is not None and data is not None:
            pulse[room] = {"data": data, "date": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")}
            return jsonify({"message": "ok"})
        else:
            return abort(404)
    except:
        return abort(404)

@app.route("/api/get_pulse", methods=["GET"])
def api_get_pulse():
    try:
        room = request.args.get("room")
        if room is not None:
            return jsonify(pulse.get(room, "None"))
        else:
            return abort(404)
    except:
        return abort(404)
'''
@app.route("/api/diagnose", methods=["POST"])
def api_diagnose():
    try:
        img = Image.open(request.files["data"])
        return {"data": diagnose(img)}
    except:
        return abort(404)
'''

@app.route("/de", methods=["GET", "POST"])
def test():

    return render_template("test.html", **{"name": "test"}, cc=ccs)

@app.route("/ask", methods=["GET", "POST"])
def ask():
    naming = {}
    num = 1
    for val in ccs.values():
        for k, v in val.items():
            if type(v) == dict:
                for i in v.keys():
                    naming[i] = "sick-" + str(num)
                    num += 1
            else:
                naming[k] = "sick-" + str(num)
                num += 1

    return render_template("ask.html", name=request.args.get("name"), cc=ccs, naming=naming)

@app.route("/api/ask", methods=["POST"])
def api_ask():
    try:
        chose = request.get_json()["chose"]
        ask_back = dia.ask1(chose)
        # dcc = {}
        # for c in ask_back:
        #     dcc[c] = "無提示"
        #     for i in ccs.values():
        #         if c in i:
        #             dcc[c] = i.get(c, "無提示")
        #             break
        
        mongo.db.users.update_one({"username": request.get_json()["name"]}, {"$set": {"cc": chose, "dcc": ask_back}})

        return jsonify({"message": "ok"})
    except:
        return jsonify({"message": "error"})
    
@app.route("/ask1", methods=["GET", "POST"])
def ask1():
    tmp = mongo.db.users.find_one({"username": request.args.get("name")})["dcc"]
    dcc = {}
    for c in tmp:
        dcc[c] = ccs_dict.get(c, "無提示")
    
    naming = gen_naming(dcc.keys())

    return render_template("ask1.html", name=request.args.get("name"), dcc=dcc, naming=naming)

@app.route("/api/ask1", methods=["POST"])
def api_ask1():
    # try:
        cc = mongo.db.users.find_one({"username": request.get_json()["name"]})["cc"]
        dcc = request.get_json()["dcc"]
        mongo.db.users.update_one({"username": request.get_json()["name"]}, {"$set": {"dcc": dcc}})

        return jsonify({"message": "ok", "result": dia.ask2(cc, dcc)})
    # except:
    #     return jsonify({"message": "error"})

if __name__ == "__main__":
    app.run(debug=True, port=3000)
