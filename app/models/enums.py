# app/models/enums.py
from enum import Enum

class InvoiceStatusEnum(str, Enum):
    validated = "validated"
    error = "error"
    duplicate = "duplicate"