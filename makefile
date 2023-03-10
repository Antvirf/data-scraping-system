# TODO dependency installation


# TODO private keys etc. configuration


# base spinup
up:
	docker-compose build
	docker-compose up

# initialize data
initialize: initialize-data-28hse

# spin down, including removall of all volumes (i.e. loses all data)
down:
	docker-compose down --volumes

# TODO build all images
build-images: build-scraper-28hse build-ingestion-service

# TODO run data collectors
collect: run-scraper-28hse
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
	cd ./scrapers/28hse/ && python scraper_28hse.py -o ingestion-service

initialize-data-28hse:
	cd ./scrapers/28hse/ && python scraper_28hse.py --initialize-db

run-scraper-locally-28hse:
	cd ./scrapers/28hse/ && python scraper_28hse.py