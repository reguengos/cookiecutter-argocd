variable "project" {
  description = "The id of the gcp project"
  default     = "{{cookiecutter.gcp_project}}"
}

variable "region" {
  description = "The region of the gcp project"
  default     = "{{cookiecutter.gcp_region}}"
}

variable "environment" {
  description = "The name of the environment"
  default     = "stage"
}
