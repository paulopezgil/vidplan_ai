import uuid
from datetime import datetime

from sqlalchemy import Text, ForeignKey, Column, Table, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from backend.core.database import Base

# Association table for Many-to-Many relationship between Projects and Tags
project_tags = Table(
    "project_tags",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, unique=True, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    projects: Mapped[list["Project"]] = relationship(
        "Project", secondary=project_tags, back_populates="tags"
    )