"""
Product-Supplier association model.
Many-to-many with supplier-specific data (inspired by InvenTree).
"""
from models import db


class ProductSupplier(db.Model):
    """
    Links products to suppliers with supplier-specific pricing and SKU.
    """
    __tablename__ = "product_supplier"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("supplier.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    supplier_sku = db.Column(db.String(100))  # Supplier's part number
    supplier_price = db.Column(db.Numeric(12, 2))  # Purchase price from this supplier
    min_order_qty = db.Column(db.Integer, default=1, nullable=False)
    is_preferred = db.Column(db.Boolean, default=False, nullable=False)
    lead_time_days = db.Column(db.Integer)  # Override supplier default
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

    product = db.relationship("Product", back_populates="suppliers")
    supplier = db.relationship("Supplier", back_populates="product_suppliers")

    __table_args__ = (
        db.UniqueConstraint("product_id", "supplier_id", name="uq_product_supplier"),
        db.Index("ix_product_supplier_preferred", "product_id", "is_preferred"),
    )

    def __repr__(self):
        return f"<ProductSupplier product={self.product_id} supplier={self.supplier_id}>"