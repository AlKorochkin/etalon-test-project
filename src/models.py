from datetime import datetime
from typing import List
import uuid

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    MetaData,
    String,
    ForeignKey,
    UUID,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {uuid.UUID: UUID}
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    fullname: Mapped[str] = mapped_column(String(150))
    email_notify: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    projects: Mapped[List["Project"]] = relationship(back_populates="owner")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    location: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.current_timestamp()
    )

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    owner: Mapped["User"] = relationship(
        back_populates="projects", cascade="all, delete", passive_deletes=True
    )
