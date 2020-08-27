terraform {
  backend "gcs" {
    bucket = "conceptstream-terraform"
    prefix = "terraform/prod/data"
  }
}
provider "google" {
  project = var.project
  region  = var.region
}

resource "google_storage_bucket" "kafka_sink_bucket" {
  name     = "${terraform.workspace}_${var.environment}_kafka_sink"
  provider = google
  location = var.region
}

resource "google_storage_bucket" "concept_scores_bucket" {
  name     = "${terraform.workspace}_${var.environment}_concept_scores"
  provider = google
  location = var.region
}