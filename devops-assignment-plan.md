# DevOps Assignment Plan — ACEest Fitness & Gym CI/CD Pipeline

## Top-Level Overview

**Goal**: Transform the existing ACEest tkinter desktop application into a Flask web application,
then surround it with a full professional DevOps lifecycle: Git version control, Pytest unit tests,
Docker containerisation, a Jenkins BUILD quality gate (local via Docker), and a GitHub Actions
CI/CD pipeline that builds, lints, tests, and pushes a Docker image to Docker Hub on every push.

**Scope**: The Flask application covers the feature set of v2.1.2 + workout logging (v2.2.4 scope):
- Client CRUD (name, age, height, weight, program, calorie estimate)
- Weekly progress logging and retrieval
- Workout session logging (date, type, duration, notes)

**Persistence**: SQLite (`aceest_fitness.db`) — unchanged from the existing codebase.

**Out of scope**: Authentication/login, PDF export, matplotlib charts, AI program generator, membership billing.

**Deliverables required by assignment**:
- `app.py` — Flask application
- `requirements.txt` — Python dependencies
- Pytest test files
- `Dockerfile`
- `.github/workflows/main.yml` — GitHub Actions pipeline
- `README.md`

---

## Sub-Task 1 — Repository & Project Scaffold

**Intent**: Establish the Git repository structure and project layout that all subsequent sub-tasks
will build into. All deliverable files must live at the repo root so the Dockerfile, GitHub Actions
runner, and Jenkins can find them without path gymnastics.

**Expected Outcomes**:
- A local Git repository exists, initialised with a `.gitignore` (Python + SQLite artefacts).
- Remote GitHub repository is created and the local repo is pushed to `main`.
- Directory structure matches the assignment's expected layout.
- An initial commit with scaffold files is present (empty `app.py`, placeholder `requirements.txt`,
  placeholder `README.md`).

**Todo List**:
1. Create the project directory at the repo root.
2. Run `git init` and set the default branch to `main`.
3. Create a `.gitignore` covering `__pycache__`, `*.pyc`, `*.db`, `.env`, `*.egg-info`, `.pytest_cache`, `dist/`.
4. Create stub files: `app.py`, `requirements.txt`, `README.md`, `tests/` folder with `__init__.py`.
5. Make an initial commit: `"chore: scaffold project structure"`.
6. Create a public GitHub repository (`aceest-devops`) and push.

**Relevant Context**:
- All 10 existing `.py` files live in `The code versions for DevOps Assignment/`. They are reference
  material only — do not include them in the Flask project structure.

**Status**: [ ] pending

---

## Sub-Task 2 — Flask Application (`app.py` + Templates)

**Intent**: Implement the Flask web application using the SQLite schema and business logic ported from
`Aceestver-2.1.2.py` (client CRUD + progress) and `Aceestver-2.2.4.py` (workout logging). This is
the core of the assignment — all other phases wrap this application.

**Expected Outcomes**:
- `app.py` exposes the following routes:
  - `GET /` — homepage / client list
  - `GET/POST /clients/new` — create client
  - `GET /clients/<name>` — client profile page
  - `POST /clients/<name>/edit` — update client
  - `POST /clients/<name>/progress` — log weekly adherence
  - `POST /clients/<name>/workouts` — log a workout session
  - `GET /clients/<name>/workouts` — workout history
  - `GET /health` — returns `{"status": "ok"}` (used by tests and Docker HEALTHCHECK)
- `templates/` folder contains Bootstrap-styled Jinja2 templates for each view.
- `database.py` (or `db` module inside `app.py`) exposes `get_db()` using Flask's `g` object and
  `init_db()` using `schema.sql`.
- `schema.sql` defines the three tables: `clients`, `progress`, `workouts`.
- `requirements.txt` is complete: `flask`, `pytest`, `pytest-flask`.
- The app runs locally with `flask run` and all routes are manually verified.

**Todo List**:
1. Write `schema.sql` with `CREATE TABLE IF NOT EXISTS` for `clients`, `progress`, `workouts`
   (columns taken directly from `Aceestver-2.2.4.py` `init_db()`).
2. Write `app.py`:
   a. Create Flask app, configure `DATABASE` path from env var with SQLite default.
   b. Implement `get_db()` / `close_db()` / `init_db()` / `init_app()` pattern.
   c. Add a CLI command `flask init-db` that creates the schema.
   d. Implement all routes listed above.
   e. Port calorie calculation logic: `calories = weight * program_factors[program]` (factors from
      `Aceestver-2.1.2.py`: FL=22, MG=35, BG=26).
3. Create `templates/base.html` with Bootstrap CDN navbar and block layout.
4. Create individual templates: `index.html`, `client_form.html`, `client_detail.html`,
   `workout_form.html`, `workout_history.html`.
5. Write `requirements.txt` with pinned versions.
6. Verify manually: `flask init-db && flask run`, walk through all routes.
7. Commit: `"feat: implement Flask application with client CRUD, progress, and workout logging"`.

**Relevant Context**:
- Calorie factor dict from `Aceestver-2.1.2.py` lines 47–51:
  `{"Fat Loss (FL)": 22, "Muscle Gain (MG)": 35, "Beginner (BG)": 26}`
- `clients` schema from `Aceestver-2.2.4.py` lines 60–74 (includes `height`, `target_weight`, etc.)
- `progress` schema from `Aceestver-2.2.4.py` lines 77–86
- `workouts` schema from `Aceestver-2.2.4.py` lines 89–100
- Use the `exercises` table only if time allows — it is not in core scope.

**Status**: [ ] pending

---

## Sub-Task 3 — Pytest Unit Test Suite

**Intent**: Produce a Pytest test suite that validates the core Flask application logic. Tests must
run inside the containerised environment (requirement of GitHub Actions stage 3) and must provide
meaningful coverage over the routes and business logic.

**Expected Outcomes**:
- `tests/conftest.py` provides a `client` fixture that creates an in-memory SQLite test database and
  a Flask test client. Tests are fully isolated (each test gets a fresh DB).
- `tests/test_clients.py` covers: create client (valid), create client (missing fields → 4xx),
  load client profile, update client, calorie calculation.
- `tests/test_progress.py` covers: log weekly progress, retrieve progress for client.
- `tests/test_workouts.py` covers: log workout session, retrieve workout history.
- `tests/test_health.py` covers: `GET /health` returns `200` with `{"status": "ok"}`.
- `pytest` runs from repo root with `pytest --tb=short` and all tests pass.

**Todo List**:
1. Write `tests/conftest.py`:
   - Define `app` fixture with `TESTING=True` and `DATABASE=':memory:'`.
   - Call `init_db()` in fixture setup.
   - Define `client` fixture wrapping Flask test client.
2. Write `tests/test_health.py` — single GET `/health` assertion.
3. Write `tests/test_clients.py`:
   - `test_create_client_success` — POST to `/clients/new`, expect redirect to client page.
   - `test_create_client_missing_name` — POST without name, expect 400 or form re-render.
   - `test_client_profile_page` — GET `/clients/<name>`, expect client name in response.
   - `test_calorie_calculation` — create a client with known weight+program, assert calories field.
4. Write `tests/test_progress.py`:
   - `test_log_progress` — POST progress, then GET client profile and assert week/adherence visible.
5. Write `tests/test_workouts.py`:
   - `test_log_workout` — POST workout, then GET workout history and assert entry visible.
6. Run `pytest -v` locally, confirm all green.
7. Commit: `"test: add pytest suite for client CRUD, progress, workouts, and health endpoint"`.

**Relevant Context**:
- Flask testing pattern uses `app.test_client()` and `app.app_context()`.
- Use `app.config["TESTING"] = True` and `DATABASE = ":memory:"` to avoid touching the real DB.
- `conftest.py` fixtures follow the Flask docs pattern for SQLite testing.

**Status**: [ ] pending

---

## Sub-Task 4 — Dockerfile

**Intent**: Package the Flask application into a portable, optimised Docker image so it can run
identically in development, in the Jenkins BUILD environment, and in the GitHub Actions runner.

**Expected Outcomes**:
- `Dockerfile` at repo root builds successfully with `docker build -t aceest-app .`.
- Image is based on `python:3.11-slim` (small, secure base).
- Non-root user `appuser` runs the application (security best practice, evaluator criterion).
- `requirements.txt` is installed in a separate layer before copying source code (build cache optimisation).
- Container starts with `flask run --host=0.0.0.0` (or `gunicorn` if preferred).
- `HEALTHCHECK` instruction hits `GET /health`.
- `docker run -p 5000:5000 aceest-app` starts the app and it responds at `http://localhost:5000`.
- `.dockerignore` excludes `*.db`, `*.pyc`, `__pycache__`, `.git`, `tests/`, `.github/`.
- Commit: `"feat: add Dockerfile with non-root user and HEALTHCHECK"`.

**Todo List**:
1. Create `.dockerignore`.
2. Write `Dockerfile`:
   a. `FROM python:3.11-slim`
   b. `WORKDIR /app`
   c. Copy `requirements.txt` first, then `RUN pip install --no-cache-dir -r requirements.txt`.
   d. Copy remaining source files.
   e. Create non-root user: `RUN adduser --disabled-password appuser && chown -R appuser /app`.
   f. `USER appuser`
   g. `ENV FLASK_APP=app.py`
   h. `EXPOSE 5000`
   i. `HEALTHCHECK CMD curl -f http://localhost:5000/health || exit 1`
   j. `CMD ["flask", "run", "--host=0.0.0.0"]`
3. Build and smoke-test locally: `docker build -t aceest-app . && docker run -p 5000:5000 aceest-app`.
4. Verify `/health` from host.
5. Commit: `"feat: add Dockerfile with non-root user and HEALTHCHECK"`.

**Relevant Context**:
- `python:3.11-slim` has `curl` available for HEALTHCHECK; confirm or install with `apt-get`.
- `*.db` must be excluded from image — the DB is initialised at container startup, not baked in.

**Status**: [ ] pending

---

## Sub-Task 5 — GitHub Actions CI/CD Pipeline

**Intent**: Automate the build, lint, test, and Docker push lifecycle on every push or pull_request
to `main`. This is the primary CI/CD deliverable evaluated by the assignment.

**Expected Outcomes**:
- `.github/workflows/main.yml` exists at repo root.
- Workflow triggers on `push` and `pull_request` to `main`.
- Three sequential jobs (or stages within one job):
  1. **build-lint**: checkout → set up Python 3.11 → install deps → run `flake8 app.py` for syntax/lint.
  2. **docker-build**: build Docker image → run Pytest inside the container
     (`docker run aceest-app pytest --tb=short`).
  3. **push**: on success and only for `push` to `main` (not PRs), tag and push image to Docker Hub
     using `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` repository secrets.
- All three stages appear green in the GitHub Actions tab on a clean push.
- Commit: `"ci: add GitHub Actions workflow for build, lint, test, and Docker push"`.

**Todo List**:
1. Create `.github/workflows/main.yml`.
2. Define trigger: `on: push: branches: [main]` and `pull_request: branches: [main]`.
3. Define `build-lint` job:
   - `runs-on: ubuntu-latest`
   - steps: `actions/checkout@v4`, `actions/setup-python@v5` (python 3.11), `pip install -r requirements.txt flake8`, `flake8 app.py tests/`.
4. Define `docker-build` job (depends on `build-lint`):
   - Build image: `docker build -t aceest-app .`
   - Run Pytest: `docker run aceest-app pytest --tb=short`
5. Define `push` job (depends on `docker-build`, only runs on `push` to `main`):
   - `docker/login-action@v3` using secrets `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN`.
   - Tag: `docker tag aceest-app ${{ secrets.DOCKERHUB_USERNAME }}/aceest-app:latest`
   - Push: `docker push ${{ secrets.DOCKERHUB_USERNAME }}/aceest-app:latest`
6. Add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` as GitHub repository secrets.
7. Push branch, observe Actions tab, fix any failures.
8. Commit: `"ci: add GitHub Actions workflow for build, lint, test, and Docker push"`.

**Relevant Context**:
- `flake8` must be added to `requirements.txt` (or installed inline in the workflow).
- The Pytest run inside the container requires `pytest` to be in `requirements.txt` and for the
  `tests/` folder to be present in the image (remove `tests/` from `.dockerignore` for this purpose,
  or mount it — simpler to keep tests in the image for CI use).
- Docker Hub token can be created at hub.docker.com → Account Settings → Security → New Access Token.

**Status**: [ ] pending

---

## Sub-Task 6 — Jenkins BUILD Quality Gate

**Intent**: Set up a Jenkins server locally via Docker and configure a Freestyle project that pulls
the latest code from GitHub and performs a clean build. This acts as an additional, independent
quality gate — distinct from GitHub Actions.

**Expected Outcomes**:
- Jenkins is running locally at `http://localhost:8080` via `docker run jenkins/jenkins:lts`.
- A Jenkins Freestyle project (`ACEest-Build`) is configured to:
  - Pull source from the public GitHub repository (Git SCM, `main` branch).
  - Build step: `pip install -r requirements.txt && pytest --tb=short`.
- A successful build run is visible in Jenkins with a green/blue ball.
- (Optional) Build is triggered by a GitHub webhook or manually via "Build Now".

**Todo List**:
1. Start Jenkins container:
   ```
   docker run -d -p 8080:8080 -p 50000:50000 \
     -v jenkins_home:/var/jenkins_home \
     --name jenkins jenkins/jenkins:lts
   ```
2. Retrieve the initial admin password: `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`.
3. Complete Jenkins setup wizard at `http://localhost:8080` — install suggested plugins.
4. Create a new Freestyle project named `ACEest-Build`.
5. Under Source Code Management, select Git and enter the GitHub repo URL.
6. Under Build Steps, add "Execute shell":
   ```
   pip install -r requirements.txt
   pytest --tb=short
   ```
7. Save and click "Build Now" — verify console output shows all tests passing.
8. Document the Jenkins setup steps in `README.md`.

**Relevant Context**:
- The Jenkins container runs on the Docker host; it can reach GitHub directly over the internet.
- Python must be available in the Jenkins container — install via the Jenkins "Execute Shell" step
  using `apt-get install -y python3 python3-pip` as a first step, or use the `jenkins/jenkins:lts`
  image with Python pre-configured using a custom Dockerfile for Jenkins.
- If Python is not available inside the Jenkins container, wrap the build step as a Docker Pipeline
  step using `docker.image('python:3.11-slim').inside { ... }`.

**Status**: [ ] pending

---

## Sub-Task 7 — README.md Documentation

**Intent**: Produce a professional `README.md` that satisfies the assignment's documentation
criterion and enables any engineer to clone the repo and run everything from scratch.

**Expected Outcomes**:
- `README.md` contains all sections listed below and passes a reading comprehension check.
- A new engineer can follow the README with no prior knowledge of the project.

**Todo List**:
1. Write `README.md` with the following sections:
   - **Project Overview** — what ACEest is, what this repo delivers.
   - **Architecture Diagram** — ASCII or Mermaid showing: Local Dev → GitHub → GitHub Actions → Docker Hub, and separately Local Dev → Jenkins.
   - **Prerequisites** — Python 3.11+, Docker, Git, (optional) Jenkins.
   - **Local Setup & Execution**:
     - `git clone ...`
     - `pip install -r requirements.txt`
     - `flask init-db`
     - `flask run`
   - **Running Tests Manually**:
     - `pytest --tb=short`
   - **Docker**:
     - `docker build -t aceest-app .`
     - `docker run -p 5000:5000 aceest-app`
   - **Jenkins BUILD Setup** — step-by-step from Sub-Task 6.
   - **GitHub Actions Pipeline Overview** — describe the three stages and what triggers them.
   - **Environment Variables / Secrets** — `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.
2. Commit: `"docs: add professional README with full setup, test, and CI/CD instructions"`.

**Relevant Context**:
- Assignment evaluation criterion: "Documentation Clarity: Is the README.md professional and easy
  to follow for other engineers."

**Status**: [ ] pending

---

## Dependency Order

```
Sub-Task 1 (Scaffold)
    └── Sub-Task 2 (Flask App)
            ├── Sub-Task 3 (Pytest Tests)
            │       └── Sub-Task 4 (Dockerfile)
            │               ├── Sub-Task 5 (GitHub Actions)
            │               └── Sub-Task 6 (Jenkins)
            └── Sub-Task 7 (README) — can be done last, after all other tasks
```

Sub-tasks 5, 6, and 7 can be done in parallel once Sub-Task 4 is complete.
Sub-Task 7 should be finalised last so it accurately reflects the finished state.

---

## File Layout (Final State)

```
aceest-devops/                         ← repo root
├── app.py                             ← Flask application
├── schema.sql                         ← SQLite DDL
├── requirements.txt                   ← Python dependencies
├── Dockerfile                         ← Container image definition
├── .dockerignore
├── .gitignore
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── client_form.html
│   ├── client_detail.html
│   ├── workout_form.html
│   └── workout_history.html
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_clients.py
│   ├── test_progress.py
│   └── test_workouts.py
└── .github/
    └── workflows/
        └── main.yml
```
