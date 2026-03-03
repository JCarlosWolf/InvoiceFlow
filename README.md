# InvoiceFlow

InvoiceFlow is a production-ready backend API designed to support internal invoicing operations within a single-company environment.

The system focuses on secure multi-user access, controlled data isolation, and clean business-oriented architecture. It was built to reflect real-world enterprise backend standards rather than tutorial-style CRUD applications.

---

## Executive Summary

InvoiceFlow demonstrates how backend systems can be structured to support controlled financial workflows inside an organization.

Key characteristics:

- Secure multi-user authentication
- Strict user-level data isolation
- Modular and maintainable architecture
- Automated testing validation
- Containerized deployment for operational consistency

This project represents a backend foundation for internal business process automation.

---

## Technology Stack

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic migrations
- JWT-based authentication
- Docker & Docker Compose
- Pytest automated testing

---

## System Design Philosophy

The system was designed following enterprise-oriented backend principles:

- Separation of concerns
- Service-layer abstraction for business logic
- Secure authentication and protected endpoints
- Scalable modular structure
- Reproducible containerized environments

## Project Structure

```
app/
├── api/        # Endpoint definitions
├── core/       # Security and configuration
├── models/     # Database models
├── schemas/    # Data validation schemas
├── services/   # Business logic layer
├── database.py # Database engine and session management
```

## Security & Access Control

- OAuth2 password flow
- JWT token generation
- Password hashing
- Protected routes
- User-level invoice ownership enforcement

Each authenticated user can only access and manage their own invoice records.

---

## Automated Testing

The project includes automated test coverage for:

- User registration flow
- Authentication and token issuance
- Endpoint protection validation
- Invoice creation workflows
- Multi-user data isolation scenarios
- Core business logic validation

Run all tests:

```bash
pytest

All tests must pass before production deployment.

Containerized Deployment

The application is fully containerized.

To run locally:

docker compose up --build

This command:

Launches PostgreSQL

Configures environment variables

Starts the FastAPI application

Interactive API documentation available at:

http://localhost:8000/docs
Business Relevance

InvoiceFlow is structured to simulate a controlled internal invoicing system, demonstrating:

Backend discipline aligned with business requirements

Secure operational workflows

Data segregation principles

Production-ready configuration practices

It represents a foundational backend component for broader business process automation systems.

Author

José Carlos Lobo
Backend Developer – Business Process Automation
