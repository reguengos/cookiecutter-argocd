variable "project" {
  description = "The id of the gcp project"
  default     = "{{cookiecutter.gcp_project}}-edge"
}

variable "region" {
  description = "The region of the gcp project"
  default     = "{{cookiecutter.gcp_region}}"
}

variable "k8s_cluster" {
  description = "Name of shared k8s cluster"
  default     = "{{cookiecutter.k8s_cluter_name}}"
}

variable "k8s_project" {
  description = "The id of the gcp project where shared k8s cluster is"
  default     = "{{cookiecutter.k8s_project}}"
}

variable "environment" {
  description = "The name of the environment"
  default     = "edge"
}

variable "namespace" {
  description = "The namespace of the project used in the shared kubernetes cluster"
  default     = "{{cookiecutter.k8s_namespace}}"
}