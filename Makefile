REPO_NAME := temmiecvml
APP_NAME := lingua_trainer/word_explorer
IMAGE_TAG := 0.0.1
DOCKERFILE := Dockerfile.lingua_trainer

	
build:
	docker build --progress=plain -f $(DOCKERFILE) . --no-cache -t $(REPO_NAME)/$(APP_NAME):$(IMAGE_TAG)
	
push:
	docker push $(REPO_NAME)/$(APP_NAME):$(IMAGE_TAG)

pull:
	docker pull $(REPO_NAME)/$(APP_NAME):$(IMAGE_TAG)
