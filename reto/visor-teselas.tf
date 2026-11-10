# RETO FINAL · ¿Cuántos problemas de seguridad encuentras? (hay trampas a propósito)
resource "google_storage_bucket" "teselas" {
  name                        = "igeo-visor-teselas"
  location                    = "europe-southwest1"
  uniform_bucket_level_access = false
}

resource "google_storage_bucket_iam_member" "lectura" {
  bucket = google_storage_bucket.teselas.name
  role   = "roles/storage.objectViewer"
  member = "allAuthenticatedUsers"
}

resource "google_service_account" "visor" {
  account_id = "visor-teselas"
}

resource "google_service_account_key" "visor" {
  service_account_id = google_service_account.visor.name
}

output "clave_visor" {
  value = google_service_account_key.visor.private_key
}

resource "google_compute_firewall" "escritorio_remoto" {
  name    = "permitir-rdp"
  network = "default"
  allow {
    protocol = "tcp"
    ports    = ["3389"]
  }
  source_ranges = ["0.0.0.0/0"]
}
