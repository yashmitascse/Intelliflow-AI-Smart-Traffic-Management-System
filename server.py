from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

traffic_data = {
    "vehicle_count": 0,
    "traffic_density": "LOW",
    "green_signal": 15
}


@app.route("/")
def home():
    return "IntelliFlow AI Backend Running"


@app.route("/traffic")
def traffic():
    return jsonify(traffic_data)


def update_traffic(vehicle_count, density, signal_time):
    traffic_data["vehicle_count"] = vehicle_count
    traffic_data["traffic_density"] = density
    traffic_data["green_signal"] = signal_time


if __name__ == "__main__":
    app.run(debug=True)