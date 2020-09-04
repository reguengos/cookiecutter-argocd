.DEFAULT_GOAL := help
include ../.bootstrap.mk

##@ All Bots

bots:: ## Deploy all bots
	$(MAKE) preview-bot release-bot

##@ Individual Bots

preview-bot:: ## Deploy the preview bot
	echo "preview-bot:"
	make -C preview-bot deploy

release-bot:: ## Deploy the release bot
	echo "release-bot:"
	make -C release-bot deploy

##@ Misc

help:: ## Display this help
	awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[%.a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
