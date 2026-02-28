def test_users_are_isolated(client):
    from tests.conftest import create_user_and_get_token

    # Usuario A
    token_a = create_user_and_get_token(client, "a@test.com")
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Usuario B
    token_b = create_user_and_get_token(client, "b@test.com")
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Usuario A consulta facturas
    response_a = client.get("/api/invoiceFlow/invoices", headers=headers_a)
    assert response_a.status_code == 200
    assert response_a.json() == []

    # Usuario B consulta facturas
    response_b = client.get("/api/invoiceFlow/invoices", headers=headers_b)
    assert response_b.status_code == 200
    assert response_b.json() == []