import os
import tempfile
import pytest
from app import create_app


@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    application = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )

    with application.app_context():
        application.init_db()

    yield application

    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()
