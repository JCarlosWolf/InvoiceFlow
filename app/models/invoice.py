from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Enum,
    ForeignKey,
    UniqueConstraint,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.models.enums import InvoiceStatusEnum


class Invoice(Base):
    __tablename__ = "invoices"

    __table_args__ = (
        UniqueConstraint(
            "provider_id",
            "invoice_number",
            "user_id",
            name="uq_provider_invoice_user"
        ),
    )

    # =========================
    # Primary Key
    # =========================
    id = Column(Integer, primary_key=True, index=True)

    # =========================
    # File Info
    # =========================
    file_name = Column(String(255), nullable=True, index=True)

    # =========================
    # Invoice Data
    # =========================
    invoice_number = Column(String(50), nullable=False, index=True)

    base = Column(Numeric(10, 2), nullable=False)
    vat = Column(Numeric(5, 4), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    status = Column(
        Enum(InvoiceStatusEnum),
        nullable=False,
        default=InvoiceStatusEnum.validated
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # =========================
    # Provider Relationship
    # =========================
    provider_id = Column(
        Integer,
        ForeignKey("providers.id"),
        nullable=False
    )

    provider = relationship(
        "Provider",
        back_populates="invoices"
    )

    # =========================
    # User Relationship
    # =========================
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="invoices"
    )

    # =========================
    # Computed Properties
    # =========================
    @property
    def provider_name(self):
        return self.provider.name if self.provider else None