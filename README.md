# Fitness Studio Booking API

A lightweight and robust RESTful API built with FastAPI for managing class bookings in a fictional fitness studio. It supports class listing, booking with availability checks, email-based retrieval, and timezone-adjusted scheduling.

---

## Features

- View all available fitness classes (`GET /classes`)
- Book a class (`POST /book`)
- Retrieve bookings (all or by email) (`GET /bookings`)
- Timezone support (classes default to IST, adjustable via query)
- In-memory SQLite DB for simplicity
- Logging & basic input validation
- Modular code structure and Pydantic models
- Unit tests using `pytest`

---

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** SQLite (in-memory/file)
- **ORM:** SQLAlchemy
- **Timezone:** pytz
- **Testing:** Pytest + HTTPX
- **Logging:** Python `logging` module

---

## Project Structure

fitness_api/
│

├── main.py # FastAPI application and routes

├── models.py # SQLAlchemy models

├── schemas.py # Pydantic request/response schemas

├── database.py # SQLite DB connection

├── seed.py # Seed sample data into DB

├── test_main.py # Unit tests

├── app.log # Log file (generated at runtime)

└── README.md # You're here!


## Setup Instructions

1. **Clone the repo:**

- bash
- git clone https://github.com/psmr-work/fitness-booking-api.git
- cd fitness-api


2. **Create a virtual environment and activate:**

- python -m venv venv
- source venv/bin/activate  # On Windows: venv\Scripts\activate


3. **Install Dependencies**

- pip install -r requirements.txt


4. **Seed the database with sample classes:**

- python seed.py


5. **Run the API**

- uvicorn main:app --reload


6. **Open the API docs in browser:**

- http://127.0.0.1:8000/docs


----

## Run Unit Tests

- pytest test_main.py

----

## Sample Seed Data

- The seed.py file adds 3 sample classes:
- Yoga (with slots)
- Zumba (with slots)
- HIIT (with slots)

- You can modify this file to add more classes or reset slot counts.

----

## Sample cURL Requests

1. **Get all classes**

- curl -X GET "http://localhost:8000/classes?tz=Asia/Kolkata" -H "accept: application/json"


2. **Book a class**

- curl -X POST "http://localhost:8000/book" -H "Content-Type: application/json" -d '{
  "class_id": 1,
  "client_name": "Alice",
  "client_email": "alice@example.com"
}'

3. **Get all bookings**

- curl -X GET "http://localhost:8000/bookings" -H "accept: application/json"


4. **Get booking by email**

- curl -X GET "http://localhost:8000/bookings" -H "accept: application/json"






## Author
Mahesh Reddy
