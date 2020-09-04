.DEFAULT_GOAL := help
include ../../.bootstrap.mk

# NAME of the cloud run workload
NAME="your-namespace-release-bot"
# CONFIG file to upload to BUCKET
CONFIG="config.yaml"
# BUCKET to store config in
BUCKET="your-project_your-namespace_release_bot"
# IMAGE to deploy to NAME
IMAGE="gcr.io/your-project/github-release-bot"
# TAG is the container tag to use (optional)
TAG?=""
# SERVICE_ACCOUNT to use for NAME to access pubsub and storage
SERVICE_ACCOUNT="your-namespace-release-bot@your-project.iam.gserviceaccount.com"

##@ GitHub PR Preview Bot

sops_args=--in-place --encrypted-regex 'private_key' --gcp-kms projects/your-project/locations/global/keyRings/secrets/cryptoKeys/default

sops-en::
	sops --encrypt $(sops_args) config.yaml
	echo "sops: closed config.yaml"

sops-de::
	sops --decrypt $(sops_args) config.yaml
	echo "sops: opened config.yaml"

deploy:: ## Deploy
	$(MAKE) sops-de
	deploy-github-bot -n "$(NAME)" -c "$(CONFIG)" -b "$(BUCKET)" -i "$(IMAGE)" -s "$(SERVICE_ACCOUNT)" -t "$(TAG)"
	$(MAKE) sops-en

##@ Misc

help:: ## Display this help
	awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[%.a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
