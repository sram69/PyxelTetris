from flask import Flask, request, abort, jsonify
import json
import os

app = Flask(__name__)

@app.route("/get/", methods=["GET"])
def get():
    if not os.path.exists("data.json"): # If the file doesn't exist, create it and write empty dict
        with open("data.json", 'w') as file:
            file.write('{}')
        
        return [0]
    else:
        data = json.load(open("data.json", "r"))

    return [data.get(request.remote_addr, 0)]

@app.route("/set/", methods=["GET"])
def set():
    score = request.args.get("s", type=int, default=0)

    if not os.path.exists("data.json"): # If the file doesn't exist, create it and write empty dict
        with open("data.json", 'w') as file:
            file.write('{}')

    # Saving
    data = json.load(open("data.json", "r"))

    if request.remote_addr in data.keys():
        if score < data[request.remote_addr]:
            return {"success": False, "message": "Not a best score"}
        
    data[request.remote_addr] = score
    json.dump(data, open("data.json", "w+"))

    return jsonify(success=True)

app.run(host="0.0.0.0")