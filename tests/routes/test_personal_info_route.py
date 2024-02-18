from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from tests.utilities.test_status_codes import StatusCodes
from tests.utilities.test_utilities import generate_token_for_person_id_1, \
    generate_token_for_recruiter, remove_users_from_db, \
    setup_test_user_1_in_db, \
    setup_test_user_2_in_db, setup_test_user_recruiter_in_db


def test_get_personal_info_success(app_with_client):
    app, test_client = app_with_client
    setup_test_user_1_in_db(app)
    token = generate_token_for_person_id_1(app)

    response = test_client.get(
            '/api/applicant/personal-info/',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == StatusCodes.OK
    assert response.json['name'] == 'test'
    assert response.json['surname'] == 'tester'
    assert response.json['role'] == 2

    remove_users_from_db(app)


def test_get_personal_info_recruiter_success(app_with_client):
    app, test_client = app_with_client
    setup_test_user_1_in_db(app)
    setup_test_user_recruiter_in_db(app)
    token = generate_token_for_recruiter(app)

    response = test_client.get(
            '/api/applicant/personal-info/1',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == StatusCodes.OK
    assert response.json['name'] == 'test'
    assert response.json['surname'] == 'tester'
    assert response.json['role'] == 2

    remove_users_from_db(app)


def test_get_personal_info_unauthorized_access(app_with_client):
    app, test_client = app_with_client
    setup_test_user_1_in_db(app)
    setup_test_user_2_in_db(app)
    token = generate_token_for_person_id_1(app)

    response = test_client.get(
            '/api/applicant/personal-info/2',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == StatusCodes.UNAUTHORIZED

    remove_users_from_db(app)


def test_get_recruiter_unauthorized_access(app_with_client):
    app, test_client = app_with_client
    setup_test_user_recruiter_in_db(app)
    token = generate_token_for_recruiter(app)

    response = test_client.get(
            '/api/applicant/personal-info/2',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == StatusCodes.FORBIDDEN

    remove_users_from_db(app)


def test_get_personal_info_no_result(app_with_client):
    app, test_client = app_with_client
    remove_users_from_db(app)
    token = generate_token_for_person_id_1(app)

    response = test_client.get(
            '/api/applicant/personal-info/',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == StatusCodes.NOT_FOUND
    assert response.json['error'] == 'USER_NOT_FOUND'


@patch('app.routes.personal_info_route.fetch_personal_info')
def test_get_personal_info_sqlalchemy_error(mock_fetch, app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_person_id_1(app)

    mock_fetch.side_effect = SQLAlchemyError("A database error occurred")

    response = test_client.get(
            '/api/applicant/personal-info/',
            headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == StatusCodes.INTERNAL_SERVER_ERROR
    assert response.json['error'] == 'COULD_NOT_FETCH_USER'
