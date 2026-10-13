-- ACEest Fitness & Gym — SQLite schema
-- Tables: clients, progress, workouts

CREATE TABLE IF NOT EXISTS clients (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    name              TEXT UNIQUE NOT NULL,
    age               INTEGER,
    height            REAL,
    weight            REAL,
    program           TEXT,
    calories          INTEGER,
    target_weight     REAL,
    target_adherence  INTEGER
);

CREATE TABLE IF NOT EXISTS progress (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name  TEXT NOT NULL,
    week         TEXT NOT NULL,
    adherence    INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS workouts (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name   TEXT NOT NULL,
    date          TEXT NOT NULL,
    workout_type  TEXT NOT NULL,
    duration_min  INTEGER NOT NULL,
    notes         TEXT
);
