### **1. Executive Summary**

**Application Name:** Baggers
**Objective:** To create a simple, server-based application for a small group to manage and share contact details and AFL membership numbers.
**Technology Stack:** FastAPI (Python web framework), SQLite (database).
**Core Functionality:** The application will provide full CRUD (Create, Read, Update, Delete) capabilities for user records via a RESTful API.
**Project Tooling:** `uv` will be used for environment management, dependency installation, and running the application. `pytest` will be used for all testing.

---

### **2. Development Environment and Tooling**

The project will be developed using Python. To ensure a consistent and reproducible environment, specific tools will be mandated.

*   **Environment and Package Manager:** `uv` will be used to create and manage a project-specific virtual environment (`uv venv`) and to handle the installation and management of all Python dependencies from a `pyproject.toml` file.
*   **Application Server:** The application will be served using `uvicorn`, an ASGI server. `uv` will be used to run the development server (`uv run uvicorn baggers.main:app --reload`).
*   **Testing Framework:** `pytest` will be the framework for writing and running all tests. It will be included as a development dependency.

---

### **3. System Architecture**

The application will feature a modular, multi-tiered architecture for a clear separation of concerns.

*   **Presentation Layer (API):** FastAPI will define API endpoints, handle HTTP requests, and send responses.
*   **Business Logic Layer (CRUD Operations):** This layer will contain the core application logic for database interactions.
*   **Data Access Layer (Database Interaction):** SQLAlchemy will serve as the ORM to map Python objects to database records.
*   **Database Layer:** A single SQLite database file will provide data persistence.

---

### **4. Project Structure**

The project will be organized into a main application package (`baggers`) and a separate directory for tests (`tests/`).

```
baggers-project/
├── .venv/                      # Virtual environment managed by uv
├── baggers/                    # Main application package
│   ├── __init__.py             # Makes the directory a Python package
│   ├── main.py                 # FastAPI app initialization and router inclusion
│   ├── router.py               # API endpoint definitions (the Presentation Layer)
│   ├── crud.py                 # Business logic for database operations
│   ├── models.py               # SQLAlchemy database models (the Data Access Layer)
│   ├── schemas.py              # Pydantic data validation models (DTOs)
│   └── database.py             # Database engine and session configuration
├── tests/                      # Directory for all tests
│   ├── __init__.py
│   ├── test_crud.py            # Unit tests for business logic
│   ├── test_api.py             # Integration tests for API endpoints
│   └── conftest.py             # pytest fixtures and test setup
├── .gitignore                  # Git ignore file
├── pyproject.toml              # Project metadata and dependencies for uv/pip
└── README.md                   # Project documentation
```

---

### **5. Database Design**

The application will use a single SQLite database file (`baggers.db`).

#### **5.1. Database Schema**

**Table: `Baggers`**

| Field Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTOINCREMENT` | A unique, auto-generated identifier. |
| `name` | `TEXT` | `NOT NULL` | The full name of the person. |
| `membershipNo` | `TEXT` | `NOT NULL`, `UNIQUE` | The unique AFL membership number. |
| `emailAddress` | `TEXT` | `NULLABLE` | The person's email address. |
| `phoneNumber` | `TEXT` | `NULLABLE` | The person's phone number. |

---

### **6. API Design**

A RESTful API will be exposed with the base URL `/baggers`.

#### **6.1. Data Transfer Objects (DTOs)**

Pydantic models (in `schemas.py`) will be used for data validation and serialization.

*   `BaggerBase`: `name`, `membershipNo`, `emailAddress`, `phoneNumber`.
*   `BaggerCreate`: Inherits from `BaggerBase` for creating new records.
*   `Bagger`: Inherits from `BaggerBase` and adds the `id` field for API responses.

#### **6.2. API Endpoints**

| HTTP Method | Path | Description | Success Response |
| :--- | :--- | :--- | :--- |
| `POST` | `/baggers/` | Creates a new Bagger record. | `200 OK` with a `Bagger` object. |
| `GET` | `/baggers/` | Retrieves a list of all Bagger records. | `200 OK` with a list of `Bagger` objects. |
| `GET` | `/baggers/{bagger_id}` | Retrieves a single Bagger record by its `id`. | `200 OK` with a `Bagger` object. |
| `PUT` | `/baggers/{bagger_id}` | Updates an existing Bagger record. | `200 OK` with the updated `Bagger` object. |
| `DELETE` | `/baggers/{bagger_id}` | Deletes a Bagger record by its `id`. | `200 OK` with the deleted `Bagger` object. |

#### **6.3. Error Handling**

*   **`404 Not Found`:** For requests targeting a non-existent `bagger_id`.
*   **`422 Unprocessable Entity`:** For request validation failures.

---

### **7. Testing Strategy**

The application will be thoroughly tested using `pytest`. The testing strategy will be divided into two main categories: unit tests and integration tests. A separate, in-memory SQLite database will be used for testing to ensure that tests are fast, isolated, and do not affect the development database.

#### **7.1. Test Setup (`conftest.py`)**

A `conftest.py` file will be used to define `pytest` fixtures that provide the necessary setup for the test suite. This includes:
*   A fixture to create and manage an in-memory SQLite database session for the duration of the tests.
*   A fixture to provide a test client for the FastAPI application, allowing tests to make HTTP requests to the API endpoints without a running server.

#### **7.2. Unit Tests (`test_crud.py`)**

Unit tests will focus on testing the business logic in isolation. They will directly call the functions in `crud.py` to verify their correctness.
*   **Create:** Test that `create_bagger` correctly adds a new record to the database.
*   **Read:** Test that `get_bagger` retrieves the correct record and `get_baggers` retrieves all records.
*   **Update:** Test that `update_bagger` correctly modifies an existing record.
*   **Delete:** Test that `delete_bagger` correctly removes a record from the database.
*   **Constraints:** Test that database constraints (e.g., the `UNIQUE` constraint on `membershipNo`) are enforced.

#### **7.3. Integration Tests (`test_api.py`)**

Integration tests will focus on testing the application as a whole, from the API endpoint to the database. They will use the `TestClient` to simulate HTTP requests and validate the responses.
*   **POST `/baggers/`:** Test successful creation and verify the `200` status code and response body. Test creation with invalid data to verify the `422` status code.
*   **GET `/baggers/`:** Test successful retrieval of a list of baggers.
*   **GET `/baggers/{bagger_id}`:** Test successful retrieval of a single bagger. Test retrieval of a non-existent bagger to verify the `404` status code.
*   **PUT `/baggers/{bagger_id}`:** Test successful updates and verify the response. Test updates for non-existent baggers (`404`) and with invalid data (`422`).
*   **DELETE `/baggers/{bagger_id}`:** Test successful deletion. Test deletion of a non-existent bagger to verify the `404` status code.