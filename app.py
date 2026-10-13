import os
import sqlite3

from flask import Flask, g, render_template, request, redirect, url_for, abort, jsonify

# ---------------------------------------------------------------------------
# Calorie calculation factors (ported from Aceestver-2.1.2 / 2.2.4)
# ---------------------------------------------------------------------------
PROGRAMS = {
    "Fat Loss (FL) – 3 day": {"factor": 22, "desc": "3-day full-body fat loss"},
    "Fat Loss (FL) – 5 day": {"factor": 24, "desc": "5-day split, higher volume fat loss"},
    "Muscle Gain (MG) – PPL": {"factor": 35, "desc": "Push/Pull/Legs hypertrophy"},
    "Beginner (BG)": {"factor": 26, "desc": "3-day simple beginner full-body"},
}

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "aceest_fitness.db"),
        SECRET_KEY="dev",
    )

    if test_config is not None:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    # ------------------------------------------------------------------
    # Database helpers
    # ------------------------------------------------------------------

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(
                app.config["DATABASE"],
                detect_types=sqlite3.PARSE_DECLTYPES,
            )
            g.db.row_factory = sqlite3.Row
        return g.db

    def close_db(e=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        db = get_db()
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, encoding="utf-8") as f:
            db.executescript(f.read())

    app.teardown_appcontext(close_db)

    # CLI command: flask init-db
    import click

    @app.cli.command("init-db")
    def init_db_command():
        """Initialise the database from schema.sql."""
        init_db()
        click.echo("Database initialised.")

    # ------------------------------------------------------------------
    # Helper: calorie calculation
    # ------------------------------------------------------------------

    def calculate_calories(weight, program):
        if not weight or program not in PROGRAMS:
            return None
        return int(float(weight) * PROGRAMS[program]["factor"])

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------

    @app.route("/health")
    def health():
        """Health-check endpoint used by Docker HEALTHCHECK and tests."""
        return jsonify({"status": "ok"}), 200

    @app.route("/")
    def index():
        db = get_db()
        clients = db.execute("SELECT * FROM clients ORDER BY name").fetchall()
        return render_template("index.html", clients=clients)

    @app.route("/clients/new", methods=["GET", "POST"])
    def new_client():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                return render_template(
                    "client_form.html",
                    programs=PROGRAMS,
                    error="Name is required.",
                    form=request.form,
                ), 400

            age = request.form.get("age") or None
            height = request.form.get("height") or None
            weight = request.form.get("weight") or None
            program = request.form.get("program") or None
            target_weight = request.form.get("target_weight") or None
            target_adherence = request.form.get("target_adherence") or None

            calories = calculate_calories(weight, program)

            db = get_db()
            try:
                db.execute(
                    """
                    INSERT INTO clients
                        (name, age, height, weight, program, calories, target_weight, target_adherence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (name, age, height, weight, program, calories, target_weight, target_adherence),
                )
                db.commit()
            except sqlite3.IntegrityError:
                return render_template(
                    "client_form.html",
                    programs=PROGRAMS,
                    error=f"A client named '{name}' already exists.",
                    form=request.form,
                ), 400

            return redirect(url_for("client_detail", name=name))

        return render_template("client_form.html", programs=PROGRAMS, error=None, form={})

    @app.route("/clients/<name>")
    def client_detail(name):
        db = get_db()
        client = db.execute("SELECT * FROM clients WHERE name = ?", (name,)).fetchone()
        if client is None:
            abort(404)
        progress = db.execute(
            "SELECT * FROM progress WHERE client_name = ? ORDER BY week DESC",
            (name,),
        ).fetchall()
        return render_template("client_detail.html", client=client, progress=progress)

    @app.route("/clients/<name>/edit", methods=["GET", "POST"])
    def edit_client(name):
        db = get_db()
        client = db.execute("SELECT * FROM clients WHERE name = ?", (name,)).fetchone()
        if client is None:
            abort(404)

        if request.method == "POST":
            age = request.form.get("age") or None
            height = request.form.get("height") or None
            weight = request.form.get("weight") or None
            program = request.form.get("program") or None
            target_weight = request.form.get("target_weight") or None
            target_adherence = request.form.get("target_adherence") or None

            calories = calculate_calories(weight, program)

            db.execute(
                """
                UPDATE clients
                SET age=?, height=?, weight=?, program=?, calories=?,
                    target_weight=?, target_adherence=?
                WHERE name=?
                """,
                (age, height, weight, program, calories, target_weight, target_adherence, name),
            )
            db.commit()
            return redirect(url_for("client_detail", name=name))

        return render_template(
            "client_form.html", programs=PROGRAMS, error=None,
            form=dict(client), edit=True, client_name=name,
        )

    @app.route("/clients/<name>/progress", methods=["POST"])
    def log_progress(name):
        db = get_db()
        if db.execute("SELECT 1 FROM clients WHERE name = ?", (name,)).fetchone() is None:
            abort(404)

        week = request.form.get("week", "").strip()
        adherence = request.form.get("adherence", "").strip()

        if not week or not adherence:
            abort(400)

        db.execute(
            "INSERT INTO progress (client_name, week, adherence) VALUES (?, ?, ?)",
            (name, week, int(adherence)),
        )
        db.commit()
        return redirect(url_for("client_detail", name=name))

    @app.route("/clients/<name>/workouts", methods=["GET", "POST"])
    def workouts(name):
        db = get_db()
        if db.execute("SELECT 1 FROM clients WHERE name = ?", (name,)).fetchone() is None:
            abort(404)

        if request.method == "POST":
            date = request.form.get("date", "").strip()
            workout_type = request.form.get("workout_type", "").strip()
            duration_min = request.form.get("duration_min", "").strip()
            notes = request.form.get("notes", "").strip()

            if not date or not workout_type or not duration_min:
                abort(400)

            db.execute(
                """
                INSERT INTO workouts (client_name, date, workout_type, duration_min, notes)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, date, workout_type, int(duration_min), notes or None),
            )
            db.commit()
            return redirect(url_for("workouts", name=name))

        history = db.execute(
            "SELECT * FROM workouts WHERE client_name = ? ORDER BY date DESC",
            (name,),
        ).fetchall()
        return render_template("workout_history.html", client_name=name, history=history)

    # ------------------------------------------------------------------
    # Make init_db importable for tests
    # ------------------------------------------------------------------
    app.init_db = init_db

    return app


# Allow `flask run` without FLASK_APP pointing to the factory
app = create_app()
