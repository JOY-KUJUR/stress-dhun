from flask import Flask, render_template, request, jsonify
import json
from datetime import date

app = Flask(__name__)
DATA_FILE = "stress_data.json"


def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_data(entry):
    data = load_data()
    data.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/save", methods=["POST"])
def save():
    data = request.json
    entry = {
        "date": str(date.today()),
        "hours": data["hours"],
        "stress": data["stress"],
        "summary": data["summary"]
    }
    save_data(entry)
    return jsonify({"status": "saved"})


@app.route("/history")
def history():
    return jsonify(load_data())


if __name__ == "__main__":
    app.run(debug=True)
