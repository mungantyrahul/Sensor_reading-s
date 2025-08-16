from flask import Flask, request

app = Flask(__name__)

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "GET":
        temp = request.args.get("temp")
    else:
        data = request.get_json(force=True)
        temp = data.get("temp")
    print("✅ Received temperature:", temp)
    return {"status": "success", "temperature": temp}

@app.route("/", methods=["GET"])
def home():
    return "🌍 Temperature Server is Running!"

