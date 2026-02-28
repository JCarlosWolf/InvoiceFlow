# models/provider.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import  Base

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    cif = Column(String(20), unique=True, nullable=False)

    # <-- RELACIÓN HACIA FACTURAS
    invoices = relationship("Invoice", back_populates="provider")