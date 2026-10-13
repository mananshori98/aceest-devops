def _create_alice(client):
    client.post(
        "/clients/new",
        data={"name": "Alice", "weight": 60, "program": "Beginner (BG)"},
    )


def test_log_progress(client):
    _create_alice(client)
    r = client.post(
        "/clients/Alice/progress",
        data={"week": "2026-W10", "adherence": 85},
    )
    assert r.status_code == 302


def test_progress_visible_on_profile(client):
    _create_alice(client)
    client.post(
        "/clients/Alice/progress",
        data={"week": "2026-W10", "adherence": 85},
    )
    r = client.get("/clients/Alice")
    assert r.status_code == 200
    assert b"2026-W10" in r.data
    assert b"85" in r.data


def test_log_progress_missing_fields(client):
    _create_alice(client)
    r = client.post("/clients/Alice/progress", data={"week": "2026-W10"})
    assert r.status_code == 400


def test_log_progress_unknown_client(client):
    r = client.post(
        "/clients/Nobody/progress",
        data={"week": "2026-W10", "adherence": 80},
    )
    assert r.status_code == 404
