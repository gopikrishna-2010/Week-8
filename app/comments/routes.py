from flask import abort, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.comments import bp
from app.comments.forms import CommentForm
from app.models import Comment, Post

@bp.route("/post/<int:post_id>", methods=["POST"])
@login_required
def create(post_id):
    post = db.session.get(Post, post_id)
    if post is None or not post.published:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data.strip(),
            author=current_user,
            post=post,
            approved=current_user.is_admin,
        )
        db.session.add(comment)
        db.session.commit()
        flash(
            "Comment added and approved." if current_user.is_admin
            else "Comment submitted and is awaiting approval.",
            "success",
        )
    else:
        flash("Please enter a valid comment.", "danger")
    return redirect(url_for("posts.detail", post_id=post.id))

@bp.route("/<int:comment_id>/approve", methods=["POST"])
@login_required
def approve(comment_id):
    if not current_user.is_admin:
        abort(403)
    comment = db.session.get(Comment, comment_id)
    if comment is None:
        abort(404)
    comment.approved = True
    db.session.commit()
    flash("Comment approved.", "success")
    return redirect(url_for("posts.detail", post_id=comment.post_id))

@bp.route("/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete(comment_id):
    comment = db.session.get(Comment, comment_id)
    if comment is None:
        abort(404)
    if not current_user.is_admin and comment.user_id != current_user.id:
        abort(403)
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted.", "success")
    return redirect(url_for("posts.detail", post_id=post_id))
