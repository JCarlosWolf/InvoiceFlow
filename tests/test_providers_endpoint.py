def test_get_providers(client):
    from tests.conftest import create_user_and_get_token

    token = create_user_and_get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/invoiceFlow/providers", headers=headers)
    assert response.status_code == 200