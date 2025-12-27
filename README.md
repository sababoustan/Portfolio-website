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
- **Pytest / pytest-django**
- **SQLite (development)**
- **Zibal Payment Gateway**
- HTML / CSS / JavaScript (basic frontend)

---

## 👤 Author
Developed by **Saba Boustan doust**

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

