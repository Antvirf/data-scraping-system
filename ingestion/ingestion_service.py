"""Data ingestion API that interacts with the persistence backend."""

import logging
import os

from backends.postgres.db_model_28hse import scraped_listing_db_entry
from backends.postgres.postgres import PostgresBackend
from fastapi import Depends, FastAPI
from ingestion_backend import DataBackendABC
# 28hse specific models
from models.model_28hse import scraped_listing

INGESTION_STORAGE_BACKEND = os.getenv(
    "INGESTION_STORAGE_BACKEND", default="POSTGRES")
INGESTION_STORAGE_BACKEND_HOST = os.getenv("INGESTION_STORAGE_BACKEND_HOST")
INGESTION_STORAGE_BACKEND_PORT = os.getenv("INGESTION_STORAGE_BACKEND_PORT")

INGESTION_LOGGING_LEVEL = {
    "DEBUG":  logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL

}[os.getenv("LOGGING_LEVEL", default="INFO")]

# internally set constants
AVAILABLE_BACKENDS = {
    "POSTGRES": PostgresBackend
}


# logger configuration
logger = logging.getLogger()
logger.setLevel(INGESTION_LOGGING_LEVEL)

app = FastAPI()

storage_backend = AVAILABLE_BACKENDS[INGESTION_STORAGE_BACKEND]()

# ingestion endpoints


@app.post("/ingest/28hse/")
def ingest_incoming_data_28hse(listing: scraped_listing):
    """Takes data from the POST request payload and stores it in storage backend."""
    new_listing = scraped_listing_db_entry(**listing.dict())
    storage_backend.create_entry(new_listing)
    return listing


@app.post("/ingest/debug/")
def ingest_incoming_data_any(incoming):
    """Prints incoming data to standard out and INFO logs for debugging."""
    logging.info(incoming)
    print(incoming)
    return 0

# ops endpoints


@app.get("/health")
def read_root():
    """Health check endpoint"""
    return "ingestion service is alive"
