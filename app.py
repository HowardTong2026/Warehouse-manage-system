"""
Flask application factory.
Initializes extensions, registers blueprints, and configures CLI commands.
"""
import os
from flask import Flask
from flask_migrate import Migrate
from config import config
from models import db, init_db

# Import models to register them with SQLAlchemy
from models import (
    category, supplier, product, product_supplier,
    location, stock_item, salesperson, stock_movement
)

migrate = Migrate()


def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    init_db(app)
    migrate.init_app(app, db)

    # Register blueprints
    from routes import (
        products_bp, categories_bp, suppliers_bp, locations_bp,
        stock_bp, alerts_bp, salespeople_bp, reports_bp, dashboard_bp
    )

    app.register_blueprint(products_bp, url_prefix="/api")
    app.register_blueprint(categories_bp, url_prefix="/api")
    app.register_blueprint(suppliers_bp, url_prefix="/api")
    app.register_blueprint(locations_bp, url_prefix="/api")
    app.register_blueprint(stock_bp, url_prefix="/api")
    app.register_blueprint(alerts_bp, url_prefix="/api")
    app.register_blueprint(salespeople_bp, url_prefix="/api")
    app.register_blueprint(reports_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")

    # Register CLI commands
    from seeds.cli import register_seed_commands
    register_seed_commands(app)

    # Health check
    @app.route("/api/health")
    def health():
        return {"status": "ok", "service": "inventory-api"}

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return {"error": "NOT_FOUND", "message": "Resource not found"}, 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return {"error": "SERVER_ERROR", "message": "Internal server error"}, 500

    @app.errorhandler(400)
    def bad_request(e):
        return {"error": "BAD_REQUEST", "message": str(e)}, 400

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)