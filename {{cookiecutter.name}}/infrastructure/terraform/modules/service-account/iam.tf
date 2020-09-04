resource "google_service_account" "gsa" {
  provider   = google
  account_id = var.name
}

resource "google_project_iam_member" "role" {
  provider = google
  count    = length(var.roles)

  role   = "${dirname(var.roles[count.index]) == "custom" ? local.org-role : local.gcp-role}${basename(var.roles[count.index])}"
  member = "serviceAccount:${google_service_account.gsa.email}"
}

resource "google_project_iam_member" "external-role" {
  provider = google
  count    = length(local.external-projects)
  project  = local.external-projects[count.index]

  role   = "${dirname(local.external-roles[count.index]) == "custom" ? local.org-role : local.gcp-role}${basename(local.external-roles[count.index])}"
  member = "serviceAccount:${google_service_account.gsa.email}"
}

resource "google_service_account_iam_member" "workload-identity-binding" {
  provider = google-beta
  count    = length(var.namespaces)

  service_account_id = google_service_account.gsa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.k8s_project}.svc.id.goog[${var.namespaces[count.index]}/${var.name}]"
}

resource "kubernetes_service_account" "kubernetes-service-account" {
  count    = length(var.namespaces)
  metadata {
    name = var.name
    annotations = {
      "iam.gke.io/gcp-service-account" = google_service_account.gsa.email
    }
    namespace = var.namespaces[count.index]
  }
}

output "name" {
  value = var.name
}