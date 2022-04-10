.DEFAULT_GOAL := help

help:
	@echo "build: Create the api image"
	@echo "run: Run the image on detached mode"
	@echo "up: Run the image and put a bash to interact with it"
	@echo "stop: Stops the image"
	@echo "down: Stops the image and removes the container"
	@echo "prune: Eliminates non used images"
	@echo "reset: Stop current image, eliminate the non used images and then build the container again"

build:
	@docker-compose build api

run:
	@docker-compose up -d

up: run
	@docker exec -it repositorium-api-1 /bin/bash

stop:
	@docker-compose stop

down:
	@docker-compose down

prune:
	@docker system prune -a

logs:
	@docker-compose logs

reset: down prune build
