def test_invoices_requires_auth(client):
    response = client.get("/api/invoiceFlow/invoices")
    assert response.status_code == 401