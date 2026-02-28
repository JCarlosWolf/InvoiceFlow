from pydantic import BaseModel
from app.models.enums import InvoiceStatusEnum


class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    base: float
    vat: float
    total: float
    status: InvoiceStatusEnum
    provider_name: str
    file_name: str

    model_config = {"from_attributes": True}