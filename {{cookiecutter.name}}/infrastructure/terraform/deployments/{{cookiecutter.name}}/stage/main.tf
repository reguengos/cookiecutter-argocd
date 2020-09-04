terraform {
  backend "gcs" {
    bucket = "{{cookiecutter.name}}-terraform"
    prefix = "terraform/{{cookiecutter.name}}"
  }
}
provider "google" {
  project = var.project
  region  = var.region
}

provider "google" {
  alias   = "k8s_project"
  project = var.k8s_project
  region  = var.region
}

provider "kubernetes" {
  host = "https://${data.google_container_cluster.k8s_cluster.endpoint}"
}

data "google_container_cluster" "k8s_cluster" {
  provider = google.k8s_project
  name     = var.k8s_cluster
  location = var.region
}

data "google_project" "project" {
}

data "google_project" "k8s_project" {
  project_id = var.k8s_project
}

data "google_project" "k8s_project_prod" {
  project_id = var.k8s_project_prod
}

module "{{cookiecutter.name}}-service-account" {
  source = "../../../modules/service-account"

  name        = "{{cookiecutter.name}}-ksa"
  environment = var.environment
  region      = var.region

  namespaces = ["{{cookiecutter.k8s_namespace}}"]
  roles      = ["storage.objectAdmin", "pubsub.admin", "datastore.user"]

  k8s_project = var.k8s_project
}

resource "google_storage_bucket_iam_binding" "binding" {
  bucket = "${terraform.workspace}_${var.environment}_kafka_sink"
  role   = "roles/storage.objectAdmin"

  members = [
    "serviceAccount:${var.k8s_project}.svc.id.goog[${var.namespace}/${module.{{cookiecutter.name}}-service-account.name}]"
  ]
}

resource "google_container_registry" "registry" {
  project  = var.project
  location = "EU"
}

resource "google_project_iam_member" "kubernetes-service-compute-user" {
  project = var.project
  role    = "roles/storage.objectViewer"
  member  =  "serviceAccount:${data.google_project.k8s_project.number}-compute@developer.gserviceaccount.com"
}

resource "google_project_iam_member" "kubernetes-service-compute-user-prod" {
  project = var.project
  role    = "roles/storage.objectViewer"
  member  =  "serviceAccount:${data.google_project.k8s_project_prod.number}-compute@developer.gserviceaccount.com"
}

