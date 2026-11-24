import pytest
from app import APP_VERSION, app, body_metrics, clients, progress_records, workouts


@pytest.fixture
def client():
    app.config["TESTING"] = True
    clients.clear()
    progress_records.clear()
    workouts.clear()
    body_metrics.clear()
    with app.test_client() as test_client:
        yield test_client


def create_client(client):
    return client.post(
        "/clients",
        json={"name": "Test Client", "email": "test@example.com", "program_id": 1}
    )


def test_home(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.get_json()["version"] == APP_VERSION
    assert r.get_json()["status"] == "running"


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "healthy"
    assert r.get_json()["version"] == APP_VERSION


def test_ready(client):
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ready"
    assert r.get_json()["version"] == APP_VERSION


def test_version(client):
    r = client.get("/version")
    assert r.status_code == 200
    assert r.get_json()["version"] == APP_VERSION
    assert r.get_json()["application"] == "ACEest Fitness & Gym"


def test_programs(client):
    r = client.get("/programs")
    assert r.status_code == 200
    assert len(r.get_json()) == 3


def test_empty_clients(client):
    r = client.get("/clients")
    assert r.status_code == 200
    assert r.get_json() == []


def test_add_client(client):
    r = create_client(client)
    assert r.status_code == 201
    assert r.get_json()["program"] == "Weight Loss"
    assert r.get_json()["email"] == "test@example.com"


def test_missing_client_fields(client):
    assert client.post("/clients", json={"name": "Incomplete"}).status_code == 400
    assert client.post("/clients", data="not json", content_type="text/plain").status_code == 400


def test_invalid_email(client):
    assert client.post(
        "/clients",
        json={"name": "Test", "email": "invalid", "program_id": 1}
    ).status_code == 400


def test_invalid_program(client):
    assert client.post(
        "/clients",
        json={"name": "Test", "email": "test@example.com", "program_id": 99}
    ).status_code == 400


def test_duplicate_email(client):
    create_client(client)
    assert create_client(client).status_code == 409


def test_calories(client):
    r = client.post(
        "/calories",
        json={"weight_kg": 70, "duration_minutes": 30, "intensity": "moderate"}
    )
    assert r.status_code == 200
    assert r.get_json()["estimated_calories"] == 168.0


def test_invalid_intensity(client):
    assert client.post(
        "/calories",
        json={"weight_kg": 70, "duration_minutes": 30, "intensity": "extreme"}
    ).status_code == 400


def test_non_positive_calories(client):
    assert client.post(
        "/calories",
        json={"weight_kg": 0, "duration_minutes": 30}
    ).status_code == 400
    assert client.post("/calories", data="invalid", content_type="text/plain").status_code == 400


def test_add_progress(client):
    create_client(client)
    r = client.post("/progress", json={"client_id": 1, "weight_kg": 70})
    assert r.status_code == 201
    assert r.get_json()["weight_kg"] == 70.0


def test_progress_unknown_client(client):
    assert client.post("/progress", json={"client_id": 999, "weight_kg": 70}).status_code == 404
    assert client.post("/progress", data="invalid", content_type="text/plain").status_code == 400
    assert client.get("/progress").status_code == 200


def test_add_workout(client):
    create_client(client)
    r = client.post(
        "/workouts",
        json={"client_id": 1, "activity": "Running", "duration_minutes": 30}
    )
    assert r.status_code == 201
    assert r.get_json()["activity"] == "Running"
    assert client.get("/workouts").status_code == 200


def test_invalid_workout_duration(client):
    create_client(client)
    assert client.post(
        "/workouts",
        json={"client_id": 1, "activity": "Running", "duration_minutes": 0}
    ).status_code == 400
    assert client.post(
        "/workouts",
        json={"client_id": 999, "activity": "Running", "duration_minutes": 30}
    ).status_code == 404
    assert client.post("/workouts", data="invalid", content_type="text/plain").status_code == 400


def test_metric_bmi(client):
    create_client(client)
    r = client.post(
        "/metrics",
        json={"client_id": 1, "height_cm": 175, "weight_kg": 70}
    )
    assert r.status_code == 201
    assert r.get_json()["bmi"] == 22.86
    assert client.post(
        "/metrics",
        json={"client_id": 999, "height_cm": 175, "weight_kg": 70}
    ).status_code == 404
    assert client.post("/metrics", data="invalid", content_type="text/plain").status_code == 400


def test_json_404(client):
    r = client.get("/does-not-exist")
    assert r.status_code == 404
    assert r.get_json()["error"] == "Resource not found"
