from flask import Flask, request, jsonify
from hashlib import sha256
import json
import os

app = Flask(__name__)

@app.route("/get/", methods=["GET"])
def get():
    ip = sha256(request.remote_addr.encode('utf-8')).hexdigest()
    if not os.path.exists("data.json"): # If the file doesn't exist, create it and write empty dict
        with open("data.json", 'w') as file:
            file.write('{}')
        
        return [0]
    else:
        data = json.load(open("data.json", "r"))

    return [data.get(ip, 0)]

@app.route("/set/", methods=["GET"])
def set():
    ip = sha256(request.remote_addr.encode('utf-8')).hexdigest()
    score = request.args.get("s", type=int, default=0)

    if not os.path.exists("data.json"): # If the file doesn't exist, create it and write empty dict
        with open("data.json", 'w') as file:
            file.write('{}')
    # Saving
    data = json.load(open("data.json", "r"))

    if ip in data.keys():
        if score < data[ip]:
            return {"success": False, "message": "Not a best score"}
        
    data[ip] = score
    json.dump(data, open("data.json", "w+"))

    return jsonify(success=True)

app.run(host="0.0.0.0")