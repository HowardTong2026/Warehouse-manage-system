"""
CLI commands for seeding demo data.
"""
import click
from flask import current_app
from seeds.demo_data import create_demo_data


def register_seed_commands(app):
    """Register seed commands with Flask CLI."""

    @app.cli.command("seed-demo")
    @click.option("--password", default="demo123", help="Password for demo accounts")
    def seed_demo(password):
        """Create demo data for teaching purposes."""
        with current_app.app_context():
            create_demo_data(password=password)
            click.echo("✅ Demo data created successfully!")

    @app.cli.command("seed-clear")
    def seed_clear():
        """Clear all demo data (use with caution)."""
        if click.confirm("This will delete ALL data. Continue?"):
            from models import db
            from models import (
                stock_movement, stock_item, product_supplier, product,
                location, category, supplier, salesperson
            )
            with current_app.app_context():
                # Delete in reverse dependency order
                StockMovement = stock_movement.StockMovement
                StockItem = stock_item.StockItem
                ProductSupplier = product_supplier.ProductSupplier
                Product = product.Product
                Location = location.Location
                Category = category.Category
                Supplier = supplier.Supplier
                Salesperson = salesperson.Salesperson

                StockMovement.query.delete()
                StockItem.query.delete()
                ProductSupplier.query.delete()
                Product.query.delete()
                Location.query.delete()
                Category.query.delete()
                Supplier.query.delete()
                Salesperson.query.delete()
                db.session.commit()
                click.echo("✅ All demo data cleared!")