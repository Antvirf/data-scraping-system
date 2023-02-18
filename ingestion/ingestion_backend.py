"""Abstract base class for data backends"""

from abc import ABC


class DataBackendABC(ABC):
    """ABC for data backends to decouple API code from backend operations."""

    def __init__(self):
        """Implementation specific initialisation"""

    def __del__(self):
        """Implementation specific connection closure and object deletion"""

    def create_entry(self, entry):
        """C / U of CRUD"""

    def read_entry(self, id_field: str, entry_id: str, model):
        """R of CRUD"""

    def read_entry_ids(self, id_field: str, model):
        """R of CRUD but return list of IDs"""

    def delete_entry(self, id_field: str, entry_id: str, model) -> bool:
        """D of CRUD"""
