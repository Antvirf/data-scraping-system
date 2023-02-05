"""Pydantic datamodel for scraper_28hse listings"""
from typing import Union

from pydantic import BaseModel


class scraped_listing(BaseModel):
    """Data model for FastAPI"""
    listingId: str
    listingUrl: str

    listingTitle: Union[str, None] = None
    listingPostedAgo: Union[str, None] = None
    listingTags: Union[list[str], None] = None
    listingCompanyName: Union[str, None] = None
    listingBuilding: Union[str, None] = None
    listingArea: Union[str, None] = None

    listingGrossArea: Union[float, None] = None
    listingSaleableArea: Union[float, None] = None
    listingPrice: Union[float, None] = None

    scrapeTime: Union[float, None] = None
