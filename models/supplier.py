"""
Supplier model for inventory management.
Inspired by InvenTree's supplier management.
"""
from datetime import datetime
from models import db


class Supplier(db.Model):
    """
    Supplier model for purchasing and reorder management.
    """
    __tablename__ = "supplier"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    contact_name = db.Column(db.String(100))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    lead_time_days = db.Column(db.Integer, default=7, nullable=False)  # For reorder planning
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

    product_suppliers = db.relationship(
        "ProductSupplier",
        back_populates="supplier",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Supplier {self.id}: {self.name}>"