# Application Form API

This API is used by applicants to submit their application for a job. The API allows applicants to check their
registered personal information as well as submit an application. Recruiters can also check the personal information of
applicants.

## Personal Info Endpoint

`GET /api/personal-info`
`GET /api/personal-info/<int:person_id>`

### Additional requirements

* The user must be logged in when calling this API
* The user's JWT token must be included in the `Authorization` header
* For the second URL, the user must have a role of 1 to fetch another user's information
* Information of a user with a role of 1 (recruiter) cannot be retrieved

### Successful response

The API returns an object with the following structure:

```json
{
  "id": 1,
  "name": "John",
  "surname": "Doe",
  "pnr": "1234567890",
  "email": "johndoe@example.com",
  "username": "johndoe",
  "role": 2
}
```

### Error responses

#### `USER_NOT_FOUND` (404 Not Found)

No user was found with the ID specified in the JWT token

#### `COULD_NOT_FETCH_USER` (500 Internal Server Error)

There was an issue with the database operation when trying to fetch the user's information

#### `UNAUTHORIZED` (401 Unauthorized)

User is not logged in (JWT token was not provided or is invalid)

#### `FORBIDDEN` (401 Forbidden)

The person_id provided in the URL belonged to a recruiter

#### `INVALID_TOKEN` (401 Unauthorized)

The provided JWT token is invalid (e.g., it is expired, not yet valid, or does not contain the required claims)

#### `TOKEN_NOT_PROVIDED` (401 Unauthorized)

No JWT token was provided in the `Authorization` header

#### `TOKEN_REVOKED` (401 Unauthorized)

The provided JWT token has been revoked

## Installation

This project uses pip for package management. The dependencies for the project are listed in the `requirements.txt`
and `requirements-dev.txt` files.

### Installing Dependencies

To install the dependencies for this project, follow the steps below:

1. Create a virtual environment (optional, but recommended):

```bash
python -m venv env
```

2. Activate the virtual environment:

On Windows:

```bash
env\Scripts\activate
```

On Unix or MacOS:

```bash
source env/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

### Installing Development Dependencies

If you plan to contribute to the project, you should also install the development dependencies. After activating your
virtual environment, run:

```bash
pip install -r requirements-dev.txt
```

## Deployment

The application is designed to be deployed on Heroku. You can follow the steps below to deploy the application:

1. Create a new Heroku application.
2. Set the `DATABASE_URL` environment variable in the Heroku application settings to your PostgreSQL database URL.
3. Push the application code to the Heroku application's Git repository.

## Database Configuration

The application uses PostgreSQL as its database. The database URL should be set in the `DATABASE_URL` environment
variable.

## Testing

Tests are written using pytest. You can run the tests by executing the following command in the root directory of the
project:

```bash
pytest
```

## Linting

Flake8 is used for linting the code. You can run the linter by executing the following command in the root directory of
the project:

```bash
flake8 --show-source app tests
```

## Static Analysis

Mypy is used for static type checking. You can run the static type checker by executing the following command in the
root directory of the project:

```bash
mypy app tests
```