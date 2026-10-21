"""
Salesperson model for sales attribution and performance tracking.
"""
from datetime import date
from models import db


class Salesperson(db.Model):
    """
    Salesperson model for attributing sales and tracking performance.
    """
    __tablename__ = "salesperson"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, index=True)
    phone = db.Column(db.String(20))
    employee_id = db.Column(db.String(50), unique=True, index=True)  # HR system ID
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    hire_date = db.Column(db.Date)
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

    stock_movements = db.relationship(
        "StockMovement",
        back_populates="salesperson"
    )

    def __repr__(self):
        return f"<Salesperson {self.id}: {self.name}>"