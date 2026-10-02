from app import db
from app.models import Comment, Post

def test_comment_requires_login(client):
    response = client.post("/comments/post/1", data={"content": "Hello"})
    assert response.status_code in (302, 401)

def test_comment_creation(client, app):
    client.post("/auth/register", data={
        "username": "commenter", "email": "commenter@example.com",
        "password": "secret123", "password_confirm": "secret123"
    })
    client.post("/auth/login", data={"username": "commenter", "password": "secret123"})
    client.post("/posts/new", data={
        "title": "Comment Test", "category": "Testing",
        "content": "A test post with enough content.", "published": "y"
    })

    with app.app_context():
        post = db.session.scalar(db.select(Post).where(Post.title == "Comment Test"))
        post_id = post.id

    response = client.post(
        f"/comments/post/{post_id}",
        data={"content": "Useful post!"},
        follow_redirects=True
    )
    assert response.status_code == 200
    with app.app_context():
        comment = db.session.scalar(db.select(Comment).where(Comment.content == "Useful post!"))
        assert comment is not None
        assert comment.approved is True
