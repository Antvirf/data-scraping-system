# TODO dependency installation


# TODO private keys etc. configuration


# TODO base spinup






# TODO build all images
build:	build-scraper-28hse build-ingestion-service

# TODO run data collectors
collect: run-ingestion-service run-scraper-28hse

collect-local: run-scraper-locally-28hse

## ingestion
ingestion-image-name := ingestion-service
build-ingestion-service:
	docker build ./ingestion/ -t ${ingestion-image-name}

run-ingestion-service:
	docker run -p 8080:8080 ${ingestion-image-name}

## scraper - 28hse
build-scraper-28hse:
	docker build ./scrapers/28hse/ -t scraper-28hse

run-scraper-28hse:
	docker run scraper-28hse

run-scraper-locally-28hse:
	cd ./scrapers/28hse/ && python scraper_28hse.py