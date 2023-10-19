REGION := us-east-1
ACCOUNT_ID := 222311789433
REPO_NAME := lingua_trainer/word_explorer
IMAGE_TAG := 0.0.1
DOCKERFILE := Dockerfile.lingua_trainer
TARGET_PLATFORM := linux/amd64

ecr_login:
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com

ecr_create_repo:
	aws --region $(REGION) ecr create-repository --repository-name $(REPO_NAME)
	
ecr_build:
	docker build --progress=plain --platform $(TARGET_PLATFORM) -f $(DOCKERFILE) . --no-cache -t $(IMAGE_TAG) -t $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(REPO_NAME):$(IMAGE_TAG)

ecr_push:
	docker push $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(REPO_NAME):$(IMAGE_TAG)

ecr_pull:
	- make ecr_login
	- docker pull $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(REPO_NAME):$(IMAGE_TAG)

con_run:
	docker run -d -p 80:8501 $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(REPO_NAME):$(IMAGE_TAG)
