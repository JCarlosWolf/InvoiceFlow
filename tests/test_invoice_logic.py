# tests/test_invoice_logic.py
import pytest
from app.services.invoice_processing import parse_and_validate_invoice

# Casos de prueba rápidos, sin archivos
test_invoices = [
    {"number": "FAC-001", "base": 100, "vat": 0.21, "total": 121, "expected": "validated"},
    {"number": "FAC-002", "base": 100, "vat": 0.21, "total": 130, "expected": "error"},
]

@pytest.mark.parametrize("invoice_data", test_invoices)
def test_parse_invoice(invoice_data):
    data = {
        "provider_cif": "B12345678",
        "provider_name": "ACME SL",
        "invoice_number": invoice_data["number"],
        "base": invoice_data["base"],
        "vat": invoice_data["vat"],
        "total": invoice_data["total"],
    }
    result = parse_and_validate_invoice(data)
    assert result.status == invoice_data["expected"]