"""Abstract base class for data backends"""

from abc import ABC

from pydantic import BaseModel


class DataBackendABC(ABC):
    """ABC for data backends to decouple API code from backend operations."""

    def __init__(self):
        """Implementation specific initialisation"""

    def __del__(self):
        """Implementation specific connection closure and object deletion"""

    def create_entry(self, table: str, entry):
        """C of CRUD"""

    def read_entry(self, table: str, entry_id: str):
        """R of CRUD"""

    def update_entry(self, table: str, entry):
        """U of CRUD"""

    def delete_entry(self, table: str, entry_id: str):
        """D of CRUD"""
