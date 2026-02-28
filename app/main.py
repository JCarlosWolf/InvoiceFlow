from fastapi import FastAPI
from app.api.invoice_router import router as invoice_router
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status
from app.api.auth_router import router as auth_router

app = FastAPI(title="InvoiceFlow API")

app.include_router(auth_router)
app.include_router(invoice_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )