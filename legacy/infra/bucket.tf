# Bucket de informes del visor (heredado, 2022). Ejemplo con fallos deliberados.
resource "google_storage_bucket" "informes" {
  name          = "igeo-visor-informes"
  location      = "EU"
  force_destroy = true
}

# "Para que BI lo lea desde cualquier sitio"
resource "google_storage_bucket_iam_member" "lectura_publica" {
  bucket = google_storage_bucket.informes.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

resource "google_compute_firewall" "ssh" {
  name    = "permitir-ssh"
  network = "default"
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  source_ranges = ["35.235.240.0/20"]
}
