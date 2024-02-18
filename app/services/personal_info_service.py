from app.repositories.personal_info_repository import get_person_from_db


def fetch_personal_info(person_id: int) -> dict[str, str]:
    """
    Fetches personal information for a specified user ID.

    This function retrieves the personal information of a user from the
    database using the provided user ID. The information is then converted
    into a dictionary and returned.
    into a dictionary and returned.

    :param person_id: The ID of the user to fetch information for.
    :returns: A dictionary containing the personal information of the user.
    :raises PermissionError: If the user has a role_id of 1.
    """

    person = get_person_from_db(person_id)
    if person.role_id == 1:
        raise PermissionError

    return get_person_from_db(person_id).to_dict()
