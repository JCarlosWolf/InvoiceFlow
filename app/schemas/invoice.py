from pydantic import BaseModel
from app.models.enums import InvoiceStatusEnum

class InvoiceSchema(BaseModel):
    invoice_number: str
    status: InvoiceStatusEnum

    model_config = {"from_attributes": True}