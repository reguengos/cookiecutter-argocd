resource "google_pubsub_topic" "topic" {
  provider  = google
  name      = var.topic_name
}

resource "google_pubsub_subscription" "subscription" {
  provider  = google
  name      = var.topic_name
  topic     = google_pubsub_topic.topic.id

  # 20 minutes
  message_retention_duration  = var.message_retention_duration
  retain_acked_messages       = var.retain_acked_messages

  ack_deadline_seconds        = var.ack_deadline_seconds

  expiration_policy {
    ttl = var.ttl
  }
}

resource "google_pubsub_topic_iam_binding" "binding" {
  topic   = google_pubsub_topic.topic.id
  role    = "roles/pubsub.publisher"

  members = var.members
}

resource "google_storage_notification" "notification" {
  bucket              = var.bucket
  payload_format      = "JSON_API_V1"
  topic               = google_pubsub_topic.topic.id
  event_types         = var.event_types
  depends_on          = [google_pubsub_topic_iam_binding.binding]
  object_name_prefix  = var.object_name_prefix
}