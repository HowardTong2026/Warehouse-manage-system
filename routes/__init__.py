"""
Route blueprints package - exports all blueprints.
"""
from routes.products import products_bp
from routes.categories import categories_bp
from routes.suppliers import suppliers_bp
from routes.locations import locations_bp
from routes.stock import stock_bp
from routes.alerts import alerts_bp
from routes.salespeople import salespeople_bp
from routes.reports import reports_bp
from routes.dashboard import dashboard_bp

__all__ = [
    "products_bp", "categories_bp", "suppliers_bp", "locations_bp",
    "stock_bp", "alerts_bp", "salespeople_bp", "reports_bp", "dashboard_bp"
]