from app import db
from app.models import User

def register(client, username="alice", email="alice@example.com", password="secret123"):
    return client.post("/auth/register", data={
        "username": username, "email": email,
        "password": password, "password_confirm": password
    }, follow_redirects=True)

def login(client, username="alice", password="secret123"):
    return client.post("/auth/login", data={
        "username": username, "password": password
    }, follow_redirects=True)

def test_registration_and_login(client, app):
    response = register(client)
    assert response.status_code == 200
    with app.app_context():
        user = db.session.scalar(db.select(User).where(User.username == "alice"))
        assert user is not None
        assert user.check_password("secret123")
        assert user.is_admin is True
    response = login(client)
    assert b"Welcome back" in response.data

def test_invalid_login(client):
    register(client)
    response = login(client, password="wrongpass")
    assert b"Invalid username or password" in response.data
