"""
StockMovement model - append-only ledger for all inventory changes.
Inspired by flask-react-inventory's immutable movement log.
"""
from decimal import Decimal
from models import db


class StockMovement(db.Model):
    """
    Append-only ledger for all stock movements.
    Never updated or deleted - audit trail integrity.
    """
    __tablename__ = "stock_movement"

    id = db.Column(db.BigInteger, primary_key=True)

    # References
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id", ondelete="RESTRICT"),  # RESTRICT for audit trail
        nullable=False,
        index=True
    )
    location_id = db.Column(
        db.Integer,
        db.ForeignKey("location.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    salesperson_id = db.Column(
        db.Integer,
        db.ForeignKey("salesperson.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("supplier.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Movement classification
    type = db.Column(db.String(20), nullable=False, index=True)  # 'in', 'out', 'adjustment', 'transfer', 'return'
    reference_type = db.Column(db.String(20), index=True)  # 'sale', 'purchase', 'adjustment', 'transfer', 'return'
    reference_id = db.Column(db.Integer, index=True)  # Links to sale/purchase/adjustment record

    # Quantities (positive for in, negative for out)
    quantity = db.Column(db.Integer, nullable=False)

    # Price snapshot at movement time (critical for historical accuracy)
    unit_price_at_time = db.Column(db.Numeric(12, 2), nullable=False)
    total_amount = db.Column(db.Numeric(12, 2))  # quantity * unit_price_at_time

    # Context
    reason = db.Column(db.String(500))
    notes = db.Column(db.Text)
    changed_by = db.Column(db.String(100))  # Username or system

    # Timestamp
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        nullable=False,
        index=True
    )

    # Relationships
    product = db.relationship("Product", back_populates="stock_movements")
    location = db.relationship("Location")
    salesperson = db.relationship("Salesperson", back_populates="stock_movements")
    supplier = db.relationship("Supplier")

    __table_args__ = (
        db.CheckConstraint(
            "type IN ('in', 'out', 'adjustment', 'transfer', 'return')",
            name="ck_movement_type"
        ),
        db.CheckConstraint("quantity != 0", name="ck_movement_quantity_nonzero"),
        db.CheckConstraint("unit_price_at_time >= 0", name="ck_movement_price"),
        db.Index("ix_stock_movement_product_created", "product_id", "created_at"),
        db.Index("ix_stock_movement_salesperson_created", "salesperson_id", "created_at"),
        db.Index("ix_stock_movement_type_created", "type", "created_at"),
        db.Index("ix_stock_movement_reference", "reference_type", "reference_id"),
    )

    def __repr__(self):
        return f"<StockMovement {self.id}: {self.type} {self.quantity} of product {self.product_id}>"

    @property
    def is_in(self) -> bool:
        return self.type == "in"

    @property
    def is_out(self) -> bool:
        return self.type == "out"

    @property
    def is_sale(self) -> bool:
        return self.reference_type == "sale"

    @property
    def is_purchase(self) -> bool:
        return self.reference_type == "purchase"