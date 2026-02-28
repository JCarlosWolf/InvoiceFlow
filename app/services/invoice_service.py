from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.invoice import Invoice
from app.models.enums import InvoiceStatusEnum


# =========================================================
# Detectar factura duplicada (por usuario)
# =========================================================

def check_duplicate(
    db: Session,
    provider_id: int,
    invoice_number: str,
    user_id: int,
) -> bool:
    """
    Verifica si ya existe una factura con el mismo
    provider_id + invoice_number + user_id.
    """
    existing = db.query(Invoice).filter(
        Invoice.provider_id == provider_id,
        Invoice.invoice_number == invoice_number,
        Invoice.user_id == user_id,
    ).first()

    return existing is not None


# =========================================================
# Guardar factura
# =========================================================

def save_invoice(
    db: Session,
    provider_id: int,
    invoice_number: str,
    base,
    vat,
    total,
    status: InvoiceStatusEnum,
    file_name: str,
    user_id: int,
) -> Invoice:
    """
    Guarda una factura asociada a un usuario.
    Si falla el commit, realiza rollback.
    """

    try:
        invoice = Invoice(
            provider_id=provider_id,
            invoice_number=invoice_number,
            base=base,
            vat=vat,
            total=total,
            status=status,
            file_name=file_name,
            user_id=user_id,
        )

        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        return invoice

    except SQLAlchemyError:
        db.rollback()
        raise


# =========================================================
# Listar facturas por usuario
# =========================================================

def list_invoices(db: Session, user_id: int):
    """
    Devuelve todas las facturas del usuario actual,
    ordenadas por ID descendente.
    """
    return (
        db.query(Invoice)
        .filter(Invoice.user_id == user_id)
        .order_by(Invoice.id.desc())
        .all()
    )