import os
import uuid
import shutil
import logging

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.enums import InvoiceStatusEnum
from app.models.user import User
from app.core.dependencies import get_current_user

from app.services.invoice_processing import (
    extract_from_pdf,
    extract_from_image,
    parse_and_validate_invoice,
)

from app.services.invoice_service import (
    save_invoice,
    check_duplicate,
    list_invoices,
)

from app.services.provider_service import (
    get_or_create_provider,
    list_providers,
)

logger = logging.getLogger("invoiceflow")

router = APIRouter(
    prefix="/api/invoiceFlow",
    tags=["InvoiceFlow"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


# ------------------------------------------------------------------
# File validation helpers
# ------------------------------------------------------------------

def validate_file(file: UploadFile) -> str:
    """
    Validate file extension and size.
    Raises HTTPException if invalid.
    """
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    return ext


def save_file(file: UploadFile, ext: str) -> str:
    """
    Save uploaded file with a unique name.
    Returns file path.
    """
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


def extract_data(file_path: str, ext: str):
    """
    Extract structured invoice data depending on file type.
    """
    if ext == ".pdf":
        return extract_from_pdf(file_path)
    return extract_from_image(file_path)


# ------------------------------------------------------------------
# Upload endpoint
# ------------------------------------------------------------------

@router.post("/upload")
def upload_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload and process an invoice file.
    Validates structure, VAT consistency and duplicate detection.
    """

    file_path = None

    try:
        # Validate file
        ext = validate_file(file)

        # Save file to disk
        file_path = save_file(file, ext)

        # Extract data from document
        extracted_data = extract_data(file_path, ext)

        if not extracted_data:
            raise HTTPException(
                status_code=400,
                detail="Unable to extract invoice data",
            )

        # Mathematical validation
        result = parse_and_validate_invoice(extracted_data)

        if result.status == "error":
            raise HTTPException(status_code=400, detail="Invalid invoice")

        provider_name = extracted_data.get("provider_name", "").strip()
        provider_cif = extracted_data.get("provider_cif")
        invoice_number = extracted_data.get("invoice_number", "").strip().upper()
        base = extracted_data.get("base")
        vat = extracted_data.get("vat")
        total = extracted_data.get("total")

        if not provider_name or not invoice_number:
            raise HTTPException(
                status_code=400,
                detail="Missing provider or invoice number",
            )

        # Prevent CIF collision when missing
        if not provider_cif:
            provider_cif = f"NO-CIF-{uuid.uuid4()}"

        # Create or retrieve provider
        provider = get_or_create_provider(
            db=db,
            name=provider_name,
            cif=provider_cif,
        )

        # Logical duplicate check
        if check_duplicate(db, provider.id, invoice_number, current_user.id):
            raise HTTPException(status_code=400, detail="Invoice already exists")

        # Persist invoice
        try:
            invoice = save_invoice(
                db=db,
                provider_id=provider.id,
                invoice_number=invoice_number,
                base=base,
                vat=vat,
                total=total,
                status=InvoiceStatusEnum(result.status),
                file_name=os.path.basename(file_path),
                user_id=current_user.id,
            )

        except IntegrityError:
            db.rollback()
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=400, detail="Invoice already exists")

        except Exception:
            db.rollback()
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail="Internal error")

        logger.info(
            "Invoice processed | user=%s | provider=%s | invoice=%s | status=%s",
            current_user.email,
            provider_name,
            invoice_number,
            result.status,
        )

        return {
            "message": "Invoice processed successfully",
            "invoice_id": invoice.id,
            "provider": provider.name,
            "total": float(total),
            "status": result.status,
        }

    except HTTPException:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        raise

    except Exception:
        logger.exception("Unexpected error during upload")
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail="Internal server error")


# ------------------------------------------------------------------
# Read endpoints
# ------------------------------------------------------------------

@router.get("/invoices")
def get_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve invoices belonging to the authenticated user.
    """
    return list_invoices(db, current_user.id)


@router.get("/providers")
def get_providers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve provider list.
    """
    return list_providers(db)


@router.get("/health")
def health():
    """
    Basic health check endpoint.
    """
    return {"status": "ok"}