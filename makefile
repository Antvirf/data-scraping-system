# TODO dependency installation


# TODO private keys etc. configuration


# TODO base spinup

# TODO build all images
build:	build-scraper-28hse

# TODO run data collectors
collect: run-scraper-28hse
	echo "Data collected"



## scraper - 28hse
build-scraper-28hse:
	docker build ./scrapers/28hse/ -t scraper-28hse

run-scraper-28hse:
	docker run scraper-28hse