InvoiceFlow – API de Gestión y Validación de Facturas

InvoiceFlow es una API REST desarrollada con FastAPI orientada a la gestión y validación automática de facturas.

El proyecto simula un entorno real de validación documental, aplicando reglas de negocio para comprobar coherencia entre base imponible, IVA y total, así como gestión de estados de factura.

🚀 Tecnologías utilizadas

Python

FastAPI

Pydantic

SQL

Pytest

OpenAPI / Swagger

📌 Funcionalidades principales

Creación y gestión de facturas mediante API REST

Validación automática de cálculos (base imponible, IVA y total)

Control de estados: validada / error

Subida y gestión de archivos PDF

Arquitectura modular por capas

Documentación automática con Swagger

🏗 Arquitectura

El proyecto sigue una estructura modular separando:

Modelos

Esquemas

Lógica de negocio

Endpoints

Base de datos

Facilitando mantenibilidad y escalabilidad.

📂 Instalación

Clonar repositorio:

git clone https://github.com/JCarlosWolf/InvoiceFlow.git

Crear entorno virtual:

python -m venv venv

Instalar dependencias:

pip install -r requirements.txt

Ejecutar servidor:

uvicorn main:app --reload

Acceder a documentación:

http://127.0.0.1:8000/docs
🎯 Objetivo del proyecto

Demostrar capacidades en:

Desarrollo backend con FastAPI

Implementación de lógica de negocio

Validación de datos

Diseño de APIs REST

Organización modular de código

📌 Autor

José Carlos Lobo Arroyo
Backend Developer | Python | FastAPI
