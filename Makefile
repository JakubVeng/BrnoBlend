# also for initial dev purposes

IMAGE_NAME=brno-blend

CONTAINER_ENGINE ?= $(shell command -v podman 2> /dev/null || echo docker)


# regenerate new image when needed
build-image:
	$(CONTAINER_ENGINE) build --rm --tag $(IMAGE_NAME) -f ./docker/Containerfile


enter-image:
	$(CONTAINER_ENGINE) run -v .:/opt/brno-blend:z -ti $(IMAGE_NAME) bash
