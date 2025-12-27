# 🛒 GexyShop - Django E-commerce Backend

A production-style e-commerce backend built with Django, focusing on **clean architecture**, **service layer separation**, and **testable business logic**.

This project is designed as a **portfolio project** to demonstrate backend engineering skills rather than frontend/UI design.

---

## 📌 Overview

This project implements a simple online shop with features such as:

- User authentication
- Product listing
- Shopping cart
- Order creation
- Online payment integration
- Payment verification
- Stock management

The main goal of this project is to showcase:
- Proper project structure
- Separation of concerns
- Real-world payment flow
- Unit testing of business logic

---

## 🧰 Tech Stack

- **Python**
- **Django**
- **pytest / pytest-django**
- **PostgreSQL (primary database)**
- **Zibal Payment Gateway**
  Zibal is used as a real Iranian payment gateway to simulate a production payment flow.
- HTML / CSS / JavaScript (basic frontend)

---

## 🗂 Project Structure

```text
project_django/
├── accounts/        # Authentication, user addresses
├── cart/            # Shopping cart logic
├── comments/        # Product comments
├── main/            # Homepage & landing views
├── orders/          # Orders, payments, service layer
│   ├── services.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
│       ├── conftest.py
│       └── test_payment_service.py
├── products/        # Product catalog
├── templates/       # HTML templates (per app)
├── static/          # Static assets (css, js, images)
├── media/           # Uploaded media
├── manage.py
├── pytest.ini
└── README.md

---

🧠 Architecture

This project follows a Service Layer architecture.

Business logic is extracted from Django views and placed inside service classes.
Views are kept thin and are only responsible for handling HTTP requests and responses.

View → Service → Model


This approach improves:

Code readability

Testability

Maintainability

Separation of concerns

🧩 Service Layer

Business logic is implemented inside dedicated service classes.

PaymentService

The PaymentService handles all payment-related logic:

PaymentService.verify_and_pay_order(order, track_id)


Responsibilities:

Verify payment with Zibal gateway

Handle duplicate (idempotent) callbacks

Validate product stock

Update order status atomically

Reduce product stock

Clear cart after successful payment

All critical operations are wrapped inside a database transaction.

💳 Payment Flow

User confirms the order

Payment request is sent to Zibal

User is redirected to the payment gateway

Gateway redirects back to callback URL

Payment is verified inside the service layer

Order status is updated and stock is reduced

🧪 Testing

Unit tests are written for service layer logic, not views.

Covered scenarios:

Successful payment

Duplicate payment verification

Payment gateway failure

Stock validation errors

Testing tools:

pytest

pytest-django

mocking external HTTP requests

⚙️ Setup & Run
Prerequisites

Python 3.x

PostgreSQL

Installation
git clone <repository-url>
cd project_django
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Environment Variables

Create a .env file and configure database settings:

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

Run migrations and server
python manage.py migrate
python manage.py runserver

Run tests
pytest

👤 Author

Developed by Saba Boustan Doust

📌 Note:
This project is focused on backend architecture and business logic.
Frontend templates are intentionally kept minimal.
