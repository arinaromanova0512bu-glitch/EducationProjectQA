# EducationProjectQA

API test automation project for an e-commerce backend, created as part of my QA Automation training.

The repository contains automated REST API tests covering authentication and user management functionality, including positive and negative scenarios.

## Tech Stack

- Python 3.11
- pytest
- requests
- Faker
- REST API

## Test Coverage

### Authentication

- User registration
- User login
- Validation of required fields
- Invalid credentials
- Invalid registration data
- Authentication error scenarios

### Users

- Get user by ID
- Delete user
- Authorization checks
- Requests without an access token
- Requests with an invalid access token
- Access to another user's data
- Requests for non-existent users
- Repeated user deletion

## Project Structure

```text
tests/
├── api_client.py
├── conftest.py
├── test_auth.py
└── test_users.py
```

- `api_client.py` — API configuration
- `conftest.py` — shared pytest fixtures and test data
- `test_auth.py` — authentication and registration tests
- `test_users.py` — user management tests

## Running the Tests

Install the required dependencies:

```bash
pip install pytest requests Faker
```

Run the complete test suite:

```bash
python -m pytest
```

Run tests with verbose output:

```bash
python -m pytest -v
```

## Configuration

The API base URL can be configured using the `BASE_URL` environment variable.

By default, the tests use:

```text
http://localhost:8080
```

Example:

```bash
BASE_URL=http://localhost:8080 python -m pytest
```

## About the Project

This repository contains the test automation part of a training e-commerce project.

The backend application is maintained separately and is used as the system under test. The automated test suite is developed independently from the application source code.
