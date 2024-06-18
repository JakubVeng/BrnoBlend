# also for initial dev purposes

IMAGE_NAME=brnoblend_web

CONTAINER_ENGINE ?= $(shell command -v podman 2> /dev/null || echo docker)
COMPOSE ?= $(shell command -v podman-compose 2> /dev/null || echo docker-compose)


# regenerate new image when needed
build-base-image:
	$(CONTAINER_ENGINE) build --rm --tag $(IMAGE_NAME) -f ./docker/Containerfile


enter-container:
	$(CONTAINER_ENGINE) exec -ti $(IMAGE_NAME) bash

app-up:
	$(COMPOSE) up -d

app-down:
	$(COMPOSE) down

restart-app:
	$(COMPOSE) restart
