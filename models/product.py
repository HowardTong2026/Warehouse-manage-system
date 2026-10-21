"""
Product model - core inventory entity.
Inspired by InvenTree's part management.
"""
from decimal import Decimal
from models import db


class Product(db.Model):
    """
    Product model with inventory tracking, pricing, and supplier relationships.
    """
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(50), nullable=False, unique=True, index=True)
    barcode = db.Column(db.String(100), unique=True, index=True)
    description = db.Column(db.Text)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Pricing
    unit_price = db.Column(db.Numeric(12, 2), nullable=False, default=0)  # Selling price
    cost_price = db.Column(db.Numeric(12, 2), default=0, nullable=False)  # For margin calc

    # Inventory
    reorder_threshold = db.Column(db.Integer, nullable=False, default=10)
    reorder_quantity = db.Column(db.Integer, nullable=False, default=50)
    current_stock = db.Column(db.Integer, nullable=False, default=0)  # Denormalized total
    reserved_stock = db.Column(db.Integer, nullable=False, default=0)  # Allocated to pending
    available_stock = db.Column(db.Integer, nullable=False, default=0)  # Computed: current - reserved

    # Tracking options
    track_serial = db.Column(db.Boolean, default=False, nullable=False)  # Serialized items
    track_batch = db.Column(db.Boolean, default=False, nullable=False)   # Batch/lot tracking

    # Metadata
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False
    )

    # Relationships
    category = db.relationship("Category", back_populates="products")
    stock_movements = db.relationship(
        "StockMovement",
        back_populates="product",
        cascade="all, delete-orphan"
    )
    suppliers = db.relationship(
        "ProductSupplier",
        back_populates="product",
        cascade="all, delete-orphan"
    )
    stock_items = db.relationship(
        "StockItem",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.CheckConstraint("unit_price >= 0", name="ck_product_unit_price"),
        db.CheckConstraint("cost_price >= 0", name="ck_product_cost_price"),
        db.CheckConstraint("reorder_threshold >= 0", name="ck_product_reorder_threshold"),
        db.CheckConstraint("reorder_quantity >= 0", name="ck_product_reorder_quantity"),
        db.CheckConstraint("current_stock >= 0", name="ck_product_current_stock"),
        db.CheckConstraint("reserved_stock >= 0", name="ck_product_reserved_stock"),
        db.CheckConstraint("available_stock >= 0", name="ck_product_available_stock"),
        db.Index("ix_product_category_active", "category_id", "is_active"),
        db.Index("ix_product_sku_active", "sku", "is_active"),
    )

    def __repr__(self):
        return f"<Product {self.id}: {self.sku} - {self.name}>"

    @property
    def is_low_stock(self) -> bool:
        """Check if product is at or below reorder threshold."""
        return self.available_stock <= self.reorder_threshold

    @property
    def margin_percent(self) -> float:
        """Calculate profit margin percentage."""
        if self.unit_price and self.unit_price > 0:
            return float((self.unit_price - self.cost_price) / self.unit_price * 100)
        return 0.0

    def compute_available_stock(self) -> int:
        """Compute available stock from current - reserved."""
        self.available_stock = max(0, self.current_stock - self.reserved_stock)
        return self.available_stock