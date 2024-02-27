REPO_NAME := temmiecvml
BACKEND_VERSION := 0.0.2-g # g refers to arm version
STREAMLIT_APPS_VERSION := 0.0.2-g
DOCKERFILE_BACKEND := Dockerfile.backend
DOCKERFILE_STREAMLIT_APPS := Dockerfile.streamlit_apps
CI_REGISTRY_USER := $(REPO_NAME) # add to ci/cd > variables 
CI_REGISTRY_PASSWORD := $(shell echo $$CI_REGISTRY_PASSWORD) # add to ci/cd > variables 
TARGET_PLATFORM := linux/arm64 # linux/arm64, linux/amd64
CI_REGISTRY := docker.io # add to ci/cd > variables  
CI_REGISTRY_IMAGE_BACKEND := index.docker.io/$(REPO_NAME)/hyc-backend:$(BACKEND_VERSION)
CI_REGISTRY_IMAGE_STREAMLIT_APPS := index.docker.io/$(REPO_NAME)/hyc-streamlit-apps:$(STREAMLIT_APPS_VERSION)
DEFAULT_API_KEY := $(shell echo $$DEFAULT_API_KEY)

login:
	docker login --username $(CI_REGISTRY_USER) --password $(CI_REGISTRY_PASSWORD) $(CI_REGISTRY)
	
build:
	docker build --progress=plain --build-arg DEFAULT_API_KEY=$(DEFAULT_API_KEY) --platform $(TARGET_PLATFORM) -f $(DOCKERFILE_BACKEND) . --no-cache -t $(CI_REGISTRY_IMAGE_BACKEND)
	docker build --progress=plain --platform $(TARGET_PLATFORM) -f $(DOCKERFILE_STREAMLIT_APPS) . --no-cache -t $(CI_REGISTRY_IMAGE_STREAMLIT_APPS)
	
push:
	docker push $(CI_REGISTRY_IMAGE_BACKEND)
	docker push $(CI_REGISTRY_IMAGE_STREAMLIT_APPS)

pull:
	docker pull $(CI_REGISTRY_IMAGE_BACKEND)
	docker pull $(CI_REGISTRY_IMAGE_STREAMLIT_APPS)

run:
	docker run -d -p 8100:8100 $(CI_REGISTRY_IMAGE_BACKEND)
	docker run -d -p 8501:8501 $(CI_REGISTRY_IMAGE_STREAMLIT_APPS)
