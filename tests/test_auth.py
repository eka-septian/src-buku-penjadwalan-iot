def test_login_page(client):
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"username" in response.data
    assert b"password" in response.data


def test_valid_login_logout(client, init_db):
    response = client.post(
        "/auth/login",
        data={"username": "defTestUser", "password": "userTest1"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Welcome Back!" in response.data
    assert b"Smarthome Home" in response.data

    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Goodbye!" in response.data


def test_invalid_login(client, init_db):
    response = client.post(
        "/auth/login",
        data={"username": "randomUser", "password": "random"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Incorrect credentials" in response.data
    assert b"Login" in response.data
    assert b"username" in response.data
    assert b"password" in response.data


def test_login_when_already_logged_in(client, init_db, log_in_default_user):
    response = client.post(
        "/auth/login",
        data={"username": "defTestUser", "password": "userTest1"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Already logged in" in response.data
    assert b"Smarthome Home" in response.data


def test_register_page(client):
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"username" in response.data
    assert b"password" in response.data
    assert b"confirm" in response.data


def test_valid_registration(client):
    response = client.post(
        "/auth/register",
        data={
            "username": "HumanNoid",
            "password": "HumanIsGood",
            "confirm": "HumanIsGood",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Welcome HumanNoid!" in response.data


def test_invalid_registration(client, init_db):
    response = client.post(
        "/auth/register",
        data={"username": "fa", "password": "fail", "confirm": " "},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Field must be" in response.data
    assert b"New user" not in response.data


def test_duplicate_user_registration(client):
    client.post(
        "/auth/register",
        data={"username": "newuser", "password": "newuser", "confirm": "newuser"},
        follow_redirects=True,
    )
    client.get("/auth/logout")

    response = client.post(
        "/auth/register",
        data={"username": "newuser", "password": "newuser", "confirm": "newuser"},
        follow_redirects=True,
    )
    assert b"username already exists" in response.data
    assert b"Welcome" not in response.data


def test_register_when_already_logged_in(client, init_db, log_in_default_user):
    response = client.post(
        "/auth/register",
        data={"username": "someuser", "password": "password", "confirm": "password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Already logged in" in response.data
    assert b"New user (someuser) created!" not in response.data
