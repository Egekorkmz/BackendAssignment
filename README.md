# Car Rental Backend API

## Overview

This project is a Flask-based backend API for a car rental service. It supports user registration, authentication, car management, and rental operations. The backend uses PostgreSQL for data storage and SQLAlchemy for ORM.

## Features

- User registration and authentication (Basic Auth)
- Merchant and user roles
- Car CRUD operations (add, update, delete, list)
- Car rental and return
- Rental history with filtering
- Alembic migrations for database schema management

## Project Structure

## Project Structure (Detailed)

```
.
├── app/
│   ├── __init__.py           # App factory and initialization
│   ├── config.py             # Configuration settings
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── user.py           # User and merchant models
│   │   ├── car.py            # Car model
│   │   └── rental.py         # Rental model
│   ├── controllers/          # Business logic
│   │   ├── auth_controller.py
│   │   ├── car_controller.py
│   │   └── rental_controller.py
│   ├── routes/               # API route definitions
│   │   ├── auth_routes.py
│   │   ├── car_routes.py
│   │   └── rental_routes.py
│   └── utils/                # Utility functions/helpers
│       ├── validators.py     # Data validation helpers
│       └── auth.py           # Authentication helpers
├── migrations/               # Alembic migration scripts
│   └── ...                   # (auto-generated files)
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Docker Compose for PostgreSQL
├── run.py                    # Entry point to start the app
├── README.md                 # Project documentation
```

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Start PostgreSQL using Docker Compose**
   ```sh
   docker-compose up -d
   ```
4. **Run database migrations**
   ```sh
   flask db upgrade
   ```
5. **Start the Flask app**
   ```sh
   python run.py
   ```

## API Endpoints

### Auth

- `POST /auth/register` — Register a new user or merchant
- `POST /auth/login` — Login with Basic Auth

### Car

- `POST /car/add` — Add a new car (merchant only)
- `PUT /car/update/<car_id>` — Update car details (merchant only)
- `DELETE /car/delete/<car_id>` — Delete a car (merchant only)
- `GET /car/list` — List cars (with filters)

### Rental

- `POST /rental/rent/<car_id>` — Rent a car
- `POST /rental/return/<car_id>` — Return a rented car
- `GET /rental/history/<username>` — Get rental history (with filters)

## Database

- PostgreSQL (configured in `docker-compose.yml` and `app/config.py`)

## Migrations

- Alembic is used for database migrations. Migration scripts are in the `migrations/` directory.

---

For more details, see the source code and comments in each file.
