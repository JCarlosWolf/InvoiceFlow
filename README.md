# InvoiceFlow API: Secure Internal Invoicing, Control Operations & Data Isolation System

**Developed by:** José Carlos Lobo  
**Main Stack:** Python | FastAPI | PostgreSQL | Docker | Pytest (Automated Testing)  

---

## Language / Idioma

* For technical and architectural documentation: 👉 **[Read in English](#english-version)**
* Para el caso de estudio orientado a negocio: 👉 **[Leer en Español](#spanish-version)**

---

<div id="english-version"></div>

# English Version

## 🎯 Executive Summary & Business Value

Within any organization's financial and administrative ecosystem, handling internal invoices and billing details demands three non-negotiable pillars: absolute access security, strict data traceability, and complete informational shielding (isolation). A simple data leak or an incorrect user assignment in financial documents can cause severe regulatory penalties and direct economic losses.

InvoiceFlow is a production-ready backend API meticulously engineered to support internal enterprise invoicing operations. Moving far away from standard tutorial CRUD apps, this system implements a strict user-level data isolation model. This ensures every internal manager or department works safely and independently within the very same corporate backend.

### 🏢 Corporate Impact & Relevance:
* Centralized Financial Control: Structures workflows under real-world internal auditing standards.
* Segregation of Duties & Data: Mitigates operational risk by making sure users only view, create, or update the billing records they legitimately own.
* Regulatory Compliance: Aligned with top data governance practices and strict access control frameworks required by highly regulated fields.

---

## 🚀 Key Features & Enterprise Value

* Advanced Access Control: Fully powered by OAuth2 password flows and secure JWT token issuance, accompanied by cryptographic password hashing.
* Strict Data Isolation: Custom per-user backend logic that validates ownership on every single HTTP request. No user can intercept or view another department's invoice by tampering with resource IDs.
* Operational Assurance via Automated Testing (pytest): Features a robust suite of automated tests checking critical paths (registration, token lifecycle, multi-user isolation scenarios) before allowing any code deployment, dropping human error rates to zero.
* Containerized Infrastructure: Production-ready container deployment with Docker, ensuring identical environments across staging, testing, and cloud deployment.

---

## 🛠️ System Architecture & Code Base Layout

Designed following strict separation of concerns and service-layer patterns to enforce maintainability and effortless long-term scaling:

Layout del Proyecto:
app/
├── api/        # Endpoint routes and protected access layers
├── core/       # Security protocols, token settings, and config (.env)
├── models/     # Database tables and relation mapping (SQLAlchemy ORM)
├── schemas/    # Pydantic input/output data validation schemas
├── services/   # Business logic layer (Financial rules and isolation checks)
└── database.py # Session manager and database engine lifecycle

---

## 📋 Installation & Local Deployment Guide

### Prerequisites
* Python 3.10+
* Docker & Docker Compose installed

### 1. Repository Setup
Comandos para ejecutar en consola:
git clone [https://github.com/JCarlosWolf/invoiceflow-api.git](https://github.com/JCarlosWolf/invoiceflow-api.git)
cd invoiceflow-api
python -m venv .venv

* Activar entorno virtual:
Windows: .venv\Scripts\activate
Linux/macOS: source .venv/bin/activate

### 2. Full Stack Docker Launch
The whole solution (PostgreSQL database, environment parameters, and the FastAPI application) spins up with a single automated command:

docker compose up --build -d

Once initialized, access and test the entire business flow directly through the integrated Swagger UI documentation page:
👉 http://localhost:8000/docs

🧪 Quality Assurance & Automated Tests
To ensure business continuity and verify invoice security rules, run the test suite with:
pytest

---

## ✉️ Contact & Automation Consulting

If your business needs to strengthen its software APIs, transition from legacy workflows to automated backend systems, or requires a engineer who understands financial rules before typing code:

* Developer: José Carlos Lobo
* Specialty: Backend Automation, Secure API Engineering, & Process Optimization (Ex-Banking Professional with 35+ years of corporate business experience).
* LinkedIn: [www.linkedin.com/in/josé-carlos-lobo-473b458a](https://www.linkedin.com/in/josé-carlos-lobo-473b458a)

---
---

<div id="spanish-version"></div>

# Versión en Español: Caso de Estudio de Negocio

## 🎯 ¿Qué es InvoiceFlow? (Perspectiva de Negocio)

En el ámbito de la gestión administrativa y financiera de cualquier empresa, el manejo de facturas internas y datos de facturación exige tres pilares innegociables: seguridad absoluta de acceso, trazabilidad del dato y blindaje de la información (aislamiento). Un error de asignación o una fuga de visibilidad en documentos financieros puede acarrear sanciones regulatorias graves y pérdidas económicas.

InvoiceFlow es una API backend de nivel de producción diseñada específicamente para dar soporte a las operaciones de facturación interna de una organización. A diferencia de las aplicaciones básicas del mercado, este sistema implementa un modelo de aislamiento de datos a nivel de usuario estricto, garantizando que cada gestor o departamento opere de forma aislada, segura y controlada dentro del mismo entorno corporativo.

### 🏢 Impacto y Relevancia en el Negocio:
* Control Financiero Centralizado: Estructura flujos operativos financieros bajo estándares reales de auditoría.
* Segregación de Funciones y Datos: Mitiga el riesgo operativo asegurando que un usuario solo pueda visualizar, crear o modificar los registros de facturación que le pertenecen legítimamente.
* Cumplimiento Normativo (Compliance): Alineado con las mejores prácticas de gobierno del dato y control de acceso exigidos en sectores rigurosos como el financiero.

---

## 🚀 Características Clave y Valor Empresarial

* Seguridad y Control de Accesos Avanzado: Implementa el flujo de contraseñas OAuth2 y generación de tokens securizados JWT, acompañado de hashing de contraseñas en base de datos.
* Aislamiento Estricto de Datos (Data Isolation): Aplicación de lógica per-user que valida la propiedad de cada registro en cada petición. Nadie puede acceder a una factura ajena adivinando o alterando un ID en la API.
* Garantía Operativa mediante Testing Automatizado (pytest): El sistema cuenta con una batería de pruebas automatizadas que validan flujos críticos (registro, emisión de tokens, aislamiento multi-usuario) antes de permitir cualquier despliegue en producción, reduciendo el error humano a cero.
* Despliegue Profesional Contenerizado: Arquitectura 100% lista para la nube gracias a Docker, asegurando que el sistema funcione exactamente igual en desarrollo, pruebas o entornos reales de producción.

---

## ✉️ Contacto y Consultoría de Procesos

* Desarrollador: José Carlos Lobo
* LinkedIn: [www.linkedin.com/in/josé-carlos-lobo-473b458a](https://www.linkedin.com/in/josé-carlos-lobo-473b458a)
