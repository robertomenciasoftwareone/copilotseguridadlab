variable "project_id" {
  description = "ID del proyecto de Google Cloud donde se crea el bucket de informes."
  type        = string
}

variable "location" {
  description = "Región del bucket. Debe estar en la UE."
  type        = string
  default     = "europe-southwest1"

  validation {
    condition     = can(regex("^europe-", var.location)) || var.location == "EU"
    error_message = "La ubicación debe estar en la UE (europe-* o EU)."
  }
}

variable "bucket_logs" {
  description = "Nombre del bucket de auditoría donde se envían los logs de acceso."
  type        = string
}

variable "kms_key" {
  description = "ID completo de la clave CMEK (Cloud KMS) para cifrar los informes."
  type        = string
}

variable "bi_group" {
  description = "Grupo de Google (sin prefijo) del equipo de BI con acceso de solo lectura."
  type        = string
}

resource "google_storage_bucket" "informes_organismos" {
  project                     = var.project_id
  name                        = "${var.project_id}-informes-organismos"
  location                    = var.location
  storage_class               = "STANDARD"
  force_destroy               = false
  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  encryption {
    default_kms_key_name = var.kms_key
  }

  logging {
    log_bucket        = var.bucket_logs
    log_object_prefix = "informes-organismos"
  }
}

# Lectura para BI mediante grupo: accesible desde cualquier sitio con su cuenta corporativa, sin hacer el bucket público.
resource "google_storage_bucket_iam_member" "bi_lectura" {
  bucket = google_storage_bucket.informes_organismos.name
  role   = "roles/storage.objectViewer"
  member = "group:${var.bi_group}"
}
