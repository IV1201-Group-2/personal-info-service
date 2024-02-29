import logging

from flask import jsonify, request

from app.utilities.status_codes import StatusCodes


def handle_all_unhandled_exceptions(exception):
    """
    Handle all unhandled exceptions.

    This function handles all unhandled exceptions by logging the exception and
    returning a JSON response with an 'INTERNAL_SERVER_ERROR' message and a 500
    status code.

    :param exception: The unhandled exception.
    :returns: A tuple containing a JSON response and a status code.
    """

    requester_ip = request.remote_addr
    logging.debug(f'{requester_ip} - ' + str(exception))
    return (jsonify({'error': 'INTERNAL_SERVER_ERROR'}),
            StatusCodes.INTERNAL_SERVER_ERROR)
