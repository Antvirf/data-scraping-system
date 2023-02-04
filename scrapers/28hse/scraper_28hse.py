"""
Data scraping module for 28hse data that can be triggered on its own without further configuration.
Fetches recent listings on the main page for rental apartments, parses data and saves the output.
"""
import json
import logging

import bs4
import requests

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
    [x.text.strip() for x in entry.select(".tagLabels")[0].select(".ui")]
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


if __name__ == "__main__":
    URL = "https://www.28hse.com/en/rent/residential"
    domain = get_domain_from_url(URL)

    response = requests.get(URL)
    response.raise_for_status()
    logging.info("%s: Webpage fetched successfully", domain)

    souped_response = bs4.BeautifulSoup(response.text, 'html.parser')
    recent_listings = souped_response.select('.property_item')
    logging.info("%s: %s recent listings found", domain, len(recent_listings))

    listing_info = []
    for listing in recent_listings:
        listing_info.append(
            recent_listing_entry_into_dict(listing, scraper_dict_28hse)
        )

    with open("scraper_28hse_output.json", "w") as write_file:
        json.dump(listing_info, write_file, indent=4)
    print(listing_info)
