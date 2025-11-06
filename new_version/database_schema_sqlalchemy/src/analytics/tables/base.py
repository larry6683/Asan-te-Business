"""
Analytics schema base - shares Base with public schema

This ensures all tables (public and analytics) are in the same metadata,
which is required for cross-schema foreign key references to work.
"""
from src.public.tables.base import Base

# Export the same Base that public uses
# This means both public and analytics tables will be in the same metadata
__all__ = ['Base']