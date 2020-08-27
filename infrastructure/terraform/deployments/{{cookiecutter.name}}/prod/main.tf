terraform {
  backend "gcs" {
    bucket = "conceptstream-terraform"
    prefix = "terraform/prod/conceptstream"
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

module "conceptstream-service-account" {
  source = "../../../modules/service-account"

  name        = "conceptstream-ksa"
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
    "serviceAccount:${var.k8s_project}.svc.id.goog[${var.namespace}/${module.conceptstream-service-account.name}]"
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

module "conceptstream-pubsub-storage-notification" {
  source = "../../../modules/pubsub-storage-notification"

  topic_name          = "rc5-concept-scores"
  bucket              = "${terraform.workspace}_${var.environment}_concept_scores"
  object_name_prefix  = "concept-scores/succeeded"

  message_retention_duration  = "1200s"
  retain_acked_messages       = false
  ack_deadline_seconds        = 10
  ttl                         = "300000.5s"

  members     = ["serviceAccount:service-${data.google_project.project.number}@gs-project-accounts.iam.gserviceaccount.com"]
  event_types = ["OBJECT_FINALIZE"]
}

module "rawinput-pubsub-storage-notification" {
  source = "../../../modules/pubsub-storage-notification"

  topic_name          = "rc5-raw-input"
  bucket              = "${terraform.workspace}_${var.environment}_concept_scores"
  object_name_prefix  = "raw-input"

  message_retention_duration  = "1200s"
  retain_acked_messages       = false
  ack_deadline_seconds        = 10
  ttl                         = "300000.5s"

  members     = ["serviceAccount:service-${data.google_project.project.number}@gs-project-accounts.iam.gserviceaccount.com"]
  event_types = ["OBJECT_FINALIZE"]
}