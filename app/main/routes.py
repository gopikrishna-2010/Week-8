from flask import render_template, request
from sqlalchemy import or_
from app.main import bp
from app.main.forms import SearchForm
from app.models import Post

@bp.route("/")
@bp.route("/index")
def index():
    page_number = request.args.get("page", 1, type=int)
    search_query = request.args.get("q", "").strip()
    posts_query = Post.query.filter_by(published=True)

    if search_query:
        pattern = f"%{search_query}%"
        posts_query = posts_query.filter(
            or_(
                Post.title.ilike(pattern),
                Post.content.ilike(pattern),
                Post.category.ilike(pattern),
                Post.tags.ilike(pattern),
            )
        )

    posts_page = posts_query.order_by(Post.timestamp.desc()).paginate(
        page=page_number, per_page=5, error_out=False
    )
    form = SearchForm()
    form.query.data = search_query
    return render_template(
        "main/index.html",
        posts_page=posts_page,
        search_form=form,
        search_query=search_query,
    )
