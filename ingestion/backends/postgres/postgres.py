"""PostgreSQL-based storage backend."""
import logging
import os

from ingestion_backend import DataBackendABC
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

PSQL_USER = os.getenv("POSTGRES_USER")
PSQL_PASS = os.getenv("POSTGRES_PASSWORD")
PSQL_HOST = os.getenv("INGESTION_DB_HOST")
PSQL_PORT = os.getenv("INGESTION_DB_PORT")
PSQL_DB = os.getenv("INGESTION_DB_DBNAME")

INGESTION_LOGGING_LEVEL = {
    "DEBUG":  logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL

}[os.getenv("LOGGING_LEVEL", default="INFO")]


PSQL_CONNECTION_STRING = f"postgresql://{PSQL_USER}:{PSQL_PASS}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DB}"


# logger configuration
logger = logging.getLogger()
logger.setLevel(INGESTION_LOGGING_LEVEL)


class PostgresBackend(DataBackendABC):
    """Implementation of data backend ABC for PostgreSQL using SQL Alchemy"""

    def __init__(self):
        super().__init__()
        logger.info("PSQL: Initializing PostgreSQL storage backend..")
        try:
            self.engine = create_engine(PSQL_CONNECTION_STRING)
            local_db_session = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine)

            self.db_session = local_db_session()
        except ValueError as error:
            logger.error("PSQL: Error creating DB engine")
            raise error

    def __del__(self):
        self.db_session.close()

    def create_entry(self, entry):
        """C / U of CRUD using SQL Alchemy's MERGE"""
        # check if table exists and create based on schema if it does not
        # if not self.engine.dialect.has_table(self.engine, entry.__tablename__):
        if not inspect(self.engine).has_table(entry.__tablename__):
            entry.__table__.create(self.engine)

        logger.debug("PSQL: Adding record")
        self.db_session.merge(entry)
        self.db_session.commit()

    def read_entry(self, id_field: str, entry_id: str, model):
        """"R of CRUD by ID, allowing for the ID field to be specified."""
        entry = self.db_session.query(model).filter(
            getattr(model, id_field, None) == entry_id).first()
        if not entry:
            return False
        return entry

    def read_entry_ids(self, id_field: str, model):
        """R of CRUD but return list of IDs"""
        list_of_ids = self.db_session.query(getattr(model, id_field)).all()
        list_of_ids = [x[0] for x in list_of_ids]
        if not list_of_ids:
            return False
        return list_of_ids

    def delete_entry(self, id_field: str, entry_id: str, model):
        """D of CRUD by ID, allowing for the ID field to be specified."""
        entry = self.db_session.query(model).filter(
            getattr(model, id_field, None) == entry_id)
        if not entry:
            return False
        entry.delete(synchronize_session=False)
        self.db_session.commit()
        return True
