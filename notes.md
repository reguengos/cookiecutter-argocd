```bash
gcloud config set project trv-io-sre-testing-stage
gcloud container clusters get-credentials tools-stage0-eu-w4 --region europe-west4 --project trv-shared-kubernetes-stage
gcloud container clusters get-credentials build-prod0-eu-w4	 --region europe-west4 --project trv-shared-kubernetes-prod
kubectl config set-context --current --namespace=sre-playground
```
```bash
cookiecutter -f --no-input .
```


## TODO
- kms api needs to be enabled at project creation or during a first init stage via this repo, possibly both to double confirm
- enable cloudbuild api as described above as well
- make targets for terraform aren't finding the bucket even though locally running works fine
- add some logic so if the docker images already exist not to build them for every bootstrap command
