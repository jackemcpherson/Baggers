# Baggers

A simple server-based application for managing contact details and AFL membership numbers.

## Overview

Baggers is a FastAPI-based REST API that provides full CRUD (Create, Read, Update, Delete) capabilities for managing user records containing contact details and AFL membership numbers.

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Testing**: pytest
- **Package Management**: uv

## Features

- Create, read, update, and delete bagger records
- Unique AFL membership number validation
- Optional email and phone number fields
- Comprehensive error handling (404, 422)
- Full test coverage with unit and integration tests
- Interactive API documentation (Swagger UI)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jackemcpherson/Baggers.git
   cd Baggers
   ```

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

## Usage

### Running the Application

Start the development server:
```bash
uv run uvicorn baggers.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

Interactive documentation (Swagger UI): `http://127.0.0.1:8000/docs`

### Running Tests

Run all tests:
```bash
uv run pytest
```

Run tests with verbose output:
```bash
uv run pytest -v
```

Run specific test file:
```bash
uv run pytest tests/test_api.py -v
```

## API Endpoints

Base URL: `/baggers`

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| POST | `/baggers/` | Create a new bagger | 200 OK with bagger object |
| GET | `/baggers/` | Get all baggers | 200 OK with list of baggers |
| GET | `/baggers/{id}` | Get bagger by ID | 200 OK with bagger object |
| PUT | `/baggers/{id}` | Update existing bagger | 200 OK with updated bagger |
| DELETE | `/baggers/{id}` | Delete bagger by ID | 200 OK with deleted bagger |

### Data Model

```json
{
  "id": 1,
  "name": "John Doe",
  "membershipNo": "AFL12345",
  "emailAddress": "john@example.com",
  "phoneNumber": "0412345678"
}
```

**Note**: `emailAddress` and `phoneNumber` are optional fields.

### Example API Usage

**Create a new bagger**:
```bash
curl -X POST "http://127.0.0.1:8000/baggers/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "membershipNo": "AFL12345",
       "emailAddress": "john@example.com",
       "phoneNumber": "0412345678"
     }'
```

**Get all baggers**:
```bash
curl "http://127.0.0.1:8000/baggers/"
```

**Get a specific bagger**:
```bash
curl "http://127.0.0.1:8000/baggers/1"
```

**Update a bagger**:
```bash
curl -X PUT "http://127.0.0.1:8000/baggers/1" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Smith",
       "membershipNo": "AFL12345",
       "emailAddress": "johnsmith@example.com",
       "phoneNumber": "0412345678"
     }'
```

**Delete a bagger**:
```bash
curl -X DELETE "http://127.0.0.1:8000/baggers/1"
```

## Error Handling

- **404 Not Found**: When requesting a non-existent bagger ID
- **422 Unprocessable Entity**: For validation errors or duplicate membership numbers

## Database

The application uses SQLite with a single `baggers` table:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| name | TEXT | NOT NULL | Full name |
| membershipNo | TEXT | NOT NULL, UNIQUE | AFL membership number |
| emailAddress | TEXT | NULLABLE | Email address |
| phoneNumber | TEXT | NULLABLE | Phone number |

## Development

### Project Structure

```
Baggers/
├── .gitignore              # Git ignore rules
├── baggers/                # Main application package
│   ├── __init__.py
│   ├── main.py             # FastAPI app initialization
│   ├── router.py           # API endpoints
│   ├── crud.py             # Business logic
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   └── database.py         # Database configuration
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Test fixtures
│   ├── test_crud.py        # Unit tests
│   └── test_api.py         # Integration tests
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── README.md               # This file
├── DESIGN.md               # Original design specification
└── IMPLEMENTATION.md       # Implementation plan
```

### Key Commands

- **Install dependencies**: `uv sync`
- **Run application**: `uv run uvicorn baggers.main:app --reload`
- **Run tests**: `uv run pytest`
- **Run specific tests**: `uv run pytest tests/test_api.py`

## Contributing

1. Ensure all tests pass: `uv run pytest`
2. Follow the existing code style and patterns
3. Add tests for new functionality
4. Update documentation as needed

## License

This project is licensed under the MIT License.