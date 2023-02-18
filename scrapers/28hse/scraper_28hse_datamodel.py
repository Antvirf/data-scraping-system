"""Dict of keys and data extraction functions for the scraper"""
import time

scraper_dict_28hse = {
    "listingTitle": lambda entry:
        entry.select(".detail_page")[1].text,
    "listingId": lambda entry:
        entry.select(".detail_page")[1].get_attribute_list("attr1")[0],
    "listingUrl": lambda entry:
        entry.select(".detail_page")[1].get_attribute_list("href")[0],
    "listingPostedAgo": lambda
        entry: entry.select(".description")[0].select(".ui")[0].text.strip(),
    "listingBuilding": lambda entry:
        entry.select(".district_area")[0].select("a")[1].text,
    "listingArea": lambda entry:
        entry.select(".district_area")[0].select("a")[0].text,
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
