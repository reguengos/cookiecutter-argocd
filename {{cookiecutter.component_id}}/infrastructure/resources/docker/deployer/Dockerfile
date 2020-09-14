
FROM gcr.io/google.com/cloudsdktool/cloud-sdk:latest

ENV TERRAFORM_VERSION 0.13.2
ENV CLOUD_SDK_VERSION 237.0.0

# Google cloud SDK

WORKDIR /
RUN apt update && apt install -y \
        wget \
        unzip \
        openssh-client 
RUN gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment github_docker_image
VOLUME ["/root/.config"]

# Terraform and xterrafile/yamllint to handle terraform modules

WORKDIR $GOPATH/src/github.com/hashicorp/terraform
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/bin && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip
