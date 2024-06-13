# also for initial dev purposes

IMAGE_NAME=brnoblend_web

CONTAINER_ENGINE ?= $(shell command -v podman 2> /dev/null || echo docker)


# regenerate new image when needed
build-base-image:
	$(CONTAINER_ENGINE) build --rm --tag $(IMAGE_NAME) -f ./docker/Containerfile


enter-container:
	$(CONTAINER_ENGINE) exec -ti $(IMAGE_NAME) bash
