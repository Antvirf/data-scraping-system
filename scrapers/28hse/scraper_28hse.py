"""
Data scraping module for 28hse data that can be triggered on its own without further configuration.
Fetches recent listings on the main page for rental apartments, parses data and saves the output.
"""
import argparse
import json
import logging
import time

import bs4
import requests

# constants
FILE_OUTPUT_NAME = "scraper_28hse_output.json"


scraper_dict_28hse = {
    "listingTitle": lambda entry:
        entry.select(".detail_page")[1].text,
    "listingId": lambda entry:
        entry.select(".detail_page")[1].get_attribute_list("attr1")[0],
    "listingUrl": lambda entry:
        entry.select(".detail_page")[1].get_attribute_list("href")[0],
    "listingPostedAgo": lambda
        entry: entry.select(".description")[0].select(".ui")[0].text.strip(),
    "listingArea": lambda entry:
        entry.select(".district_area")[0].select("a")[0].text,
    "listingBuilding": lambda entry:
        entry.select(".district_area")[0].select("a")[1].text,
    "listingGrossArea": lambda entry:
        float(entry.select(".areaUnitPrice")[
            0].select("div")[0].text.split(" ")[2].replace(",", "")),
    "listingSaleableArea": lambda entry:
        float(entry.select(".areaUnitPrice")[
            0].select("div")[1].text.split(" ")[2].replace(",", "")),
    "listingCompanyName": lambda entry:
        entry.select(".companyName")[0].text.strip(),
    "listingPrice": lambda entry:
        float(entry.select(".green")[0].text.split(
            "$")[-1].replace(",", "")),
    "listingTags": lambda entry:
    [x.text.strip() for x in entry.select(".tagLabels")[0].select(".ui")],
    "scrapeTime": lambda entry:
        time.time()
}


def get_domain_from_url(input_url: str) -> str:
    """Cleans up an URL into a logging-friendly domain name by removing prefixes and
    postfixes/paths."""
    # prefixes
    for prefix in ["//", "www."]:
        input_url = input_url if prefix not in input_url else input_url.split(prefix)[
            1]

    # postfixes
    for postfix in ["/"]:
        input_url = input_url if postfix not in input_url else input_url.split(postfix)[
            0]
    return input_url


def recent_listing_entry_into_dict(entry: bs4.element.Tag, processing_dict: dict) -> dict:
    """Converts a bs4 tag of a listing element into a dictionary of strings and floats"""
    listing_dict = {}

    for field, field_parsing_function in processing_dict.items():
        try:
            listing_dict[field] = field_parsing_function(entry)
        except IndexError:
            logging.warning(
                "%s: Listing %s: Failed to fetch '%s'", domain, listing_dict["listingId"], field)
            listing_dict[field] = None

    return listing_dict


def merge_listing_lists(existing_listings: list, new_listings: list, overwrite: bool = False) -> list:
    existing_ids = [x["listingId"] for x in existing_listings]
    new_ids = [x["listingId"] for x in new_listings]
    duplicated_ids = [x for x in existing_ids if x in new_ids]

    if overwrite:
        # take only non-overlap from existing data, and then use all of new data
        merged_listings = [
            x for x in existing_listings if x["listingId"] not in duplicated_ids] + [x for x in new_listings]
    else:
        # not overwriting - so keep everything from old, and take only non-overlap from new
        merged_listings = [x for x in existing_listings] + \
            [x for x in new_listings if x["listingId"] not in duplicated_ids]

    return merged_listings


if __name__ == "__main__":
    # parse inputs configuring the scraper
    parser = argparse.ArgumentParser("scraper_28hse")
    parser.add_argument(
        "-o", "--output",
        help="Specify output type - e.g. outgoing REST call or local JSON file",
        default="json",
        type=str
    )
    args = vars(parser.parse_args())

    # scrape data
    URL = "https://www.28hse.com/en/rent/residential"
    domain = get_domain_from_url(URL)

    response = requests.get(URL)
    response.raise_for_status()
    logging.info("%s: Webpage fetched successfully", domain)

    souped_response = bs4.BeautifulSoup(response.text, 'html.parser')
    recent_listings = souped_response.select('.property_item')
    logging.info("%s: %s recent listings found", domain, len(recent_listings))

    new_listing_data = []
    for listing in recent_listings:
        new_listing_data.append(
            recent_listing_entry_into_dict(listing, scraper_dict_28hse)
        )

    # save output as specified
    if args["output"].lower() == "json":
        # open file if exists
        try:
            with open(FILE_OUTPUT_NAME, "r") as read_file:
                existing_listing_data = json.load(read_file)
        except FileNotFoundError:
            existing_listing_data = []

        # merge list of dicts
        combined_listing_data = merge_listing_lists(
            existing_listing_data,
            new_listing_data,
            overwrite=False
        )
        with open(FILE_OUTPUT_NAME, "w") as write_file:
            json.dump(combined_listing_data, write_file, indent=4)

    else:
        raise NotImplementedError(
            "'json' is the only available output method.")
