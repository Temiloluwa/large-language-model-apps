REPO_NAME := temmiecvml
APP_NAME := lingua_trainer/word_explorer
VERSION := 0.0.1
IMAGE_TAG := $(REPO_NAME)/$(APP_NAME):$(VERSION)
DOCKERFILE := Dockerfile.lingua_trainer
DOCKERHUB_USERNAME := $(REPO_NAME)
DOCKERHUB_PASSWORD := $(shell echo $$DOCKERHUB_PASSWORD)
TARGET_PLATFORM := linux/amd64
REGISTRY_NAME := index.docker.io # docker hub

login:
	docker login --username $(DOCKERHUB_USERNAME) --password $(DOCKERHUB_TOKEN) $(REGISTRY_NAME)
	
build:
	docker build --progress=plain --platform $(TARGET_PLATFORM) -f $(DOCKERFILE) . --no-cache -t $(IMAGE_TAG)
	
push:
	docker push 

pull:
	docker pull $(IMAGE_TAG)

run:
	docker run -d -p 80:8501 $(IMAGE_TAG)