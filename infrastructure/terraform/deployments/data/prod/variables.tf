variable "project" {
  description = "The id of the gcp project"
  default     = "trv-hs-src-conceptstream-prod"
}

variable "region" {
  description = "The region of the gcp project"
  default     = "europe-west4"
}

variable "environment" {
  description = "The name of the environment"
  default     = "prod"
}
