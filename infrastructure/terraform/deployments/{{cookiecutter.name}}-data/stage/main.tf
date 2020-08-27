terraform {
  backend "gcs" {
    bucket = "{{cookiecutter.name}}-terraform"
    prefix = "terraform/data"
  }
}
provider "google" {
  project = var.project
  region  = var.region
}

resource "google_storage_bucket" "{{cookiecutter.name}}_bucket" {
  name     = "${terraform.workspace}_${var.environment}_{{cookiecutter.name}}"
  provider = google
  location = var.region
}

