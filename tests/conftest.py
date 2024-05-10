import os

import pytest

from project import create_app
from project.models import User


@pytest.fixture()
def app():
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    flask_app = create_app()

    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="module")
def new_user():
    return User("usertest", "test")
