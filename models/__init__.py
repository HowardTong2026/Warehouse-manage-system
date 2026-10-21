"""
SQLAlchemy database instance and initialization helper.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Initialize SQLAlchemy with Flask app."""
    db.init_app(app)
    return db