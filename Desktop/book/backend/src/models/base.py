"""Base model configuration for SQLAlchemy ORM.

Provides the declarative base class that all models inherit from.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    All database models should inherit from this class to be part of the
    SQLAlchemy ORM metadata system.
    """
    pass
