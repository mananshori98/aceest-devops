def _create_alice(client):
    client.post(
        "/clients/new",
        data={"name": "Alice", "weight": 60, "program": "Beginner (BG)"},
    )


def _post_workout(client, **kwargs):
    data = {
        "date": "2026-03-01",
        "workout_type": "Strength",
        "duration_min": 45,
        "notes": "legs day",
    }
    data.update(kwargs)
    return client.post("/clients/Alice/workouts", data=data)


def test_log_workout(client):
    _create_alice(client)
    r = _post_workout(client)
    assert r.status_code == 302
    assert "/clients/Alice/workouts" in r.headers["Location"]


def test_workout_visible_in_history(client):
    _create_alice(client)
    _post_workout(client)
    r = client.get("/clients/Alice/workouts")
    assert r.status_code == 200
    assert b"Strength" in r.data
    assert b"legs day" in r.data


def test_log_multiple_workouts(client):
    _create_alice(client)
    _post_workout(client, workout_type="Cardio", date="2026-03-02")
    _post_workout(client, workout_type="Strength", date="2026-03-03")
    r = client.get("/clients/Alice/workouts")
    assert b"Cardio" in r.data
    assert b"Strength" in r.data


def test_log_workout_missing_fields(client):
    _create_alice(client)
    r = client.post("/clients/Alice/workouts", data={"date": ""})
    assert r.status_code == 400


def test_log_workout_unknown_client(client):
    r = _post_workout(client)
    assert r.status_code == 404
