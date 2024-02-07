import os
import datetime
import random
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort
from flask import render_template, url_for, redirect, session, flash
from flask_pymongo import PyMongo
from mail import send_mail

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

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

@app.route("/test", methods=["GET", "POST"])
def test():
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
        data = {}
        data["info"] = dict(request.get_json())

        data["oncall"] = False
        data["doctor"] = "None"
        data["room"] = "None"

        mongo.db.users.insert_one(data)

        print("User added", data)

        return jsonify({"message": "ok"})
    except:
        return abort(404)



    
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
    doctor = pat["doctor"]
    if doctor != "None":
        return jsonify({"doctor": doctor})
    try:
        doctor = mongo.db.doctors.find_one({"online": True})
        if doctor and not mongo.db.users.find_one({"username": name})["oncall"]:
            mongo.db.users.update_one({"username": name}, {"$set": {"doctor": doctor["username"]}})
            mongo.db.doctors.update_one({"username": doctor["username"]}, {"$push": {"patients": {"name": name, "time": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")}}})
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

if __name__ == "__main__":
    app.run(debug=True, port=3000)
