# RC5

The RC5 pipeline produces two Kafka streams.

* `content_synchronised.accommodation.concept_score_RC5`
* `content_synchronised.concept.concept_RC5`

If you want to know more about what RC5 does, where it gets its data, and why it has such an odd name, you should check out the [Introduction to RC5](https://paper.dropbox.com/doc/RC5-Introduction--A1dxXfKtqWUzHGRYWDn6zqjKAQ-BXv4JvLjMGGDHHwoygu71).

**Current status**: We are migrating the RC5 pipeline from AWS to GCP. This repository is for the GCP pipeline. The GCP pipeline isn't live yet. For more information about the AWS pipeline, you can read the [general overview](https://paper.dropbox.com/doc/RC5-documentation--A1fNjjh2yTbZqdVvYLXbST~2Ag-ooptKjHM2IVh9H9HKKBIR#:uid=243739316217785128051654&h2=General-Overview) or take a look at its [main repository](https://github.com/trivago/hp-pricesearch-emulator).

## Services

The RC5 pipeline consists of multiple services. All source code of the services is located in the `micro-services` subfolder.

Service | Description
--------|------------
[Concept score producer](services/concept-score-producer/README.md) | Writes data to the Kafka topic `content_synchronised.accommodation.concept_score_RC5`.  
[Transformer](services/tranformer/README.md) | Transforms the input data from its native data schema to the data schema of the RC5 stream.
[Consumer](services/consumer/README.md) | Reads Kafka topics that are of interest to the RC5 pipeline.


## Authenticating with the GKE cluster

The following command will configure your local kubectl to be able to speak with the data proc stage cluster.

`gcloud container clusters get-credentials datproc-shared-stage-eu-w4 --region europe-west4 --project trv-hs-kubernetes-stage`

## Secrets

[KMS](https://cloud.google.com/sdk/gcloud/reference/kms)Secrets are encrypted using google KMS, you can decrypt any secret by having access to the google project `trv-hs-src-conceptscore-{edge,stage,prod}` for the according secrets.

### Example
To produce the origional secret for our deployments the following commands were used.

```
gcloud kms keyrings create argocd --location global

gcloud kms keys create argocd-key --location global --keyring argocd --purpose encryption

gcloud kms keys list --location global --keyring argocd

gcloud kms encrypt --location=global --keyring=argocd --key=argocd-key --project={{cookiecutter.gcp_project}}-stage --ciphertext-file=infrastructure/resources/ssh/argocd.enc --plaintext-file=infrastructure/resources/credentials/argocd

```
To recreate the origional unencrypted file for the ssh private key you could use the following to store it locally in the credentials folder which is also found in `.gitignore`

```
gcloud kms decrypt --location=global --keyring=argocd --key=argocd-key --project={{cookiecutter.gcp_project}}-stage --ciphertext-file=infrastructure/resources/ssh/argocd.enc --plaintext-file=infrastructure/resources/credentials/argocd
```

When using the gcloud make sure your project is set correctly. For example when trying to access stage use:
`gcloud config set project {{cookiecutter.gcp_project}}-stage`

## Folder Structure ./infrastructure/

### Charts

The `charts` directory contains templates Kubernetes manifests which are rendered using Helm. Add your own charts here as well.

### Values

The `values` dir holds the configuration files in order to populate the Helm charts for the different deployments. Add your value files here as you go.

### Workloads

The `workloads` dir brings the `values` and `charts` together by defining what to render. The `Makefile` will call a utility and pass a workloads file as argument.

---

### GitHub

Home of the GitHub bots to support the process.

### Resources

The `resources` dir is used for arbitrary resources; e.g. the `make/bin` dir is automatically added to the `PATH` when the `Makefile` runs.
Put misc stuff here.

### Manifests

Do not check this into your main source code repo, but let your CI pipeline check it into a manifests repository; please see the main documentation in this repo for more information on the topic.

## Contribute

If you have an idea how to make this package more reusable *without* magic, I'd highly apreciate your porposal in a pull-request.


# TODO

- Automate access from cloudbuild to kms decrypter iam role
- Automate access from cloudbuild to container registry (artifact write) iam role
- How to tag releases, from master, tagged, ???
- Create kafka topics for input/output
- GCR api needs to be enabled for new projects manually
