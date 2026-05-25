# InvoiceFlow API: Sistema Backend para la Gestión, Control Operativo y Aislamiento de Facturación Interna

**Desarrollado por:** José Carlos Lobo  
**Stack Principal:** Python | FastAPI | PostgreSQL | Docker | Pytest (Automated Testing)  

---

## 🎯 ¿Qué es InvoiceFlow? (Perspectiva de Negocio)

En el ámbito de la gestión administrativa y financiera de cualquier empresa, el manejo de facturas internas y datos de facturación exige tres pilares innegociables: **seguridad absoluta de acceso, trazabilidad del dato y blindaje de la información (aislamiento)**. Un error de asignación o una fuga de visibilidad en documentos financieros puede acarrear sanciones regulatorias graves y pérdidas económicas.

**InvoiceFlow** es una API backend de nivel de producción diseñada específicamente para dar soporte a las operaciones de facturación interna de una organización. A diferencia de las aplicaciones básicas del mercado, este sistema implementa un modelo de **aislamiento de datos a nivel de usuario estricto**, garantizando que cada gestor o departamento opere de forma aislada, segura y controlada dentro del mismo entorno corporativo.

### 🏢 Impacto y Relevancia en el Negocio:
* **Control Financiero Centralizado:** Estructura flujos operativos financieros bajo estándares reales de auditoría.
* **Segregación de Funciones y Datos:** Mitiga el riesgo operativo asegurando que un usuario solo pueda visualizar, crear o modificar los registros de facturación que le pertenecen legítimamente.
* **Cumplimiento Normativo (Compliance):** Alineado con las mejores prácticas de gobierno del dato y control de acceso exigidos en sectores rigurosos como el financiero.

---

## 🚀 Características Clave y Valor Empresarial

* **Seguridad y Control de Accesos Avanzado:** Implementa el flujo de contraseñas OAuth2 y generación de tokens securizados JWT, acompañado de hashing de contraseñas en base de datos.
* **Aislamiento Estricto de Datos (Data Isolation):** Aplicación de lógica per-user que valida la propiedad de cada registro en cada petición. Nadie puede acceder a una factura ajena adivinando o alterando un ID en la API.
* **Garantía Operativa mediante Testing Automatizado (`pytest`):** El sistema cuenta con una batería de pruebas automatizadas que validan flujos críticos (registro, emisión de tokens, aislamiento multi-usuario) antes de permitir cualquier despliegue en producción, reduciendo el error humano a cero.
* **Despliegue Profesional Contenerizado:** Arquitectura 100% lista para la nube gracias a **Docker**, asegurando que el sistema funcione exactamente igual en desarrollo, pruebas o entornos reales de producción.

---

## 🛠️ Arquitectura Técnica y Buenas Prácticas

Diseñado bajo principios de ingeniería de software empresarial que garantizan mantenibilidad y escalabilidad a largo plazo:

* **Separación de Responsabilidades (Separation of Concerns):** Estructura limpia y modular que independiza las rutas de comunicación del núcleo de la lógica de negocio.
* **Capa de Abstracción de Servicios (Service Layer):** Toda la lógica financiera y validaciones críticas residen en servicios dedicados, aislados de los puntos de entrada de la API.
* **Persistencia Robusta:** Conexión y gestión de sesiones optimizada con **PostgreSQL** y control evolutivo de tablas mediante migraciones con **Alembic**.

app/
├── api/        # Definición de Endpoints y rutas protegidas
├── core/       # Seguridad, hashing y configuración global (.env)
├── models/     # Modelos de datos relacionales (SQLAlchemy ORM)
├── schemas/    # Validaciones y contratos de datos entrantes/salientes (Pydantic)
├── services/   # Capa de lógica de negocio (Validaciones financieras)
└── database.py # Motor de base de datos y gestión del ciclo de vida de sesiones


---

## 📋 Guía de Instalación y Despliegue Local

### Requisitos Previos
* Python 3.10+
* Docker y Docker Compose instalado

### 1. Clonar el Proyecto y Preparar Entorno
```bash
git clone [https://github.com/JCarlosWolf/invoiceflow-api.git](https://github.com/JCarlosWolf/invoiceflow-api.git)
cd invoiceflow-api
python -m venv .venv
Activar entorno virtual:

Windows: .venv\Scripts\activate

Linux/macOS: source .venv/bin/activate

2. Despliegue Automatizado con Docker
El sistema está configurado para levantarse por completo (Base de datos PostgreSQL, configuración de variables de entorno y servidor FastAPI) con un único comando:

Bash
docker compose up --build -d
Una vez levantado, puedes acceder a la documentación interactiva e integrada del sistema (Swagger UI) para probar los flujos de negocio en:

👉 http://localhost:8000/docs

🧪 Validación y Calidad de Software (Automated Tests)
Para asegurar la continuidad del negocio y evitar fallos críticos en la gestión de facturas, ejecuta la suite de pruebas automatizadas con el siguiente comando:

Bash
pytest
Las pruebas validan de forma automatizada: flujos de registro, denegación de accesos no autorizados, flujos de creación de facturas e intentos de violación de aislamiento de datos entre múltiples usuarios.

✉️ Contacto y Consultoría de Procesos
Si tu organización necesita robustecer sus APIs de negocio, migrar procesos manuales a flujos automatizados seguros o necesita un desarrollador que entienda las reglas financieras antes de picar el código:

Desarrollador: José Carlos Lobo

Especialidad: Automatización Backend, Optimización de Procesos Operativos e Integraciones Seguras (Ex-Banca con más de 35 años de trayectoria de negocio).

LinkedIn: www.linkedin.com/in/josé-carlos-lobo-473b458a

Production-ready backend API designed to support secure internal invoicing operations within an enterprise environment.
