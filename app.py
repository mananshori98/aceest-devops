from flask import Flask, jsonify, request

app = Flask(__name__)
APP_VERSION = "2.0.0"

PROGRAMS = [
    {"id": 1, "name": "Weight Loss", "duration_weeks": 8, "sessions_per_week": 4},
    {"id": 2, "name": "Muscle Gain", "duration_weeks": 12, "sessions_per_week": 5},
    {"id": 3, "name": "General Fitness", "duration_weeks": 6, "sessions_per_week": 3},
]
clients = []
progress_records = []
workouts = []
body_metrics = []


def find_client(client_id):
    return next((item for item in clients if item["id"] == client_id), None)


@app.get("/")
def home():
    return jsonify({
        "application": "ACEest Fitness & Gym",
        "version": APP_VERSION,
        "status": "running",
        "message": "Welcome to the ACEest Fitness & Gym API"
    }), 200


@app.get("/health")
def health():
    return jsonify({"status": "healthy", "version": APP_VERSION}), 200


@app.get("/ready")
def ready():
    return jsonify({"status": "ready", "version": APP_VERSION}), 200


@app.get("/version")
def version():
    return jsonify({"application": "ACEest Fitness & Gym", "version": APP_VERSION}), 200


@app.get("/programs")
def get_programs():
    return jsonify(PROGRAMS), 200


@app.get("/clients")
def get_clients():
    return jsonify(clients), 200


@app.post("/clients")
def add_client():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    program_id = data.get("program_id")
    if not name or not email or program_id is None:
        return jsonify({"error": "name, email and program_id are required"}), 400
    if "@" not in email:
        return jsonify({"error": "A valid email address is required"}), 400
    program = next((item for item in PROGRAMS if item["id"] == program_id), None)
    if program is None:
        return jsonify({"error": "Invalid program_id"}), 400
    if any(item["email"].lower() == email.lower() for item in clients):
        return jsonify({"error": "A client with this email already exists"}), 409
    client = {
        "id": len(clients) + 1,
        "name": name,
        "email": email,
        "program_id": program["id"],
        "program": program["name"]
    }
    clients.append(client)
    return jsonify(client), 201


@app.post("/calories")
def calculate_calories():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400
    try:
        weight_kg = float(data["weight_kg"])
        duration_minutes = float(data["duration_minutes"])
        intensity = str(data.get("intensity", "moderate")).lower()
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "weight_kg and duration_minutes must be valid numbers"}), 400
    if weight_kg <= 0 or duration_minutes <= 0:
        return jsonify({"error": "weight_kg and duration_minutes must be greater than zero"}), 400
    factors = {"low": 0.05, "moderate": 0.08, "high": 0.11}
    if intensity not in factors:
        return jsonify({"error": "intensity must be low, moderate or high"}), 400
    calories = round(weight_kg * duration_minutes * factors[intensity], 2)
    return jsonify({
        "weight_kg": weight_kg,
        "duration_minutes": duration_minutes,
        "intensity": intensity,
        "estimated_calories": calories
    }), 200


@app.get("/progress")
def get_progress():
    return jsonify(progress_records), 200


@app.post("/progress")
def add_progress():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400
    try:
        client_id = int(data["client_id"])
        weight_kg = float(data["weight_kg"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "client_id and weight_kg are required"}), 400
    if find_client(client_id) is None:
        return jsonify({"error": "Client not found"}), 404
    if weight_kg <= 0:
        return jsonify({"error": "weight_kg must be greater than zero"}), 400
    record = {"id": len(progress_records) + 1, "client_id": client_id, "weight_kg": weight_kg}
    progress_records.append(record)
    return jsonify(record), 201


@app.get("/workouts")
def get_workouts():
    return jsonify(workouts), 200


@app.post("/workouts")
def add_workout():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400
    try:
        client_id = int(data["client_id"])
        duration_minutes = float(data["duration_minutes"])
        activity = str(data["activity"]).strip()
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "client_id, activity and duration_minutes are required"}), 400
    if not activity:
        return jsonify({"error": "client_id, activity and duration_minutes are required"}), 400
    if find_client(client_id) is None:
        return jsonify({"error": "Client not found"}), 404
    if duration_minutes <= 0:
        return jsonify({"error": "duration_minutes must be greater than zero"}), 400
    workout = {
        "id": len(workouts) + 1,
        "client_id": client_id,
        "activity": activity,
        "duration_minutes": duration_minutes
    }
    workouts.append(workout)
    return jsonify(workout), 201


@app.post("/metrics")
def add_metric():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400
    try:
        client_id = int(data["client_id"])
        height_cm = float(data["height_cm"])
        weight_kg = float(data["weight_kg"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "client_id, height_cm and weight_kg are required"}), 400
    if find_client(client_id) is None:
        return jsonify({"error": "Client not found"}), 404
    if height_cm <= 0 or weight_kg <= 0:
        return jsonify({"error": "height_cm and weight_kg must be greater than zero"}), 400
    metric = {
        "id": len(body_metrics) + 1,
        "client_id": client_id,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "bmi": round(weight_kg / ((height_cm / 100) ** 2), 2)
    }
    body_metrics.append(metric)
    return jsonify(metric), 201


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Resource not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
