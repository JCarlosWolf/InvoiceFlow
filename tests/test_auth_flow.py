def test_register_and_login(client):
    # Register
    response = client.post("/api/auth/register", json={
        "email": "user1@test.com",
        "password": "123456"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()

    # Login
    response = client.post(
        "/api/auth/login",
        data={
            "username": "user1@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()