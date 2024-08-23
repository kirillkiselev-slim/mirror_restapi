# Dog Walking Service API

This project is a simple REST API for managing dog walking services. The API allows users to book dog walking appointments for their pets and retrieve existing appointments.

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kirillkiselev-slim/mirror_restapi
cd restapi_mirrorapp
```

### Create venv env
- python -m venv venv
#### On Mac
- `source venv/bin/activate`
#### On Windows
- `venv\Scripts\activate`

### Set Up the Database
1. `flask db init`
2. `flask db migrate`
3. `flask db upgrade`


### Run the Application
`flask run`


# Endpoints

## 1. Get Orders for a Specific Date

- **Endpoint:** `/orders/<date>`
- **Method:** `GET`
- **Description:** Retrieves all orders for a specific date.
- **Parameters:**
  - `date` (in `YYYY-MM-DD` format): The date for which you want to see the orders.
- **Response:**

```json
[
  {
    "apartment_number": "23",
    "pet_name": "Rex",
    "breed": "Terrier",
    "walk_time": "2024-08-23 07:30",
    "walker": "Anton"
  }
]
```

## 2. Create a New Order

- **Endpoint:** `/order`
- **Method:** `POST`
- **Description:** Creates a new order for a dog walking appointment.
- **Request Body:**

```json
{
  "apartment_number": "23",
  "pet_name": "Rex",
  "breed": "Terrier",
  "walk_time": "2024-08-23 07:30",
  "walker": "Anton"
}
```

**Response:**

- `201 Created:` Order created successfully.
- `400 Bad Request:` Error messages for invalid input (e.g., missing required fields, booking conflicts).

**Example Error Response:**

```json
{
  "error": "The walker is already booked at this time"
}
```


### Validation Rules

- Walk times must be in the format `'%Y-%m-%d %H:%M'`.
- Walk times are restricted to start only at 00:00 or 00:30 intervals (e.g., 07:00, 11:30).
- The earliest available walk is 07:00, and the latest is 22:30.
- Each walker (Petr or Anton) can only have one walk scheduled at any given time.

