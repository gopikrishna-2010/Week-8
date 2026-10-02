from pathlib import Path

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config


# Database
db = SQLAlchemy()

# CSRF protection
csrf = CSRFProtect()

# Login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."


def create_app(config_class=Config):
    # Project root directory
    project_root = Path(__file__).resolve().parent.parent

    # Templates are stored outside the app package
    template_path = project_root / "templates"

    # Create Flask application
    app = Flask(
        __name__,
        template_folder=str(template_path)
    )

    # Load configuration
    app.config.from_object(config_class)

    # Create required directories
    Path(app.config["UPLOAD_FOLDER"]).mkdir(
        parents=True,
        exist_ok=True
    )

    Path(app.instance_path).mkdir(
        parents=True,
        exist_ok=True
    )

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Import blueprints
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    from app.posts import bp as posts_bp
    from app.comments import bp as comments_bp

    # Register blueprints
    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    app.register_blueprint(main_bp)

    app.register_blueprint(
        posts_bp,
        url_prefix="/posts"
    )

    app.register_blueprint(
        comments_bp,
        url_prefix="/comments"
    )

    # 404 error handler
    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    # 500 error handler
    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    # Create database tables
    with app.app_context():
        db.create_all()

    return app