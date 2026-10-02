# 🌟 Week 8 — Personal Blog with Flask

A modular personal blog web application built with Flask, Jinja2, Flask-SQLAlchemy, Flask-Login, Flask-WTF, SQLite, and Bootstrap.

## Project Scope

The application implements the core Week 8 requirements:

- Flask project structure
- Jinja2 templates
- SQLite database
- Registration, login, and logout
- Password hashing
- User profiles
- Blog post CRUD
- Search and pagination
- Comments and moderation
- Static CSS and JavaScript
- Responsive Bootstrap interface
- Form validation and CSRF protection
- Error handling
- Automated tests

Optional extensions included in this project are post categories/tags and image uploads.

Out of scope for this version: social sharing, RSS, newsletter/contact workflows, cloud deployment, and rich-text editor integration.

## Assumptions

1. This is an educational/local application rather than a production deployment.
2. SQLite is used as the required local database.
3. The first registered account becomes the demo administrator so moderation can be demonstrated immediately.
4. Comments from non-admin users require administrator approval.
5. Uploaded images are limited to common image formats and 2 MB.
6. Database tables are created automatically with SQLAlchemy for simple local setup.
7. The migrations folder is included for future database migration work.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite
- Jinja2
- Bootstrap 5
- HTML/CSS/JavaScript
- Pytest

## Structure

```text
week8-flask-blog/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── auth/
│   ├── main/
│   ├── posts/
│   ├── comments/
│   └── static/
├── templates/
│   ├── base.html
│   ├── auth/
│   ├── main/
│   ├── posts/
│   └── errors/
├── migrations/
├── tests/
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── run.py
└── README.md
```

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Open the local Flask address shown in the terminal.

## Main User Flow

1. Register an account.
2. Log in.
3. The first registered account becomes the demo administrator.
4. Create a blog post.
5. View, edit, or delete your own post.
6. Search and paginate through published posts.
7. Register another account and add a comment.
8. Approve pending comments using the administrator account.
9. Update the user profile.

## Database Design

### User
Stores username, email, password hash, profile information, membership date, and administrator status.

### Post
Stores title, content, category, tags, optional image filename, timestamps, published status, and author ID.

### Comment
Stores comment content, timestamp, approval status, user ID, and post ID.

Relationships:

```text
User
 ├── Posts
 └── Comments

Post
 └── Comments

Comment
 ├── User
 └── Post
```

## Authentication

Passwords are stored as secure hashes using Werkzeug. Flask-Login manages authenticated sessions and protected routes.

## CRUD

Authenticated users can create, read, update, and delete their own posts. Administrators can manage posts as well.

## Search and Pagination

The home page searches titles, content, categories, and tags. Published posts are displayed five per page.

## Comment Moderation

Non-admin comments are stored as pending. The administrator can approve them. Users can delete their own comments, while administrators can delete any comment.

## Security and Validation

The project includes:

- Password hashing
- CSRF protection
- Login-required routes
- Post ownership checks
- Admin authorization checks
- WTForms validation
- Image extension validation
- Upload size limit
- `.env` excluded from Git

## Testing

Run:

```powershell
python -m pytest -v
```

The tests cover registration, password hashing, login validation, post creation, editing, deletion, comment authentication, and comment creation.

## Code Quality

The project uses separate modules for authentication, routing, posts, comments, models, templates, static files, and tests. Functions and variables use descriptive names to improve readability and maintainability.

## Learning Outcome

This project provides practical experience with Flask routing, Jinja2 templates, forms, authentication, SQLAlchemy models, SQLite, CRUD operations, comments, Bootstrap, validation, and automated testing.
