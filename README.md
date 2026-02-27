# InvoiceFlow

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Tests](https://img.shields.io/badge/Tests-Pytest-success)

Production-ready FastAPI backend for invoice processing with OCR, VAT validation and JWT-based multi-user authentication.

---

## 🚀 Overview

InvoiceFlow is a secure backend API built with FastAPI that allows authenticated users to upload invoices (PDF or images), extract structured data, validate VAT calculations, and store them with strict multi-user isolation.

The project demonstrates backend architecture, authentication, validation logic, and automated testing practices.

---

## ✨ Features

- JWT Authentication (Register & Login)
- Password hashing with bcrypt
- Multi-user data isolation
- PDF text extraction (pdfplumber)
- Image OCR processing (Tesseract)
- VAT validation engine (multiple formats supported)
- Duplicate invoice detection (logical + DB constraint)
- Clean layered architecture
- Alembic migrations
- Automated test suite with pytest
- Mocked file-processing tests

---

## 🏗 Architecture

The project follows a layered architecture:


app/
├── api/ # FastAPI routers (HTTP layer)
├── core/ # Security & dependencies
├── models/ # SQLAlchemy ORM models
├── schemas/ # Pydantic validation schemas
├── services/ # Business logic layer
└── main.py # Application entry point

alembic/ # Database migrations
tests/ # Automated test suite


Separation of concerns ensures scalability, maintainability and testability.

---

## 🔐 Authentication & Security

- JWT-based authentication
- Token expiration control
- OAuth2PasswordBearer integration
- Password hashing with bcrypt
- Database-level multi-user isolation
- Unique constraints to prevent duplicate invoices

---

## 📄 Invoice Processing Flow

1. Authenticated user uploads a PDF or image.
2. Text is extracted (PDF parsing or OCR).
3. Structured invoice fields are parsed.
4. VAT validation engine verifies mathematical consistency.
5. Duplicate detection is performed.
6. Invoice is stored if valid.

### Supported VAT formats:

- Direct VAT amount (base + vat)
- Percentage (21)
- Decimal (0.21)
- Multiplier (1.21)

---

## 🧠 Design Decisions

- Business logic separated into service layer.
- Duplicate detection implemented both logically and at database constraint level.
- JWT authentication with expiration for stateless security.
- Test database isolated from production database.
- File processing mocked in tests to ensure deterministic behavior.

---

## 🧪 Testing

Run all tests:

```bash
pytest

Test coverage includes:

Authentication flow

Protected endpoints

Multi-user isolation

VAT validation logic

Mocked file upload flow

Duplicate prevention

The test suite uses an isolated SQLite database.

⚙️ Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/InvoiceFlow.git
cd InvoiceFlow

Create a virtual environment:

python -m venv .venv
source .venv/bin/activate      # Linux / Mac
.venv\Scripts\activate         # Windows

Install dependencies:

pip install -r requirements.txt
🔑 Environment Variables

Set environment variables before running:

SECRET_KEY=your-super-secret-key
DATABASE_URL=sqlite:///./invoiceflow.db
▶ Run the Application
uvicorn app.main:app --reload

Swagger UI available at:

http://127.0.0.1:8000/docs
🗄 Database Migrations

Apply migrations:

alembic upgrade head
🛠 Tech Stack

FastAPI

SQLAlchemy

Alembic

Pydantic

python-jose (JWT)

passlib (bcrypt)

pdfplumber

pytesseract

pytest

📌 Project Purpose

This project was built as a backend portfolio demonstration showcasing:

API design

Authentication and authorization

Data validation logic

Multi-user data isolation

Clean architecture principles

Automated testing practices

📜 License

MIT License
