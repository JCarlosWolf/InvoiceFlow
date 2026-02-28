import io
import pytest
from unittest.mock import patch

from tests.conftest import create_user_and_get_token


@pytest.mark.parametrize(
    "file_type, filename, content_type",
    [
        ("pdf", "invoice1.pdf", "application/pdf"),
        ("pdf", "invoice2.pdf", "application/pdf"),
        ("image", "invoice1.jpg", "image/jpeg"),
        ("image", "invoice2.jpg", "image/jpeg"),
    ]
)
@patch("app.api.invoice_router.parse_and_validate_invoice")
@patch("app.api.invoice_router.extract_from_pdf")
@patch("app.api.invoice_router.extract_from_image")
def test_upload_file_mock(
    mock_extract_image,
    mock_extract_pdf,
    mock_parse,
    client,
    file_type,
    filename,
    content_type
):
    """
    Test de subida de archivos simulando:
    - Extracción PDF / OCR
    - Validación matemática
    - Flujo completo protegido con JWT
    """

    # 1️⃣ Crear usuario y obtener token
    token = create_user_and_get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # 2️⃣ Simular datos extraídos del documento
    mock_data = {
        "provider_name": "ACME SL",
        "provider_cif": "B12345678",
        "invoice_number": "FAC-001",
        "base": 100.0,
        "vat": 0.21,
        "total": 121.0,
    }

    if file_type == "pdf":
        mock_extract_pdf.return_value = mock_data
    else:
        mock_extract_image.return_value = mock_data

    # 3️⃣ Simular resultado de validación
    class MockValidation:
        def __init__(self, status):
            self.status = status
            self.message = "mocked"

    if "1" in filename:
        mock_parse.return_value = MockValidation("validated")
    elif "2" in filename:
        mock_parse.return_value = MockValidation("error")
    else:
        mock_parse.return_value = MockValidation("duplicate")

    # 4️⃣ Crear archivo dummy
    file_content = io.BytesIO(b"dummy data")

    # 5️⃣ Llamar endpoint protegido
    response = client.post(
        "/api/invoiceFlow/upload",
        headers=headers,
        files={"file": (filename, file_content, content_type)},
    )

    # 6️⃣ Verificaciones
    if "1" in filename:
        assert response.status_code == 200
        assert response.json()["status"] == "validated"

    elif "2" in filename:
        # Factura inválida debe devolver 400
        assert response.status_code == 400

    else:
        # Duplicado u otro caso
        assert response.status_code in (200, 400)