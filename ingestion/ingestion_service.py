"""Data ingestion API that interacts with the persistence backend."""

import logging
import os

from backends.postgres.db_model_28hse import ScrapedListingDbEntry
from backends.postgres.postgres import PostgresBackend
from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi_pagination import Page, Params, add_pagination, paginate
# 28hse specific models
from models.model_28hse import ScrapedListing

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
add_pagination(app)

storage_backend = AVAILABLE_BACKENDS[INGESTION_STORAGE_BACKEND]()

# ops endpoints


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return "ingestion service is alive"


@app.post("/ingest/debug/")
def ingest_incoming_data_any(incoming):
    """Prints incoming data to standard out and INFO logs for debugging."""
    logging.info(incoming)
    print(incoming)
    return 0


# scrapers' endpoints - 28hse

@app.post("/ingest/28hse/")
def ingest_incoming_data_28hse(listing: ScrapedListing):
    """Takes a scrapedListing from the POST request payload and stores it in storage backend."""
    new_listing = ScrapedListingDbEntry(**listing.dict())
    storage_backend.create_entry(new_listing)
    return "record created"


@app.get("/data/28hse/", response_model=Page[str])
def fetch_data_28hse(params: Params = Depends()):
    """Fetches list of 28hse datapoint IDs"""
    list_of_ids = storage_backend.read_entry_ids(
        "listingId", ScrapedListingDbEntry)
    if not list_of_ids:
        raise HTTPException(status_code=404,
                            detail="No records found")
    return paginate(list_of_ids, params)


@app.get("/data/28hse/{identifier}")
def fetch_data_by_id_28hse(identifier: str):
    """Fetches a scraped 28hse datapoint by ID"""
    record = storage_backend.read_entry(
        "listingId", identifier, ScrapedListingDbEntry)
    if not record:
        raise HTTPException(status_code=404,
                            detail=f"No record found with id: {identifier}")
    return record


@app.delete("/data/28hse/{identifier}")
def delete_data_by_id_28hse(identifier: str):
    """Deletes a scraped 28hse datapoint by ID"""
    deleted = storage_backend.delete_entry(
        "listingId", identifier, ScrapedListingDbEntry)
    if not deleted:
        raise HTTPException(status_code=404,
                            detail=f"No record found with id: {identifier}")
    return Response(status_code=204)
