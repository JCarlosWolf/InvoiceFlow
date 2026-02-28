import re
import logging
from dataclasses import dataclass
from typing import Dict, Any

import pytesseract


logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Optional Tesseract configuration (Windows)
# ------------------------------------------------------------------

try:
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
except Exception:
    pass


# ------------------------------------------------------------------
# Validation result model
# ------------------------------------------------------------------

@dataclass
class ValidationResult:
    status: str
    message: str


# ------------------------------------------------------------------
# PDF text extraction
# ------------------------------------------------------------------

def extract_from_pdf(file_path: str) -> Dict[str, Any]:
    """
    Extract text from a PDF file and parse invoice fields.
    Returns empty dict if extraction fails.
    """
    try:
        import pdfplumber

        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return extract_fields(text)

    except Exception:
        logger.warning("PDF extraction failed for file: %s", file_path)
        return {}


# ------------------------------------------------------------------
# Image OCR extraction
# ------------------------------------------------------------------

def extract_from_image(file_path: str) -> Dict[str, Any]:
    """
    Extract text from an image using OCR and parse invoice fields.
    Returns empty dict if extraction fails.
    """
    try:
        from PIL import Image

        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

        return extract_fields(text)

    except Exception as e:
        logger.warning("OCR extraction failed: %s", str(e))
        return {}


# ------------------------------------------------------------------
# Field extraction logic
# ------------------------------------------------------------------

def extract_fields(text: str) -> Dict[str, Any]:
    """
    Extract structured invoice data from raw text.
    Supports structured invoices and simplified ticket formats.
    """
    text = text.replace(",", ".")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    data: Dict[str, Any] = {}

    # -------------------------
    # Provider name and CIF
    # -------------------------

    provider_name = None
    provider_cif = None

    for line in lines:
        if line.upper().startswith("CIF"):
            cif_match = re.search(r"[A-Z]-?\d{8}", line)
            if cif_match:
                provider_cif = cif_match.group()

        if line.lower().startswith("proveedor"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                provider_name = parts[1].strip()

    if not provider_name and lines:
        first_line = lines[0]
        cif_match = re.search(r"[A-Z]-?\d{8}", first_line)
        if cif_match:
            provider_cif = cif_match.group()
            provider_name = first_line.replace(provider_cif, "").strip()
        else:
            provider_name = first_line

    data["provider_name"] = provider_name
    data["provider_cif"] = provider_cif

    # -------------------------
    # Invoice number
    # -------------------------

    invoice_match = re.search(
        r"FACTURA.*?:\s*([A-Z0-9\-]+)",
        text,
        re.IGNORECASE
    )

    if invoice_match:
        data["invoice_number"] = invoice_match.group(1)

    # -------------------------
    # Structured base / VAT / total
    # -------------------------

    base_match = re.search(r"Base:\s*(\d+\.?\d*)", text, re.IGNORECASE)
    vat_match = re.search(r"IVA:\s*(\d+\.?\d*)", text, re.IGNORECASE)
    total_match = re.search(r"Total:\s*(\d+\.?\d*)", text, re.IGNORECASE)

    if base_match and vat_match and total_match:
        data["base"] = float(base_match.group(1))
        data["vat"] = float(vat_match.group(1))
        data["total"] = float(total_match.group(1))
        return data

    # -------------------------
    # Ticket-style VAT lines (multiple rates)
    # -------------------------

    base_total = 0.0
    vat_total = 0.0

    iva_pattern = re.findall(
        r"(\d+)%\s+(\d+\.\d{2})\s+(\d+\.\d{2})",
        text
    )

    for percent, base_val, vat_val in iva_pattern:
        base_total += float(base_val)
        vat_total += float(vat_val)

    if base_total > 0:
        data["base"] = round(base_total, 2)
        data["vat"] = round(vat_total, 2)

    # -------------------------
    # Flexible total detection
    # -------------------------

    total_match = re.search(
        r"TOTAL.*?(\d+[\.,]?\d{2})",
        text,
        re.IGNORECASE
    )

    if total_match:
        total_raw = total_match.group(1).replace(",", ".")
        data["total"] = float(total_raw)

    if "total" not in data:
        numbers = re.findall(r"\d+\.\d{2}", text)
        if numbers:
            data["total"] = float(max(numbers))

    return data


# ------------------------------------------------------------------
# Mathematical validation
# ------------------------------------------------------------------

def parse_and_validate_invoice(data: Dict[str, Any]) -> ValidationResult:
    """
    Validate invoice totals against different VAT formats:
    - Direct VAT amount
    - Percentage (21)
    - Decimal (0.21)
    - Multiplier (1.21)
    """

    base = data.get("base")
    vat_raw = data.get("vat")
    total = data.get("total")

    if base is None or vat_raw is None or total is None:
        return ValidationResult("error", "Missing financial fields")

    base = float(base)
    vat_raw = float(vat_raw)
    total = float(total)

    # Case 1: direct VAT amount
    if round(base + vat_raw, 2) == round(total, 2):
        return ValidationResult("validated", "Direct VAT amount")

    # Case 2: percentage integer (21)
    if round(base * (1 + vat_raw / 100), 2) == round(total, 2):
        return ValidationResult("validated", "Percentage VAT")

    # Case 3: decimal (0.21)
    if round(base * (1 + vat_raw), 2) == round(total, 2):
        return ValidationResult("validated", "Decimal VAT")

    # Case 4: multiplier (1.21)
    if vat_raw > 1 and round(base * vat_raw, 2) == round(total, 2):
        return ValidationResult("validated", "Multiplier VAT")

    return ValidationResult("error", "Mathematical validation failed")