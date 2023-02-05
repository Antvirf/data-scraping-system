"""PostgreSQL-based storage backend."""
import logging
import os

from ingestion_backend import DataBackendABC
from pydantic import BaseModel
from sqlalchemy import MetaData, create_engine, inspect
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

    def __init__(self):
        logger.info("PSQL: Initializing PostgreSQL storage backend..")
        try:
            self.engine = create_engine(PSQL_CONNECTION_STRING)
            local_db_session = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine)

            self.db_session = local_db_session()
        except ValueError as e:
            logger.error("PSQL: Error creating DB engine",
                         e.with_traceback)
            raise e

    def __del__(self):
        self.db_session.close()

    def create_entry(self, entry):
        # check if table exists and create based on schema if it does not
        # if not self.engine.dialect.has_table(self.engine, entry.__tablename__):
        if not inspect(self.engine).has_table(entry.__tablename__):
            entry.__table__.create(self.engine)

        logger.debug("PSQL: Adding record")
        self.db_session.add(entry)
        self.db_session.commit()
        self.db_session.refresh(entry)
