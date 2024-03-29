import datetime

from flask_jwt_extended import create_access_token

from tests.utilities.test_status_codes import StatusCodes
from tests.utilities.test_utilities import generate_token_for_person_id_1, \
    remove_users_from_db, setup_test_user_1_in_db


def test_valid_token(app_with_client):
    app, test_client = app_with_client
    setup_test_user_1_in_db(app)
    valid_token = generate_token_for_person_id_1(app)

    response = test_client.get(
            '/api/applicant/personal-info/',
            headers={
                'Authorization': f'Bearer {valid_token}'})
    assert response.status_code == StatusCodes.OK
    remove_users_from_db(app)


def test_invalid_token(app_with_client):
    app, test_client = app_with_client
    setup_test_user_1_in_db(app)
    valid_token = generate_token_for_person_id_1(app)
    invalid_token = valid_token + 'invalid'

    response = test_client.get(
            '/api/applicant/personal-info/',
            headers={
                'Authorization': f'Bearer {invalid_token}'})
    assert response.status_code == StatusCodes.UNAUTHORIZED
    assert response.json['error'] == 'INVALID_TOKEN'


def test_expired_token(app_with_client):
    app, test_client = app_with_client
    setup_test_user_1_in_db(app)

    with app.app_context():
        expired_token = create_access_token(
                identity=None,
                additional_claims={'id': 1},
                expires_delta=datetime.timedelta(days=-1))

    response = test_client.get(
            '/api/applicant/personal-info/',
            headers={
                'Authorization': f'Bearer {expired_token}'})
    assert response.status_code == StatusCodes.UNAUTHORIZED
    assert response.json['error'] == 'TOKEN_EXPIRED'
    remove_users_from_db(app)


def test_unauthorized_request(app_with_client):
    app, test_client = app_with_client
    response = test_client.get(
            '/api/applicant/personal-info/')
    assert response.status_code == StatusCodes.UNAUTHORIZED
    assert response.json['error'] == 'UNAUTHORIZED'
