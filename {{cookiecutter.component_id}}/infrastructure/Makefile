.DEFAULT_GOAL := help
include .bootstrap.mk

## All CI/CD infrastructure will be created/deployed to your staging environment as to not duplicated it and create unessicary redundancy. This is why some values are hardcoded to stage.

##@ Setup
HELM_VERSION=$(shell helm version --client | sed -En 's/.*Version\:"v([0-9]+)\.([0-9]+)\.([0-9]+)".*/\1/p')
TERRAFORM_VERSION="0.12.26"
ENVIRONMENT="stage"

ifeq "$(BRANCH_NAME)" "main"
	ENVIRONMENT="prod"
endif

install-deps:: ## Install local dependancies 
	echo "Installing dependancies..."
	install-local-deps

bootstrap:: ## Deploy Secrets, ArgoCD, and supporting infra
	echo "switching context to ${ENVIRONMENT} env"
	gcloud container clusters get-credentials tools-stage0-eu-w4 --region europe-west4 --project {{cookiecutter.k8s_project}}
	echo "switching context to {{cookiecutter.k8s_namespace}} namespace"
	kubectl config set-context --current --namespace={{cookiecutter.k8s_namespace}}
	echo "Deploying Secrets"
	$(MAKE) k8s-secrets 
	echo "Terraform init & apply"
	## $(MAKE) k8s-secrets plan-infra-data-prod plan-infra-conceptstream-prod apply-infra-data-prod apply-infra-conceptstream-prod
	$(MAKE) terra-init terra-apply 
	echo "deploying argo-cd"
	helm template {{cookiecutter.k8s_namespace}} charts/argo-cd --values values/argo-cd-${ENVIRONMENT}-eu-w4.yaml | kubectl apply -f -

bootstrap-kms::
	gcloud kms keyrings create argocd --location global --project={{cookiecutter.gcp_project_stripped}}-stage
	gcloud kms keys create argocd-key --location global --keyring argocd --purpose encryption --project={{cookiecutter.gcp_project_stripped}}-stage
	gcloud kms keys list --location global --keyring argocd --project={{cookiecutter.gcp_project_stripped}}-stage
	gcloud kms encrypt --location=global --keyring=argocd --key=argocd-key --project={{cookiecutter.gcp_project_stripped}}-stage --ciphertext-file=resources/ssh/rc5-argocd.enc --plaintext-file=resources/credentials/rc5-argocd --project={{cookiecutter.gcp_project_stripped}}-stage

k8s-secrets::
	mkdir -p resources/credentials
	gcloud kms decrypt --location=global --keyring=argocd --key=argocd-key --ciphertext-file=resources/ssh/rc5-argocd.enc --plaintext-file=resources/credentials/rc5-argocd --project={{cookiecutter.gcp_project_stripped}}-stage
	kubectl create secret generic argocd-manifests-key --from-file=ssh-privatekey=resources/credentials/rc5-argocd --from-file=ssh-publickey=resources/ssh/rc5-argocd.pub -n {{cookiecutter.k8s_namespace}}

check-tools:: ## Check tools
ifneq "$(HELM_VERSION)" "3"
	echo "Helm v3 is required"
	echo "Have a look at 'helmenv' for convenience:"
	echo "  https://github.com/little-angry-clouds/kubernetes-binaries-managers/tree/master/cmd/helmenv"
	exit 1
endif
	helm repo list | grep argo || helm repo add argo https://argoproj.github.io/argo-helm
	helm repo update

##@ Infrastructure

cidocker:: ## build the latest ci image for testing
	@gcloud builds submit --tag gcr.io/{{cookiecutter.gcp_project_stripped}}-stage/ci-image:${VERSION_TAG} ./resources/ci-image/.

##@ Argo CD

argo-cd:: charts/argo-cd ## Render argocd chart
	echo "argo-cd:" && render-chart argocd/workloads/argo-cd.yaml
argocd:: argo-cd # alias

charts/argocd-notifications:
	helm pull argo/argocd-notifications --untar --untardir ./charts

argo-notifications:: charts/argocd-notifications ## Render argocd notifications chart
	echo "argo-notifications:" && render-chart workloads/argo-notifications.yaml
argocd-notifications:: argo-notifications # alias

argo-resources:: ## Render argocd resources, such as projects and app
	echo "argo-resources:" && render-chart workloads/argo-resources.yaml
resources:: argo-resources # alias

services::
	$(MAKE) {{cookiecutter.component_id}}

service-%::
	echo "$*:" && ./resources/make/bin/render-chart "argocd/workloads/service-$(dash-1).yaml" $(ENVIRONMENT)

digest:: ## Run kbld to replace image tags with digests
	kbld-digest ./manifests

##@ Pub/Sub to Kubectl

charts/pubsub2kubectl:
	rm -rf ./charts/pubsub2kubectl
	git clone git@github.com:trivago/pubsub2kubectl.git /tmp/p2k
	cp -r /tmp/p2k/chart/pubsub2kubectl ./charts
	rm -rf /tmp/p2k

pubsub2kubectl:: charts/pubsub2kubectl ## Render all pubsub2kubectl deployments
	echo "pubsub2kubectl previews:" && render-chart workloads/pubsub2kubectl-previews.yaml
	echo "pubsub2kubectl releases:" && render-chart workloads/pubsub2kubectl-releases.yaml

##@ GitHub Bots on Cloud Run

bots:: ## Deploy all bots
	make -C github-bots bots

##@ Misc

apply:: ## kubectl apply, e.g. WORKLOAD="argocd/workloads/argo-cd.yaml" DEPLOYMENT="edge-eu-w4" KUBECONFIG=path/to/kubeconfig
	deploy-chart $(WORKLOAD) $(DEPLOYMENT) $(KUBECONFIG)

render:: ## render all manifests
	$(MAKE) argo-cd argo-resources argo-notifications pubsub2kubectl services

help:: ## Display this help
	awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[\/%.a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

build-%::## build docker image localy and tag with latest. make build-producer or other component from the code folder
	@docker build -t gcr.io/{{cookiecutter.gcp_project_stripped}}-${ENVIRONMENT}/$(dash-1):latest -f ../code/$(dash-1)/Dockerfile ../code/ && docker push gcr.io/{{cookiecutter.gcp_project_stripped}}-${ENVIRONMENT}/$(dash-1):latest

gcr-%::## build and push to gcr with short hash from git for tag. make 
	@echo gcloud builds submit --tag gcr.io/{{cookiecutter.gcp_project_stripped}}-${ENVIRONMENT}-$(dash-2)/$(dash-1):latest ../code/$(dash-1)/.

images::
	$(MAKE) gcr-{{cookiecutter.component_id}}-${ENVIRONMENT}

##@ Terraform
terra-init::## make terra-plan
	@docker run --rm -e GOOGLE_APPLICATION_CREDENTIALS=/workdir/credentials.json -v ~/.config/gcloud:/root/.config/gcloud -v ~/.kube/config:/workdir/kube_config -e KUBE_CONFIG=/workdir/kube_config -v $(GOOGLE_APPLICATION_CREDENTIALS):/workdir/credentials.json -v ${PWD}/terraform:/workdir -w /workdir/deployments/${ENVIRONMENT} gcr.io/{{cookiecutter.gcp_project}}/deployer:v1 terraform init .

terra-plan::## make terra-plan
	@docker run --rm -e GOOGLE_APPLICATION_CREDENTIALS=/workdir/credentials.json -v ~/.config/gcloud:/root/.config/gcloud -v ~/.kube/config:/workdir/kube_config -e KUBE_CONFIG=/workdir/kube_config -v $(GOOGLE_APPLICATION_CREDENTIALS):/workdir/credentials.json -v ${PWD}/terraform:/workdir -w /workdir/deployments/${ENVIRONMENT} gcr.io/{{cookiecutter.gcp_project}}/deployer:v1 terraform plan -refresh=true .

terra-apply::## make terra-apply *skips approval to deploy directly
	@docker run --rm -e GOOGLE_APPLICATION_CREDENTIALS=/workdir/credentials.json -v ~/.config/gcloud:/root/.config/gcloud -v ~/.kube/config:/workdir/kube_config -e KUBE_CONFIG=/workdir/kube_config -v $(GOOGLE_APPLICATION_CREDENTIALS):/workdir/credentials.json -v ${PWD}/terraform:/workdir -w /workdir/deployments/${ENVIRONMENT} gcr.io/{{cookiecutter.gcp_project}}/deployer:v1 terraform apply -auto-approve -refresh=true .

##@ Deploy Locally

deploy::## deploy to environment locally 
			@gcloud --project={{cookiecutter.gcp_project_stripped}}-stage builds submit --config=../cloudbuild.yaml ../
