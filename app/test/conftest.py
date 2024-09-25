import sys
import pathlib
from unittest.mock import Mock

import pytest

from database import db
from api.service.api_requests import PagerDutyAPI
from api.service.data_storage import DataStorage
from config import Config
from app import app as flask_app

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))



@pytest.fixture(scope="session")
def app():
    return flask_app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function") # To avoid test contamination
def session(app):
    with app.app_context():
        db.engine.echo = True
        db.create_all()
        try:
            yield db.session
        finally:
            db.session.close()
            db.drop_all()


@pytest.fixture(scope="session")
def pagerduty_api():
    return PagerDutyAPI(base_url="https://api.pagerduty.com", token_api=Config.PAGERDUTY_API_KEY)

