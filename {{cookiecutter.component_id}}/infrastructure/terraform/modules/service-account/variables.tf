variable "name" {
  type = string
}

variable "environment" {
  type = string
}

variable "region" {
  type = string
}

variable "namespaces" {
  description = "workload identity binding namespaces"
  type = list(string)
}

variable "roles" {
  description = "Roles to assign in the current project"
  type = list(string)
}

variable "externalRole" {
  description = "Assign one role in an external project. Map project to role"
  type    = map(string)
  default = {}
}

variable "k8s_project" {
  description = "The project in which the shared resources will be accessed from"
  type        = string
}

data "google_project" "self" {
}

data "google_organization" "trivago" {
  domain = "trivago.com"
}

output "config" {
  value = {
    account_id      = google_service_account.gsa.account_id
    kubernetes-name = var.name
    namespaces      = join(",", var.namespaces)
  }
}

locals {
  org-role = "${data.google_organization.trivago.name}/roles/"
  gcp-role = "roles/"

  external-projects = keys(var.externalRole)
  external-roles    = values(var.externalRole)
}

