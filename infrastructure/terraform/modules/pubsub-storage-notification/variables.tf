variable "topic_name" {
  type = string
}

variable "bucket" {
  type = string
}

variable "object_name_prefix" {
  type = string
}

variable "message_retention_duration" {
  type = string
}

variable "retain_acked_messages" {
  type = bool
}

variable "ack_deadline_seconds" {
  type = number
}

variable "ttl" {
  type = string
}

variable "members" {
  type = list(string)
}

variable "event_types" {
  type = list(string)
}