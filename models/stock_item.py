"""
StockItem model - per-location stock tracking (InvenTree pattern).
Separates logical product from physical stock location.
"""
from models import db


class StockItem(db.Model):
    """
    Physical stock at a specific location.
    Supports batch/serial tracking for regulated industries.
    """
    __tablename__ = "stock_item"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    location_id = db.Column(
        db.Integer,
        db.ForeignKey("location.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    quantity = db.Column(db.Integer, nullable=False, default=0)
    reserved = db.Column(db.Integer, nullable=False, default=0)
    available = db.Column(db.Integer, nullable=False, default=0)

    # Batch/serial tracking
    batch_number = db.Column(db.String(100), index=True)
    serial_numbers = db.Column(db.JSON)  # List of serial numbers if track_serial

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

    product = db.relationship("Product", back_populates="stock_items")
    location = db.relationship("Location", back_populates="stock_items")

    __table_args__ = (
        db.UniqueConstraint("product_id", "location_id", "batch_number", name="uq_stock_item"),
        db.CheckConstraint("quantity >= 0", name="ck_stock_item_quantity"),
        db.CheckConstraint("reserved >= 0", name="ck_stock_item_reserved"),
        db.CheckConstraint("available >= 0", name="ck_stock_item_available"),
        db.Index("ix_stock_item_location_product", "location_id", "product_id"),
    )

    def __repr__(self):
        return f"<StockItem product={self.product_id} loc={self.location_id} qty={self.quantity}>"

    @property
    def is_low_stock(self) -> bool:
        """Check if stock item is at or below product's reorder threshold."""
        return self.available <= self.product.reorder_threshold

    def compute_available(self) -> int:
        """Compute available = quantity - reserved."""
        self.available = max(0, self.quantity - self.reserved)
        return self.available