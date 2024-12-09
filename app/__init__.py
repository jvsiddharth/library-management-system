from flask import Flask
from typing import Optional

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.books import books_bp
    from app.routes.members import members_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(members_bp, url_prefix='/members')

    return app
