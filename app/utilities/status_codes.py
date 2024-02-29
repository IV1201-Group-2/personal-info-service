class StatusCodes:
    """
    Represents the HTTP status codes that can be returned by the API.

    :ivar OK: The request was successful.
    :ivar CREATED: The resource was created successfully.
    :ivar BAD_REQUEST: The request was malformed.
    :ivar UNAUTHORIZED: The request was unauthorized.
    :ivar FORBIDDEN: The request was forbidden.
    :ivar NOT_FOUND: The resource was not found.
    :ivar INTERNAL_SERVER_ERROR: An internal server error occurred.
    """

    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
