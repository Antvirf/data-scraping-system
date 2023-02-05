"""Pydantic datamodel for scraper_28hse listings"""
from sqlalchemy import (TIMESTAMP, Boolean, Column, Float, ForeignKey, String,
                        text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base_model = declarative_base()


class scraped_listing_db_entry(base_model):
    """Data model for SQLAlchemy"""
    __tablename__ = 'scraper_28hse'

    listingId = Column(String, nullable=False, primary_key=True)
    listingUrl = Column(String, nullable=False)
    listingTitle = Column(String, nullable=False)

    listingPostedAgo = Column(String, nullable=True)
    listingTags = Column(String, nullable=True)
    listingCompanyName = Column(String, nullable=True)
    listingBuilding = Column(String, nullable=True)
    listingArea = Column(String, nullable=True)

    listingGrossArea = Column(Float, nullable=True)
    listingSaleableArea = Column(Float, nullable=True)
    listingPrice = Column(Float, nullable=True)
    scrapeTime = Column(Float, nullable=True)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
