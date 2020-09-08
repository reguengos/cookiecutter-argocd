# {{cookiecutter.component_id}}


## Authenticating with the GKE cluster

The following command will configure your local kubectl to be able to speak with the data proc stage cluster.

`gcloud container clusters get-credentials datproc-shared-stage-eu-w4 --region europe-west4 --project trv-hs-kubernetes-stage`

## Secrets

[KMS](https://cloud.google.com/sdk/gcloud/reference/kms)Secrets are encrypted using google KMS, you can decrypt any secret by having access to the google project `{{cookiecutter.gcp_project_stripped}}-{edge,stage,prod}` for the according secrets.

### Example
To produce the origional secret for our deployments the following commands were used.

```
gcloud kms keyrings create argocd --location global

gcloud kms keys create argocd-key --location global --keyring argocd --purpose encryption

gcloud kms keys list --location global --keyring argocd

gcloud kms encrypt --location=global --keyring=argocd --key=argocd-key --project={{cookiecutter.gcp_project_stripped}}-stage --ciphertext-file=infrastructure/resources/ssh/argocd.enc --plaintext-file=infrastructure/resources/credentials/argocd

```
To recreate the origional unencrypted file for the ssh private key you could use the following to store it locally in the credentials folder which is also found in `.gitignore`

```
gcloud kms decrypt --location=global --keyring=argocd --key=argocd-key --project={{cookiecutter.gcp_project_stripped}}-stage --ciphertext-file=infrastructure/resources/ssh/argocd.enc --plaintext-file=infrastructure/resources/credentials/argocd
```

When using the gcloud make sure your project is set correctly. For example when trying to access stage use:
`gcloud config set project {{cookiecutter.gcp_project_stripped}}-stage`

## Folder Structure ./infrastructure/

### Argocd

The `argocd` directory contains the configuration for argocd continuious deployment

### Resources

The `resources` dir holds general tools, credentials, and dockerfiles to support the build/release process

### Terraform

The `terraform` dir provides the nessicary terraform formulas to setup basic permissions for your namespace and service account

---

### GitHub

Home of the GitHub bots to support the process.

### Manifests

Do not check this into your main source code repo, but let your CI pipeline check it into a manifests repository; please see the main documentation in this repo for more information on the topic.


