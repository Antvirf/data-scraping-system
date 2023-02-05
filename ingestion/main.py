"""Data ingestion API that interacts with the persistence backend."""

import logging
import os

from fastapi import FastAPI
from models.model_28hse import scrapedListing

INGESTION_STORAGE_BACKEND = os.getenv(
    "INGESTION_STORAGE_BACKEND", default="POSTGRES")
INGESTION_STORAGE_BACKEND_HOST = os.getenv(
    "INGESTION_STORAGE_BACKEND_HOST", default="localhost")
INGESTION_STORAGE_BACKEND_PORT = os.getenv(
    "INGESTION_STORAGE_BACKEND_PORT", default=5432)

INGESTION_LOGGING_LEVEL = {
    "DEBUG":  logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL

}[os.getenv("LOGGING_LEVEL", default="INFO")]

# logger configuration
logger = logging.getLogger()
logger.setLevel(INGESTION_LOGGING_LEVEL)

app = FastAPI()

# ingestion endpoints


@app.post("/ingest/28hse/")
def ingest_incoming_data_28hse(listing: scrapedListing):
    return listing


@app.post("/ingest/debug/")
def ingest_incoming_data_any(incoming):
    return 0


# ops endpoints

@app.get("/health")
def read_root():
    return "ingestion service is alive"
