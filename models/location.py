"""
Location model with hierarchical structure (warehouse/zone/bin).
Inspired by InvenTree's stock location hierarchy.
"""
from datetime import datetime
from typing import List
from models import db


class Location(db.Model):
    """
    Hierarchical location model for multi-warehouse support.
    Uses materialized path for O(1) subtree queries.
    """
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("location.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    # Materialized path: e.g., '1/5/12/' for O(1) subtree queries
    path = db.Column(db.String(500), nullable=False, default="/")
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

    # Self-referential relationship
    parent = db.relationship(
        "Location",
        remote_side=[id],
        back_populates="children"
    )
    children = db.relationship(
        "Location",
        back_populates="parent",
        cascade="all, delete-orphan"
    )
    stock_items = db.relationship(
        "StockItem",
        back_populates="location",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint("name", "parent_id", name="uq_location_name_parent"),
        db.Index("ix_location_path", "path"),
    )

    def __repr__(self):
        return f"<Location {self.id}: {self.name}>"

    @property
    def level(self) -> int:
        """Return depth level (root = 0)."""
        return self.path.count("/") - 1 if self.path else 0

    def get_full_path(self) -> str:
        """Return full path name like 'Warehouse A > Zone 1 > Bin 3'."""
        parts = []
        current = self
        while current:
            parts.append(current.name)
            current = current.parent
        return " > ".join(reversed(parts))

    def update_path(self):
        """Update materialized path based on parent."""
        if self.parent:
            self.path = f"{self.parent.path}{self.parent.id}/"
        else:
            self.path = "/"

    def get_descendants(self) -> List["Location"]:
        """Get all descendant locations using materialized path."""
        return Location.query.filter(
            Location.path.like(f"{self.path}{self.id}/%")
        ).all()