# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _create_alice(client, **kwargs):
    data = {
        "name": "Alice",
        "age": 30,
        "height": 165,
        "weight": 60,
        "program": "Beginner (BG)",
        "target_weight": 55,
        "target_adherence": 90,
    }
    data.update(kwargs)
    return client.post("/clients/new", data=data)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_create_client_success(client):
    r = _create_alice(client)
    assert r.status_code == 302
    assert "/clients/Alice" in r.headers["Location"]


def test_create_client_missing_name(client):
    r = client.post("/clients/new", data={"age": 25})
    assert r.status_code == 400


def test_create_client_duplicate_name(client):
    _create_alice(client)
    r = _create_alice(client)
    assert r.status_code == 400


def test_client_profile_page(client):
    _create_alice(client)
    r = client.get("/clients/Alice")
    assert r.status_code == 200
    assert b"Alice" in r.data


def test_client_profile_404(client):
    r = client.get("/clients/Nobody")
    assert r.status_code == 404


def test_calorie_calculation_beginner(client):
    # 60 kg * factor 26 = 1560 kcal
    _create_alice(client, weight=60, program="Beginner (BG)")
    r = client.get("/clients/Alice")
    assert b"1560" in r.data


def test_calorie_calculation_muscle_gain(client):
    # 70 kg * factor 35 = 2450 kcal
    _create_alice(client, weight=70, program="Muscle Gain (MG) \u2013 PPL")
    r = client.get("/clients/Alice")
    assert b"2450" in r.data


def test_edit_client(client):
    _create_alice(client, weight=60, program="Beginner (BG)")
    r = client.post(
        "/clients/Alice/edit",
        data={"weight": 70, "program": "Muscle Gain (MG) \u2013 PPL"},
    )
    assert r.status_code == 302
    # profile now shows updated calories (70 * 35 = 2450)
    r = client.get("/clients/Alice")
    assert b"2450" in r.data


def test_edit_client_form_renders(client):
    _create_alice(client)
    r = client.get("/clients/Alice/edit")
    assert r.status_code == 200
    assert b"Alice" in r.data
