import datetime as dt
from datetime import datetime

from flask_jwt_extended import create_access_token

from app.extensions import database
from app.models.person import Person


def setup_test_user_1_in_db(app):
    with app.app_context():
        database.session.add(Person(name='test', surname='tester', role_id=2))
        database.session.commit()


def setup_test_user_2_in_db(app):
    with app.app_context():
        database.session.add(Person(name='user2', surname='tester', role_id=2))
        database.session.commit()


def setup_test_user_recruiter_in_db(app):
    with app.app_context():
        database.session.add(Person(name='recru', surname='iter', role_id=1))
        database.session.commit()


def remove_users_from_db(app):
    with app.app_context():
        database.session.query(Person).filter(Person.person_id == 1).delete()
        database.session.commit()


def generate_token_for_person_id_1(app) -> tuple[str, str]:
    with app.app_context():
        return create_access_token(identity=None,
                                   additional_claims={'id': 1, 'role': 2},
                                   expires_delta=dt.timedelta(days=1))


def generate_token_for_recruiter(app) -> tuple[str, str]:
    with app.app_context():
        return create_access_token(identity=None,
                                   additional_claims={'id': 2, 'role': 1},
                                   expires_delta=dt.timedelta(days=1))
