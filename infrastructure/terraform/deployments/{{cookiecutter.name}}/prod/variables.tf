variable "project" {
  description = "The id of the gcp project"
  default     = "{{cookiecutter.gcp_project}}-prod"
}

variable "region" {
  description = "The region of the gcp project"
  default     = "europe-west4"
}

variable "k8s_cluster" {
  description = "Name of shared k8s cluster"
  default     = "datproc-shared-prod-eu-w4"
}

variable "k8s_project" {
  description = "The id of the gcp project where shared k8s cluster is"
  default     = "trv-hs-kubernetes-prod"
}

variable "environment" {
  description = "The name of the environment"
  default     = "prod"
}

variable "namespace" {
  description = "The namespace of the project used in the shared kubernetes cluster"
  default     = "{{cookiecutter.k8s_namespace}}"
}
