# Cloudbuilder

A container will required tooling we need in our Google Cloud Build pipelines.

## Rationale

Avoid building and pulling one container for each tool.

## Tools 

- bash
- curl
- git
- make
- helm3
- kbld
- rsync
- wget
- ssh
- yq

## Build

All versions are defined in the `cloudbuild.yaml` file.

```sh
gcloud builds submit --project=trv-hs-bookinglink-stage --config=cloudbuild.yaml .
```

The image is now available as `gcr.io/trv-hs-bookinglink-stage/cloudbuilder`.
