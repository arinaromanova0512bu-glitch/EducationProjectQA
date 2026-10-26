# E-Commerce QA Automation Project

Automated API and UI testing project for an e-commerce application.

The project demonstrates practical skills in test automation using Python, pytest, Playwright, and REST API testing.

It includes positive and negative test scenarios, reusable API clients, Page Object Model architecture, test fixtures, and Allure reporting.

## Tech Stack

- Python 3.11
- pytest
- Playwright
- requests
- Faker
- Allure Report
- REST API
- Page Object Model (POM)

## Test Coverage

### API Tests

Automated API tests cover the following functionality:

**Authentication**
- User registration
- User login
- Positive and negative authentication scenarios
- Input validation

**User Management**
- Retrieve user information
- Delete users
- Authorization and access control
- Invalid and missing access tokens

**Catalog**
- Product catalog functionality
- Product-related API scenarios

**Shopping Cart**
- Shopping cart operations
- Cart-related API scenarios

**Orders**
- Order management functionality
- Order-related API scenarios

**Promotions**
- Promotional functionality
- Promo-related API scenarios

### UI Tests

UI automation is implemented using Playwright and the Page Object Model pattern.

The test suite covers:

- Authentication
- Product catalog
- Shopping cart
- Checkout
- Orders

## Project Architecture

The project separates test logic from API interaction and UI page interactions.

```text
EducationProjectQA/
│
├── api_clients/
│   ├── auth_client.py
│   ├── base_http_client.py
│   ├── cart_client.py
│   ├── catalog_client.py
│   ├── order_client.py
│   └── users_client.py
│
├── pages/
│   ├── auth_page.py
│   ├── base_page.py
│   ├── cart_page.py
│   ├── catalog_page.py
│   ├── checkout_page.py
│   └── orders_page.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_cart.py
│   ├── test_catalog.py
│   ├── test_orders.py
│   ├── test_promo.py
│   └── test_users.py
│
├── ui_tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_cart.py
│   ├── test_catalog.py
│   ├── test_checkout.py
│   └── test_orders.py
│
├── config.py
├── pytest.ini
└── README.md
```

## Running the Tests

### 1. Install dependencies

```bash
pip install pytest requests Faker playwright allure-pytest
```

Install Playwright browsers:

```bash
playwright install
```

### 2. Start the application

The application backend is maintained separately and must be running before executing the tests.

Default API address:

```text
http://localhost:8080
```

### 3. Run API tests

```bash
python -m pytest tests/
```

### 4. Run UI tests

```bash
python -m pytest ui_tests/
```

### 5. Run all tests

```bash
python -m pytest
```

### 6. Run smoke tests

```bash
python -m pytest -m smoke
```

## Allure Reporting

The project uses Allure for test execution reporting.

Generate test results:

```bash
python -m pytest --alluredir=allure-results
```

Generate and open the report locally:

```bash
allure serve allure-results
```

### Published Allure Report

**[View Allure Test Report](https://arinaromanova0512bu-glitch.github.io/EducationProjectQA/)**

The published report contains the results of 55 successfully executed automated tests.

## Configuration

The API base URL can be configured using the `BASE_URL` environment variable.

Example:

```bash
BASE_URL=http://localhost:8080 python -m pytest
```

## About the Project

This repository contains the automated testing component of a training e-commerce application.

The backend application is maintained separately and serves as the system under test.

The project was developed to practice API and UI test automation, test architecture, reusable components, and automated reporting.