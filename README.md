# 🛒 GexyShop - Django E-commerce Backend

A production-style e-commerce backend built with Django, focusing on **clean architecture**, **service layer separation**, and **testable business logic**.

This project is designed as a **portfolio project** to demonstrate backend engineering skills rather than frontend/UI design.

---

## 📌 Overview

This project implements a simple online shop with features such as:

- Service Layer Architecture
- JWT-based authentication
- Product catalog and search
- Shopping cart management
- Wishlist system
- Coupon & discount system
- Order management
- Online payment integration (Zibal)
- Payment verification & stock management
- Product recommendation system
- Redis caching
- RESTful APIs
- Dockerized deployment
- Unit Tested Business Logic

---

## 🧰 Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- SimpleJWT
- Docker
- Docker Compose
- pytest / pytest-django
- Zibal Payment Gateway

---

## 🗂 Project Structure

```text
project_django/
├── accounts/        # Authentication, user addresses
│   ├── api/
├── cart/            # Shopping cart logic
│   ├── api/
├── comments/        # Product comments
│   ├── api/
├── gexyshop/        # Core project configuration
├── main/            # Homepage & landing views
├── media/           # Uploaded media
├── orders/          # Orders, payments, service layer
│   ├── api/
│   ├── services.py
│   └── tests/
├── products/        # Product catalog
│   ├── api/
├── static/          # Static assets
├── templates/       # HTML templates
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── pytest.ini
├── README.md
└── requirements.txt
---


---

## 🧠 Architecture

This project follows a Service Layer architecture.

Business logic is extracted from Django views and placed inside service classes.
Views are kept thin and are only responsible for handling HTTP requests and responses.

```text
Request
   ↓
View
   ↓
Service Layer
   ↓
Model
   ↓
Database
```

This approach improves:

- Code readability
- Testability
- Maintainability
- Separation of concerns


## 🔐 Authentication

JWT-based authentication is implemented using SimpleJWT.

Features:

- Access Token
- Refresh Token
- User Registration
- Login
- Logout
- Password Change
- Authenticated Profile Management

## 🌐 REST API Features

- User Registration API
- JWT Login / Refresh Token
- Profile Management API
- Password Change API
- Product List API
- Product Detail API
- Product Search API
- Shopping Cart API
- Wishlist API
- Coupon System API
- Order Management API
- Payment Request API
- Payment Verification API
- Product Recommendation API
- Comment System API

## 🧩 Service Layer

Business logic is implemented inside dedicated service classes.

### PaymentService

```python
PaymentService.verify_and_pay_order(order, track_id)
```


Responsibilities:

- Verify payment with Zibal gateway
- Handle duplicate (idempotent) callbacks
- Validate product stock
- Update order status atomically
- Reduce product stock
- Clear cart after successful payment

## ⚡ Caching Strategy

Cache invalidation is performed automatically whenever product data changes.

Cached Endpoints:

- Product List API
- Product Detail API

## 💡 Product Recommendation

A recommendation engine suggests products based on:

- User purchase history
- Wishlist activity
- Product categories

## 🐳 Docker Support

The project is fully containerized using Docker and Docker Compose.

Included services:

- Django Application
- PostgreSQL Database
- Redis Cache

Development environment can be started with a single command using Docker Compose.

## 🏗 Engineering Concepts Demonstrated

- Service Layer Architecture
- Database Transactions
- JWT Authentication
- Redis Caching
- REST API Design
- External Payment Integration
- Unit Testing
- Permission-based Access Control
- Docker Containerization
- Performance Optimization

## 💳 Payment Flow

1. User confirms the order
2. Order is created
3. Payment request is sent to Zibal
4. User is redirected to the payment gateway
5. Gateway redirects to callback URL
6. Payment is verified
7. Stock is updated atomically
8. Cart is cleared
9. Order status becomes Paid

## 🧪 Testing
Unit tests are written for service layer business logic.

Covered scenarios:

- Successful payment verification
- Duplicate payment handling
- Payment gateway failures
- Stock validation errors
- Coupon validation
- Order status updates

Tools:

- pytest
- pytest-django
- mocking external HTTP requests

## ⭐ Key Features

- Service Layer Architecture
- JWT Authentication
- Redis Caching
- Dockerized Environment
- Payment Gateway Integration
- Product Recommendation System
- Coupon & Discount System
- Wishlist Functionality
- Unit Tested Business Logic
- PostgreSQL Database

## ⚙️ Setup & Run

### Prerequisites

- Python 3.x
- PostgreSQL
- Redis
- Docker (optional)

### Installation

```bash
git clone <repository-url>
cd project_django
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables

```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

REDIS_HOST=localhost
REDIS_PORT=6379
```

### Run Migrations and Server

```bash
python manage.py migrate
python manage.py runserver
```

### Run with Docker

```bash
docker-compose up --build
```

### Run Tests

```bash
pytest
```

## 👤 Author
Developed by Saba Boustan Doust

## 📌 Note
This project is focused on backend architecture and business logic.
Frontend templates are intentionally kept minimal.
