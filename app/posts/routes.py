from pathlib import Path
from uuid import uuid4
from flask import abort, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.posts import bp
from app.posts.forms import PostForm

def save_image(uploaded_file):
    if not uploaded_file or not uploaded_file.filename:
        return None
    extension = Path(uploaded_file.filename).suffix.lower().lstrip(".")
    filename = f"{uuid4().hex}.{extension}"
    uploaded_file.save(Path(current_app.config["UPLOAD_FOLDER"]) / filename)
    return filename

def user_can_manage(post):
    return current_user.is_authenticated and (
        post.user_id == current_user.id or current_user.is_admin
    )

@bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data.strip(),
            category=form.category.data.strip(),
            tags=(form.tags.data or "").strip(),
            content=form.content.data.strip(),
            published=form.published.data,
            author=current_user,
        )
        image_filename = save_image(form.image.data)
        if image_filename:
            post.image_filename = image_filename
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully.", "success")
        return redirect(url_for("posts.detail", post_id=post.id))
    return render_template("posts/form.html", form=form, page_title="New Post")

@bp.route("/<int:post_id>")
def detail(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        abort(404)
    if not post.published and (
        not current_user.is_authenticated or not user_can_manage(post)
    ):
        abort(404)
    approved_comments = [
        comment for comment in post.comments
        if comment.approved or (
            current_user.is_authenticated and comment.user_id == current_user.id
        )
    ]
    return render_template(
        "posts/detail.html", post=post, approved_comments=approved_comments
    )

@bp.route("/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        abort(404)
    if not user_can_manage(post):
        abort(403)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.category = form.category.data.strip()
        post.tags = form.tags.data.strip()
        post.content = form.content.data.strip()
        post.published = form.published.data
        image_filename = save_image(form.image.data)
        if image_filename:
            post.image_filename = image_filename
        db.session.commit()
        flash("Post updated successfully.", "success")
        return redirect(url_for("posts.detail", post_id=post.id))
    return render_template("posts/form.html", form=form, page_title="Edit Post")

@bp.route("/<int:post_id>/delete", methods=["POST"])
@login_required
def delete(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        abort(404)
    if not user_can_manage(post):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "success")
    return redirect(url_for("main.index"))
