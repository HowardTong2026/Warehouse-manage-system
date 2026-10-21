"""
Category model with hierarchical structure (materialized path).
Inspired by InvenTree's category hierarchy.
"""
from datetime import datetime
from typing import List, Optional
from models import db


class Category(db.Model):
    """
    Hierarchical category model.
    Uses materialized path for O(1) subtree queries.
    """
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", ondelete="SET NULL"),
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
        "Category",
        remote_side=[id],
        back_populates="children"
    )
    children = db.relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan"
    )
    products = db.relationship("Product", back_populates="category")

    __table_args__ = (
        db.UniqueConstraint("name", "parent_id", name="uq_category_name_parent"),
        db.Index("ix_category_path", "path"),
    )

    def __repr__(self):
        return f"<Category {self.id}: {self.name}>"

    @property
    def level(self) -> int:
        """Return depth level (root = 0)."""
        return self.path.count("/") - 1 if self.path else 0

    def get_full_path(self) -> str:
        """Return full path name like 'Electronics > Computers > Laptops'."""
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

    def get_descendants(self) -> List["Category"]:
        """Get all descendant categories using materialized path."""
        return Category.query.filter(
            Category.path.like(f"{self.path}{self.id}/%")
        ).all()