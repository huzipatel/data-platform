# Define variables
APP_NAME = python-app
ACR_NAME = rtdataplatform.azurecr.io
IMAGE_NAME = $(ACR_NAME)/$(APP_NAME)
VERSION_FILE = VERSION

# Fetch the current version from the VERSION file
VERSION = $(shell cat $(VERSION_FILE))

# Define the next version (increment the patch number)
NEXT_VERSION = $(shell echo $(VERSION) | awk -F. '{$$NF = $$NF + 1;} 1' | sed 's/ /./g')

# Default rule to build, tag, and push the Docker image
all: build tag push

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

# Tag the Docker image with the incremented version number
tag:
	docker tag $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):$(NEXT_VERSION)

# Push the Docker image to ACR
push:
	docker push $(IMAGE_NAME):$(NEXT_VERSION)
	@echo "Pushed $(IMAGE_NAME):$(NEXT_VERSION) to ACR"

# Update the VERSION file with the new version
update_version:
	echo $(NEXT_VERSION) > $(VERSION_FILE)
	@echo "Updated version to $(NEXT_VERSION)"

# Clean up old Docker images (optional)
clean:
	docker rmi $(IMAGE_NAME):$(VERSION)

# Full pipeline: build, tag, push, and update version
release: all update_version
	@echo "Released version $(NEXT_VERSION)"
