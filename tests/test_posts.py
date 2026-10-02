from app import db
from app.models import Post

def register_and_login(client):
    client.post("/auth/register", data={
        "username": "writer", "email": "writer@example.com",
        "password": "secret123", "password_confirm": "secret123"
    })
    client.post("/auth/login", data={"username": "writer", "password": "secret123"})

def test_post_crud_flow(client, app):
    register_and_login(client)
    response = client.post("/posts/new", data={
        "title": "My Flask Post", "category": "Flask",
        "tags": "python, flask",
        "content": "This is a sufficiently long blog post for testing.",
        "published": "y"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"My Flask Post" in response.data

    with app.app_context():
        post = db.session.scalar(db.select(Post).where(Post.title == "My Flask Post"))
        post_id = post.id

    response = client.post(f"/posts/{post_id}/edit", data={
        "title": "Updated Flask Post", "category": "Web",
        "tags": "flask", "content": "Updated content with enough characters.",
        "published": "y"
    }, follow_redirects=True)
    assert b"Updated Flask Post" in response.data

    response = client.post(f"/posts/{post_id}/delete", follow_redirects=True)
    assert b"Updated Flask Post" not in response.data

    with app.app_context():
        assert db.session.get(Post, post_id) is None
