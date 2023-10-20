REPO_NAME := temmiecvml
APP_NAME := lingua_trainer
IMAGE_TAG := 0.0.1
DOCKERFILE := Dockerfile.lingua_trainer
DOCKERHUB_USERNAME := $(REPO_NAME)
DOCKERHUB_TOKEN := $(shell echo $$DOCKERHUB_TOKEN)
TARGET_PLATFORM := linux/amd64
REGISTRY_NAME := index.docker.io # docker hub

login:
	docker login --username $(DOCKERHUB_USERNAME) --password $(DOCKERHUB_TOKEN) $(REGISTRY_NAME)
	
build:
	docker build --progress=plain --platform $(TARGET_PLATFORM) -f $(DOCKERFILE) . --no-cache -t $(REPO_NAME)/$(APP_NAME):$(IMAGE_TAG)
	
push:
	docker push $(REPO_NAME)/$(APP_NAME):$(IMAGE_TAG)

pull:
	docker pull $(REPO_NAME)/$(APP_NAME):$(IMAGE_TAG)

run:
	docker run -d -p 80:8501 $(REPO_NAME)/$(APP_NAME):$(IMAGE_TAG)
