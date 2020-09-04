# Helm build stage
ARG HELM_VERSION
FROM alpine/helm:${HELM_VERSION} AS helm_provider

# Final build stage
FROM alpine
RUN apk update && apk add --no-cache make git bash rsync wget openssh curl

COPY --from=helm_provider /usr/bin/helm /usr/bin/
RUN ln -s /usr/bin/helm /usr/bin/helm3

ARG KBLD_VERSION
RUN wget -O /usr/bin/kbld "https://github.com/k14s/kbld/releases/download/v${KBLD_VERSION}/kbld-linux-amd64"
RUN chmod +x /usr/bin/kbld

ARG YQ_VERSION
RUN wget -O /usr/bin/yq "https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64"
RUN chmod +x /usr/bin/yq
