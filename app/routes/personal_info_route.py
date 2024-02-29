import logging
from typing import Optional

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.services.personal_info_service import fetch_personal_info
from app.utilities.status_codes import StatusCodes

personal_info_bp = Blueprint('personal-info', __name__)


@personal_info_bp.route('/', methods=['GET'])
@personal_info_bp.route('/<int:person_id>', methods=['GET'])
@jwt_required()
def get_personal_info(person_id: Optional[int] = None) -> tuple[Response, int]:
    """
    Retrieves personal information of a user.

    If no person_id is provided, it fetches the current user's information. If
    a person_id is provided, it fetches the information of the user with
    that id, given the current user has a role of 1.

    Returns a tuple containing the response and the status code.

    :param person_id: The id of the user to retrieve information for. If
                      None, retrieves current user's info.
    :returns: A tuple containing the response and the status code.
    :raises NoResultFound: If no user is found.
    :raises SQLAlchemyError: If there is a database issue.
    :raises PermissionError: If the person_id belonged to a recruiter.
    """

    requester_ip = request.remote_addr

    if person_id is None:
        person_id = get_jwt()['id']
    else:
        if person_id < 1 or person_id > 1000000:
            logging.warning(f' - {requester_ip} - Invalid person_id:'
                            f' {person_id}.')
            return jsonify({'error': 'INVALID_ID'}), StatusCodes.BAD_REQUEST
        if get_jwt()['role'] != 1:
            logging.warning(f' - {requester_ip} - Unauthorized access to '
                            f'personal info for id: {person_id}.')
            return jsonify({'error': 'UNAUTHORIZED'}), StatusCodes.UNAUTHORIZED

    try:
        personal_info = fetch_personal_info(person_id)
        logging.info(f' - {requester_ip} - Personal info fetched for id:'
                     f' {person_id}.')
        return jsonify(personal_info), StatusCodes.OK
    except NoResultFound:
        logging.warning(f' - {requester_ip} - User not found for id:'
                        f' {person_id}.')
        return jsonify({'error': 'USER_NOT_FOUND'}), StatusCodes.NOT_FOUND
    except SQLAlchemyError:
        logging.error(f' - {requester_ip} - Could not fetch user for id:'
                      f' {person_id}.')
        return (jsonify({'error': 'COULD_NOT_FETCH_USER'}),
                StatusCodes.INTERNAL_SERVER_ERROR)
    except PermissionError:
        logging.warning(f' - {requester_ip} - Unauthorized access to '
                        f'personal info for id: {person_id}.')
        return jsonify({'error': 'FORBIDDEN'}), StatusCodes.FORBIDDEN
