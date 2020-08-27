variable "project" {
  description = "The id of the gcp project"
  default     = "trv-hs-src-conceptstream-stage"
}

variable "region" {
  description = "The region of the gcp project"
  default     = "europe-west4"
}

variable "k8s_cluster" {
  description = "Name of shared k8s cluster"
  default     = "datproc-shared-stage-eu-w4"
}

variable "k8s_project" {
  description = "The id of the gcp project where shared k8s cluster is"
  default     = "trv-hs-kubernetes-stage"
}

variable "k8s_project_prod" {
  description = "The id of the production k8s project in gcp"
  default     = "trv-hs-kubernetes-prod"
}

variable "environment" {
  description = "The name of the environment"
  default     = "stage"
}

variable "namespace" {
  description = "The namespace of the project used in the shared kubernetes cluster"
  default     = "src-conceptstream"
}
